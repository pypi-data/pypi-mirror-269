######################################################################################################################
# Copyright (C) 2017-2022 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
Contains unit tests for the OptionsWidget class.

"""
import unittest
from unittest.mock import MagicMock
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QLineEdit, QSpinBox
from PySide6.QtGui import QUndoStack
from spine_items.importer.widgets.options_widget import OptionsWidget


class TestOptionsWidget(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not QApplication.instance():
            QApplication()

    def setUp(self):
        self._undo_stack = QUndoStack()

    def test_spin_box_change_signalling(self):
        option_template = {"number": {"label": "int value", "type": int, "default": 0}}
        connector = MagicMock()
        connector.connection.BASE_OPTIONS = {}
        connector.connection.OPTIONS = option_template
        widget = OptionsWidget(self._undo_stack)
        widget.set_connector(connector)
        layout = widget.form_layout
        checked = {"number": False}
        for item in (layout.itemAt(i).widget() for i in range(layout.count())):
            if isinstance(item, QSpinBox):
                item.setValue(23)
                connector.update_options.assert_called_once_with({"number": 23})
                checked["number"] = True
                break
        self.assertTrue(all(checked.values()))

    def test_line_edit_change_signalling(self):
        option_template = {"text": {"label": "text value", "type": str, "default": ""}}
        connector = MagicMock()
        connector.connection.BASE_OPTIONS = {}
        connector.connection.OPTIONS = option_template
        widget = OptionsWidget(self._undo_stack)
        widget.set_connector(connector)
        layout = widget.form_layout
        checked = False
        for item in (layout.itemAt(i).widget() for i in range(layout.count())):
            if isinstance(item, QLineEdit):
                item.setText("the text has been set")
                connector.update_options.assert_called_once_with({"text": "the text has been set"})
                checked = True
                break
        self.assertTrue(checked)

    def test_combo_box_change_signalling(self):
        option_template = {
            "choice": {"label": "a choice", "type": list, "Items": ["choice a", "choice b"], "default": "choice a"}
        }
        connector = MagicMock()
        connector.connection.BASE_OPTIONS = {}
        connector.connection.OPTIONS = option_template
        widget = OptionsWidget(self._undo_stack)
        widget.set_connector(connector)
        layout = widget.form_layout
        checked = False
        for item in (layout.itemAt(i).widget() for i in range(layout.count())):
            if isinstance(item, QComboBox):
                item.setCurrentText("choice b")
                connector.update_options.assert_called_once_with({"choice": "choice b"})
                checked = True
                break
        self.assertTrue(checked)

    def test_check_box_change_signalling(self):
        option_template = {"yesno": {"label": "check me", "type": bool, "default": True}}
        connector = MagicMock()
        connector.connection.BASE_OPTIONS = {}
        connector.connection.OPTIONS = option_template
        widget = OptionsWidget(self._undo_stack)
        widget.set_connector(connector)
        layout = widget.form_layout
        checked = False
        for item in (layout.itemAt(i).widget() for i in range(layout.count())):
            if isinstance(item, QCheckBox):
                item.setChecked(False)
                connector.update_options.assert_called_once_with({"yesno": False})
                checked = True
                break
        self.assertTrue(checked)

    def test_set_connector_makes_copy_of_connections_base_options(self):
        option_template = {"yesno": {"label": "check me", "type": bool, "default": True}}
        connector = MagicMock()
        connector.connection.BASE_OPTIONS = {"text": {"label": "text value", "type": str, "default": ""}}
        connector.connection.OPTIONS = option_template
        widget = OptionsWidget(self._undo_stack)
        widget.set_connector(connector)
        self.assertEqual(
            connector.connection.BASE_OPTIONS, {"text": {"label": "text value", "type": str, "default": ""}}
        )


if __name__ == '__main__':
    unittest.main()
