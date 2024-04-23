#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.02.18 05:00:00                  #
# ================================================== #

from pygpt_net.item.assistant import AssistantItem
from pygpt_net.utils import trans


class Editor:
    def __init__(self, window=None):
        """
        Assistants editor controller

        :param window: Window instance
        """
        self.window = window
        self.options = {
            "id": {
                "type": "text",
                "label": "assistant.id",
            },
            "name": {
                "type": "text",
                "label": "assistant.name",
            },
            "description": {
                "type": "text",
                "label": "assistant.description",
            },
            "model": {
                "type": "combo",
                "use": "models",
                "keys": [],
                "label": "assistant.model",
            },
            "instructions": {
                "type": "textarea",
                "label": "assistant.instructions",
            },
            "tool.code_interpreter": {
                "type": "bool",
                "label": "assistant.tool.code_interpreter",
                "value": True,
            },
            "tool.retrieval": {
                "type": "bool",
                "label": "assistant.tool.retrieval",
                "value": False,
            },
            "tool.function": {
                "type": "dict",
                "label": "assistant.tool.function",
                "keys": {
                    'name': 'text',
                    'params': 'textarea',
                    'desc': 'textarea',
                },
            },
        }
        self.id = "assistant"

    def get_options(self):
        """
        Get options list

        :return: options list
        """
        return self.options

    def get_option(self, key: str):
        """
        Get option by key

        :param key: option key
        :return: option
        """
        if key in self.options:
            return self.options[key]

    def setup(self):
        """Setup editor"""
        parent = "assistant"
        key = "tool.function"
        self.window.ui.dialogs.register_dictionary(
            key,
            parent,
            self.get_option(key),
        )

    def edit(self, idx: int = None):
        """
        Open assistant editor

        :param idx: assistant index (row index)
        """
        id = None
        if idx is not None:
            id = self.window.core.assistants.get_by_idx(idx)

        self.init(id)
        self.window.ui.dialogs.open_editor('editor.assistants', idx, width=800)

    def init(self, id: str = None):
        """
        Initialize assistant editor

        :param id: assistant ID (in API)
        """
        assistant = self.window.core.assistants.create()
        assistant.model = "gpt-4-1106-preview"  # default model

        # if editing existing assistant
        if id is not None and id != "":
            if self.window.core.assistants.has(id):
                assistant = self.window.core.assistants.get_by_id(id)
        else:
            # defaults
            assistant.instructions = 'You are a helpful assistant.'
            assistant.tools['code_interpreter'] = True
            assistant.tools['retrieval'] = True

        if assistant.name is None:
            assistant.name = ""
        if assistant.description is None:
            assistant.description = ""
        if assistant.instructions is None:
            assistant.instructions = ""
        if assistant.model is None:
            assistant.model = ""

        options = {}
        data_dict = assistant.to_dict()
        for key in self.options:
            options[key] = self.options[key]
            options[key]['value'] = data_dict[key]
            if options[key]['value'] is None:
                options[key]['value'] = ""

        self.window.controller.config.load_options(self.id, options)

        # restore functions
        if assistant.has_functions():
            functions = assistant.get_functions()
            values = []
            for function in functions:
                values.append(
                    {
                        "name": function['name'],
                        "params": function['params'],
                        "desc": function['desc'],
                    }
                )
            self.window.ui.config[self.id]['tool.function'].items = values
            self.window.ui.config[self.id]['tool.function'].model.updateData(values)
        else:
            self.window.ui.config[self.id]['tool.function'].items = []
            self.window.ui.config[self.id]['tool.function'].model.updateData([])

        # set focus to name field
        self.window.ui.config[self.id]['name'].setFocus()

    def save(self):
        """Save assistant"""
        created = False
        id = self.window.controller.config.get_value(
            parent_id=self.id, 
            key='id', 
            option=self.options['id'],
        )  # empty or not
        name = self.window.controller.config.get_value(
            parent_id=self.id, 
            key='name', 
            option=self.options['name'],
        )
        model = self.window.controller.config.get_value(
            parent_id=self.id, 
            key='model', 
            option=self.options['model'],
        )

        # check name
        if name is None or name == "" or model is None or model == "":
            self.window.ui.dialogs.alert(
                trans('assistant.form.empty.fields')
            )
            return

        if id is None or id == "" or not self.window.core.assistants.has(id):
            assistant = self.window.controller.assistant.create()  # id is created in API here
            if assistant is None:
                print("ERROR: Assistant not created!")
                return
            id = assistant.id  # set to ID created in API
            self.window.core.assistants.add(assistant)
            self.window.controller.config.apply_value(
                parent_id=self.id,
                key="id",
                option=self.options["id"],
                value=id,
            )
            created = True
        else:
            assistant = self.window.core.assistants.get_by_id(id)

        # assign data from fields to assistant object
        self.assign_data(assistant)

        # update data in API if only updating data here (not creating)
        if not created:
            self.window.controller.assistant.update_data(assistant)

        # save
        self.window.core.assistants.save()
        self.window.controller.assistant.refresh()
        self.window.controller.assistant.update()

        self.window.ui.dialogs.close('editor.assistants')
        self.window.ui.status(trans('status.assistant.saved'))

        # switch to edited assistant
        self.window.controller.assistant.select_by_id(id)

    def assign_data(self, assistant: AssistantItem):
        """
        Assign data from fields to assistant

        :param assistant: assistant
        """
        model = self.window.controller.config.get_value(
            parent_id=self.id,
            key='model',
            option=self.options['model'],
        )
        if model == '_':
            model = None

        assistant.name = self.window.controller.config.get_value(
            parent_id=self.id,
            key='name',
            option=self.options['name'],
        )
        assistant.model = model
        assistant.description = self.window.controller.config.get_value(
            parent_id=self.id,
            key='description',
            option=self.options['description'],
        )
        assistant.instructions = self.window.controller.config.get_value(
            parent_id=self.id,
            key='instructions',
            option=self.options['instructions'],
        )
        assistant.tools = {
            'code_interpreter': self.window.controller.config.get_value(
                parent_id=self.id,
                key='tool.code_interpreter',
                option=self.options['tool.code_interpreter'],
            ),
            'retrieval': self.window.controller.config.get_value(
                parent_id=self.id,
                key='tool.retrieval',
                option=self.options['tool.retrieval'],
            ),
            'function': [],  # functions are assigned separately (below)
        }

        # assign assistant's functions tool
        values = self.window.controller.config.get_value(
                parent_id=self.id,
                key='tool.function',
                option=self.options['tool.function'],
        )
        functions = []
        for function in values:
            name = function['name']
            params = function['params']
            desc = function['desc']
            if name is None or name == "":
                continue
            if params is None or params == "":
                params = '{"type": "object", "properties": {}}'  # default empty JSON params
            if desc is None:
                desc = ""
            functions.append(
                {
                    "name": name,
                    "params": params,
                    "desc": desc,
                }
            )

        if len(functions) > 0:
            assistant.tools['function'] = functions
        else:
            assistant.tools['function'] = []
