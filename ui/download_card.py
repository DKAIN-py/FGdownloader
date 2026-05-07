"""
Download progress card component for displaying individual file download status.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt


class DownloadCard(QWidget):
    """A card showing a single file's download progress."""
    
    def __init__(self, filename, parent=None):
        super().__init__(parent)
        self.filename = filename
        self.init_ui()
    
    def init_ui(self):
        self.setObjectName("downloadCard")
        self.setMinimumHeight(100)
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Header: filename + status badge
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
    
    def set_status(self, status):
        """Update the status badge. Expected: 'Queued', 'Active', 'Done', 'Error'"""
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
        self.progress_bar.setObjectName("cardProgressDone")
        self.progress_bar.setValue(100)
        self.progress_bar.style().unpolish(self.progress_bar)
        self.progress_bar.style().polish(self.progress_bar)
    
    def set_error(self, error_msg):
        """Mark as error."""
        self.set_status("Error")
        self.size_label.setText(f"Error: {error_msg}")
