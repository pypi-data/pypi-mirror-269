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
Unit tests for ProjectItemModel class.
"""

from tempfile import TemporaryDirectory
import unittest
from unittest.mock import NonCallableMagicMock
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from spinetoolbox.mvcmodels.project_item_model import ProjectItemModel
from spinetoolbox.mvcmodels.project_tree_item import CategoryProjectTreeItem, LeafProjectTreeItem, RootProjectTreeItem
from spinetoolbox.project_item.project_item import ProjectItem
from ..mock_helpers import clean_up_toolbox, create_toolboxui_with_project


class TestProjectItemModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not QApplication.instance():
            QApplication()

    def setUp(self):
        """Sets up toolbox."""
        self._temp_dir = TemporaryDirectory()
        self.toolbox = create_toolboxui_with_project(self._temp_dir.name)

    def tearDown(self):
        """Cleans up."""
        clean_up_toolbox(self.toolbox)
        self._temp_dir.cleanup()

    def test_empty_model(self):
        root = RootProjectTreeItem()
        model = ProjectItemModel(root)
        self.assertEqual(model.rowCount(), 0)
        self.assertEqual(model.columnCount(), 1)
        self.assertEqual(model.n_items(), 0)
        self.assertFalse(model.items())

    def test_insert_item_category_item(self):
        root = RootProjectTreeItem()
        model = ProjectItemModel(root)
        category = CategoryProjectTreeItem("category", "category description")
        model.insert_item(category)
        self.assertEqual(model.rowCount(), 1)
        self.assertEqual(model.n_items(), 0)
        category_index = model.find_category("category")
        self.assertTrue(category_index.isValid())
        self.assertEqual(category_index.row(), 0)
        self.assertEqual(category_index.column(), 0)
        self.assertEqual(model.data(category_index, Qt.ItemDataRole.DisplayRole), "category")

    def test_insert_item_leaf_item(self):
        root = RootProjectTreeItem()
        model = ProjectItemModel(root)
        category = CategoryProjectTreeItem("category", "category description")
        model.insert_item(category)
        category_index = model.find_category("category")
        mock_project_item = NonCallableMagicMock()
        mock_project_item.name = "project item"
        mock_project_item.description = "project item description"
        leaf = LeafProjectTreeItem(mock_project_item)
        model.insert_item(leaf, category_index)
        self.assertEqual(model.rowCount(), 1)
        self.assertEqual(model.rowCount(category_index), 1)
        self.assertEqual(model.n_items(), 1)
        self.assertEqual(model.items("category"), [leaf])

    def test_category_of_item(self):
        root = RootProjectTreeItem()
        category = CategoryProjectTreeItem("category", "category description")
        root.add_child(category)
        model = ProjectItemModel(root)
        self.assertEqual(model.category_of_item("nonexistent item"), None)
        project_item = ProjectItem("item", "item description", 0.0, 0.0, self.toolbox.project())
        item = LeafProjectTreeItem(project_item)
        category.add_child(item)
        found_category = model.category_of_item("item")
        self.assertEqual(found_category.name, category.name)


if __name__ == '__main__':
    unittest.main()
