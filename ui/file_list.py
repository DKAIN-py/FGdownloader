"""
File list components for displaying base and optional files.
"""

from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QListWidget, QAbstractItemView, QListWidgetItem
from PySide6.QtCore import Qt


class FileListGroup(QGroupBox):
    """A group box containing a list of files with checkboxes (optional)."""
    
    def __init__(self, title, allow_selection=False, parent=None):
        super().__init__(title, parent)
        self.allow_selection = allow_selection
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setMinimumHeight(400)
        
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
    
    def add_item(self, name, data=None, checkable=False):
        """Add an item to the list."""
        item = QListWidgetItem(name)
        if checkable:
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.Unchecked)
        
        if data:
            item.setData(Qt.UserRole, data)
        
        self.list_widget.addItem(item)
    
    def clear(self):
        """Clear all items."""
        self.list_widget.clear()
    
    def get_checked_items(self):
        """Get all checked items (only for checkable lists)."""
        items = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.checkState() == Qt.Checked:
                items.append({
                    "name": item.text(),
                    "data": item.data(Qt.UserRole)
                })
        return items
    
    def get_all_items(self):
        """Get all items regardless of check state."""
        items = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            items.append({
                "name": item.text(),
                "data": item.data(Qt.UserRole)
            })
        return items
    
    def get_items_text(self):
        """Get text of all items."""
        items = []
        for i in range(self.list_widget.count()):
            items.append(self.list_widget.item(i).text())
        return items
