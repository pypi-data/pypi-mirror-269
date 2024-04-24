#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.02.15 01:00:00                  #
# ================================================== #

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QLabel, QVBoxLayout, QSplitter, QWidget, QSizePolicy

from pygpt_net.ui.base.config_dialog import BaseConfigDialog
from pygpt_net.ui.widget.dialog.editor import EditorDialog
from pygpt_net.utils import trans


class Assistant(BaseConfigDialog):
    def __init__(self, window=None, *args, **kwargs):
        super(Assistant, self).__init__(window, *args, **kwargs)
        """
        Assistant editor dialog

        :param window: Window instance
        """
        self.window = window
        self.id = "assistant"
        self.dialog_id = "assistants"

    def setup(self):
        """Setups assistant editor dialog"""
        self.window.ui.nodes['assistant.btn.save'] = QPushButton(trans("dialog.assistant.btn.save"))
        self.window.ui.nodes['assistant.btn.save'].clicked.connect(
            lambda: self.window.controller.assistant.editor.save()
        )
        self.window.ui.nodes['assistant.btn.save'].setAutoDefault(True)

        footer = QHBoxLayout()
        footer.addWidget(self.window.ui.nodes['assistant.btn.save'])

        # get option fields config
        fields = self.window.controller.assistant.editor.get_options()

        # build settings widgets
        widgets = self.build_widgets(self.id, fields)  # from base config dialog

        # apply settings widgets
        for key in widgets:
            self.window.ui.config[self.id][key] = widgets[key]

        # btn: add function
        self.window.ui.config[self.id]['tool.function'].add_btn.setText(trans('assistant.func.add'))
        # Empty params: {"type": "object", "properties": {}}

        # set tips
        self.window.ui.nodes['assistant.id_tip'] = QLabel(trans('assistant.new.id_tip'))
        self.window.ui.nodes['assistant.id_tip'].setMinimumHeight(40)

        self.window.ui.nodes['assistant.api.tip'] = QPushButton(trans('assistant.api.tip'))  # TODO: url btn
        self.window.ui.nodes['assistant.api.tip'].setAutoDefault(False)
        self.window.ui.nodes['assistant.api.tip'].setFlat(True)
        self.window.ui.nodes['assistant.api.tip'].setStyleSheet(
            "text-align: left; "
            "color: #fff; "
            "text-decoration: underline; "
            "text-transform: none;"
        )
        self.window.ui.nodes['assistant.api.tip'].setStyleSheet("text-transform: none;")
        self.window.ui.nodes['assistant.api.tip'].setCursor(Qt.PointingHandCursor)
        self.window.ui.nodes['assistant.api.tip'].clicked.connect(
            lambda: self.window.controller.assistant.goto_online()
        )

        # apply widgets to layouts
        options = {}
        for key in widgets:
            if fields[key]["type"] == 'text' or fields[key]["type"] == 'int' or fields[key]["type"] == 'float':
                options[key] = self.add_option(widgets[key], fields[key])
            elif fields[key]["type"] == 'textarea':
                options[key] = self.add_row_option(widgets[key], fields[key])
            elif fields[key]["type"] == 'bool':
                options[key] = self.add_raw_option(widgets[key], fields[key])
            elif fields[key]["type"] == 'dict':
                options[key] = self.add_row_option(widgets[key], fields[key])
                if key == "tool.function":
                    widgets[key].setMinimumHeight(150)
            elif fields[key]["type"] == 'combo':
                options[key] = self.add_option(widgets[key], fields[key])

        self.window.ui.nodes['assistant.tool.function.label'].setVisible(False)  # hide label
        self.window.ui.nodes['assistant.id_tip'].setAlignment(Qt.AlignCenter)

        options["tool.code_interpreter"].setAlignment(Qt.AlignCenter)
        options["tool.retrieval"].setAlignment(Qt.AlignCenter)

        rows = QVBoxLayout()
        rows.addLayout(options["id"])
        rows.addLayout(options["name"])
        rows.addLayout(options["description"])
        rows.addLayout(options["model"])
        rows.addWidget(self.window.ui.nodes['assistant.id_tip'])
        rows.addWidget(self.window.ui.nodes['assistant.api.tip'])
        rows.setContentsMargins(0, 0, 0, 0)

        rows_tools = QHBoxLayout()
        rows_tools.addLayout(options["tool.code_interpreter"])
        rows_tools.addLayout(options["tool.retrieval"])
        rows_tools.setContentsMargins(0, 0, 0, 0)

        rows.addLayout(rows_tools)
        rows.addStretch()

        widget_base = QWidget()
        widget_base.setLayout(rows)

        widget_base.setMinimumWidth(400)
        widget_base.setMaximumWidth(450)

        widget_prompt = QWidget()
        widget_prompt.setLayout(options["instructions"])
        widget_prompt.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        options["instructions"].setContentsMargins(0, 0, 0, 0)
        options["tool.function"].setContentsMargins(0, 0, 0, 0)

        widget_tools = QWidget()
        widget_tools.setLayout(options["tool.function"])
        widget_tools.setMinimumWidth(400)

        main = QHBoxLayout()
        main.addWidget(widget_base)
        main.addWidget(widget_tools)
        main.setContentsMargins(0, 0, 0, 0)

        widget_main = QWidget()
        widget_main.setLayout(main)

        self.window.ui.splitters['editor.assistant'] = QSplitter(Qt.Vertical)
        self.window.ui.splitters['editor.assistant'].addWidget(widget_main)
        self.window.ui.splitters['editor.assistant'].addWidget(widget_prompt)
        self.window.ui.splitters['editor.assistant'].setStretchFactor(0, 1)
        self.window.ui.splitters['editor.assistant'].setStretchFactor(1, 2)

        layout = QVBoxLayout()
        layout.addWidget(self.window.ui.splitters['editor.assistant'])
        layout.addLayout(footer)

        self.window.ui.dialog['editor.' + self.dialog_id] = EditorDialog(self.window, self.dialog_id)
        self.window.ui.dialog['editor.' + self.dialog_id].setLayout(layout)
        self.window.ui.dialog['editor.' + self.dialog_id].setWindowTitle(trans('dialog.assistant'))
