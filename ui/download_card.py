"""
Download progress card component for displaying individual file download status.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton
from PySide6.QtCore import Qt, Signal


class DownloadCard(QWidget):
    """A card showing a single file's download progress with pause/resume controls."""
    
    pause_clicked = Signal(str)  # Emits filename when pause is clicked
    resume_clicked = Signal(str)  # Emits filename when resume is clicked
    
    def __init__(self, filename, parent=None):
        super().__init__(parent)
        self.filename = filename
        self.is_paused = False
        self.init_ui()
    
    def init_ui(self):
        self.setObjectName("downloadCard")
        self.setMinimumHeight(120)
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Header: filename + status badge + pause button
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        
        self.filename_label = QLabel(self.filename)
        self.filename_label.setObjectName("cardFilename")
        self.filename_label.setWordWrap(True)
        header_layout.addWidget(self.filename_label)
        
        self.status_badge = QLabel("Queued")
        self.status_badge.setObjectName("badgeQueued")
        self.status_badge.setMaximumWidth(60)
        self.status_badge.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.status_badge)
        
        # Pause/Resume button
        self.pause_btn = QPushButton("⏸ Pause")
        self.pause_btn.setObjectName("pauseBtn")
        self.pause_btn.setMaximumWidth(90)
        self.pause_btn.clicked.connect(self._on_pause_resume_clicked)
        header_layout.addWidget(self.pause_btn)
        
        layout.addLayout(header_layout)
        
        # File size info
        self.size_label = QLabel("0 MB / 0 MB")
        self.size_label.setObjectName("cardSizeLabel")
        layout.addWidget(self.size_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("cardProgress")
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
    
    def _on_pause_resume_clicked(self):
        """Handle pause/resume button click."""
        if self.is_paused:
            self.resume_clicked.emit(self.filename)
        else:
            self.pause_clicked.emit(self.filename)
    
    def set_paused(self, paused=True):
        """Set paused state and update button."""
        self.is_paused = paused
        if paused:
            self.pause_btn.setText("▶ Resume")
            self.pause_btn.setObjectName("resumeBtn")
            self.status_badge.setText("Paused")
            self.status_badge.setObjectName("badgePaused")
        else:
            self.pause_btn.setText("⏸ Pause")
            self.pause_btn.setObjectName("pauseBtn")
            self.status_badge.setText("Active")
            self.status_badge.setObjectName("badgeActive")
        
        # Force style refresh
        self.pause_btn.style().unpolish(self.pause_btn)
        self.pause_btn.style().polish(self.pause_btn)
        self.status_badge.style().unpolish(self.status_badge)
        self.status_badge.style().polish(self.status_badge)
    
    def set_status(self, status):
        """Update the status badge. Expected: 'Queued', 'Active', 'Paused', 'Done', 'Error'"""
        if status != "Paused":  # Don't override paused state
            self.status_badge.setText(status)
            self.status_badge.setObjectName(f"badge{status}")
            # Force style refresh
            self.status_badge.style().unpolish(self.status_badge)
            self.status_badge.style().polish(self.status_badge)
    
    def update_progress(self, current_bytes, total_bytes):
        """Update the progress bar and file size label."""
        if total_bytes > 0:
            percentage = int((current_bytes / total_bytes) * 100)
            self.progress_bar.setValue(percentage)
            
            # Convert to MB
            current_mb = current_bytes / (1024 * 1024)
            total_mb = total_bytes / (1024 * 1024)
            self.size_label.setText(f"{current_mb:.1f} MB / {total_mb:.1f} MB")
    
    def set_completed(self):
        """Mark as completed."""
        self.set_status("Done")
        self.pause_btn.setEnabled(False)
        self.progress_bar.setObjectName("cardProgressDone")
        self.progress_bar.setValue(100)
        self.progress_bar.style().unpolish(self.progress_bar)
        self.progress_bar.style().polish(self.progress_bar)
    
    def set_error(self, error_msg):
        """Mark as error."""
        self.set_status("Error")
        self.size_label.setText(f"Error: {error_msg}")
