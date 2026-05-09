"""
Downloads progress page showing all active downloads with individual progress.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QPushButton
from PySide6.QtCore import Qt, Signal
from ui.download_card import DownloadCard


class DownloadsProgressPage(QWidget):
    """Page showing progress for all downloads with counter and pause-all controls."""
    
    pause_all_clicked = Signal()  # Emitted when pause-all button is clicked
    resume_all_clicked = Signal()  # Emitted when resume-all button is clicked
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.downloads = {}  # Maps filename -> DownloadCard
        self.all_paused = False
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Header with counter and pause-all button
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        title = QLabel("Downloads")
        title.setStyleSheet("font-size: 16px; font-weight: 700; color: #4a9eff;")
        header_layout.addWidget(title)
        
        self.counter_label = QLabel("0 / 0")
        self.counter_label.setObjectName("counterLabel")
        self.counter_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.counter_label)
        
        header_layout.addStretch()
        
        # Pause-all / Resume-all button
        self.pause_all_btn = QPushButton("⏸ Pause All")
        self.pause_all_btn.setObjectName("pauseAllBtn")
        self.pause_all_btn.setMaximumWidth(120)
        self.pause_all_btn.clicked.connect(self._on_pause_all_clicked)
        header_layout.addWidget(self.pause_all_btn)
        
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
    
    def _on_pause_all_clicked(self):
        """Handle pause-all/resume-all button click."""
        if self.all_paused:
            self.resume_all_clicked.emit()
            self.set_pause_all_state(False)
        else:
            self.pause_all_clicked.emit()
            self.set_pause_all_state(True)
    
    def set_pause_all_state(self, paused=True):
        """Update pause-all button state."""
        self.all_paused = paused
        if paused:
            self.pause_all_btn.setText("▶ Resume All")
            self.pause_all_btn.setObjectName("resumeAllBtn")
        else:
            self.pause_all_btn.setText("⏸ Pause All")
            self.pause_all_btn.setObjectName("pauseAllBtn")
        
        # Force style refresh
        self.pause_all_btn.style().unpolish(self.pause_all_btn)
        self.pause_all_btn.style().polish(self.pause_all_btn)
    
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
            if hasattr(self.downloads[filename], 'set_error'):
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
