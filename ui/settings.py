from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
from PySide6.QtCore import Qt
from ui.stylesheet import DARK


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Download Settings")
        self.resize(380, 220)
        self.setStyleSheet(DARK)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Title
        title = QLabel("Download Settings")
        title.setStyleSheet("font-size: 14px; font-weight: 700; color: #4a9eff; letter-spacing: 0.4px;")
        layout.addWidget(title)

        # Mode section
        mode_label = QLabel("Download Mode Strategy")
        mode_label.setObjectName("sectionLabel")
        layout.addWidget(mode_label)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "Auto-Detect (Default)",
            "Force Synchronous (Sync)",
            "Force Asynchronous (Async)"
        ])
        layout.addWidget(self.mode_combo)

        # Priority section
        priority_label = QLabel("Process Priority")
        priority_label.setObjectName("sectionLabel")
        layout.addWidget(priority_label)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Normal", "High"])
        layout.addWidget(self.priority_combo)

        layout.addStretch()

        # Button
        save_btn = QPushButton("Save Settings")
        save_btn.setObjectName("primaryBtn")
        save_btn.setMinimumHeight(36)
        save_btn.clicked.connect(self.accept)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def get_settings(self):
        return {
            "mode": self.mode_combo.currentText(),
            "priority": self.priority_combo.currentText()
        }