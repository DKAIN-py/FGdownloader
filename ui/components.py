"""
Individual reusable UI components for FitGirl Downloader.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox
)
from PySide6.QtCore import Qt


class URLInputSection(QWidget):
    """URL input section with label and button."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Label
        label = QLabel("FitGirl Webpage URL")
        label.setObjectName("sectionLabel")
        layout.addWidget(label)
        
        # Input row
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)
        
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Paste FitGirl game URL here...")
        input_layout.addWidget(self.url_entry)
        
        self.fetch_btn = QPushButton("Fetch Links")
        self.fetch_btn.setObjectName("primaryBtn")
        self.fetch_btn.setMaximumWidth(120)
        input_layout.addWidget(self.fetch_btn)
        
        layout.addLayout(input_layout)
        self.setLayout(layout)
    
    def get_url(self):
        return self.url_entry.text().strip()
    
    def clear(self):
        self.url_entry.clear()


class DirectoryInputSection(QWidget):
    """Directory selection section with label and browse button."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Label
        label = QLabel("Download Directory")
        label.setObjectName("sectionLabel")
        layout.addWidget(label)
        
        # Input row
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)
        
        self.dir_entry = QLineEdit()
        self.dir_entry.setPlaceholderText("Select where to save files...")
        self.dir_entry.setReadOnly(True)
        input_layout.addWidget(self.dir_entry)
        
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setObjectName("secondaryBtn")
        self.browse_btn.setMaximumWidth(100)
        input_layout.addWidget(self.browse_btn)
        
        layout.addLayout(input_layout)
        self.setLayout(layout)
    
    def get_directory(self):
        return self.dir_entry.text().strip()
    
    def set_directory(self, path):
        self.dir_entry.setText(path)


class DownloadOptionsSection(QWidget):
    """Checkboxes for download options."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Label
        label = QLabel("Options")
        label.setObjectName("sectionLabel")
        layout.addWidget(label)
        
        # Options
        options_layout = QVBoxLayout()
        options_layout.setSpacing(6)
        
        self.chk_extract = QCheckBox("Auto-extract after download")
        self.chk_extract.setChecked(True)
        options_layout.addWidget(self.chk_extract)
        
        self.chk_setup = QCheckBox("Run setup.exe after completion")
        options_layout.addWidget(self.chk_setup)
        
        layout.addLayout(options_layout)
        self.setLayout(layout)
    
    def get_options(self):
        return {
            "extract": self.chk_extract.isChecked(),
            "setup": self.chk_setup.isChecked()
        }
