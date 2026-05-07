"""
Downloads progress page showing all active downloads with individual progress.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QScrollBar
from PySide6.QtCore import Qt
from ui.download_card import DownloadCard


class DownloadsProgressPage(QWidget):
    """Page showing progress for all downloads with counter."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.downloads = {}  # Maps filename -> DownloadCard
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Header with counter
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        title = QLabel("Downloads")
        title.setStyleSheet("font-size: 16px; font-weight: 700; color: #4a9eff;")
        header_layout.addWidget(title)
        
        self.counter_label = QLabel("0 / 0")
        self.counter_label.setObjectName("counterLabel")
        self.counter_label.setAlignment(Qt.AlignRight)
        header_layout.addWidget(self.counter_label)
        
        layout.addLayout(header_layout)
        
        # Status subtitle
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("counterSub")
        layout.addWidget(self.status_label)
        
        # Scroll area for download cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        # Container for cards
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout()
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(12)
        self.cards_layout.setAlignment(Qt.AlignTop)
        self.cards_container.setLayout(self.cards_layout)
        
        scroll_area.setWidget(self.cards_container)
        layout.addWidget(scroll_area)
        
        self.setLayout(layout)
    
    def add_download(self, filename):
        """Add a new download card."""
        card = DownloadCard(filename)
        self.downloads[filename] = card
        self.cards_layout.addWidget(card)
        self._update_counter()
    
    def update_progress(self, filename, current_bytes, total_bytes):
        """Update progress for a specific download."""
        if filename in self.downloads:
            self.downloads[filename].update_progress(current_bytes, total_bytes)
            self.downloads[filename].set_status("Active")
    
    def mark_completed(self, filename):
        """Mark a download as completed."""
        if filename in self.downloads:
            self.downloads[filename].set_completed()
            self._update_counter()
    
    def mark_error(self, filename, error_msg):
        """Mark a download as failed."""
        if filename in self.downloads:
            self.downloads[filename].set_error(error_msg)
            self._update_counter()
    
    def set_status_message(self, message):
        """Update the status subtitle."""
        self.status_label.setText(message)
    
    def _update_counter(self):
        """Update the counter showing completed/total."""
        total = len(self.downloads)
        completed = sum(
            1 for card in self.downloads.values()
            if card.status_badge.text() == "Done"
        )
        self.counter_label.setText(f"{completed} / {total}")
    
    def clear_all(self):
        """Clear all downloads."""
        for card in self.downloads.values():
            card.deleteLater()
        self.downloads.clear()
        self._update_counter()
