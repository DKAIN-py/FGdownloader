from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Download Settings")
        self.resize(300, 180)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("<b>Download Mode Strategy:</b>"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Auto-Detect (Default)", "Force Synchronous (Sync)", "Force Asynchronous (Async)"])
        layout.addWidget(self.mode_combo)

        layout.addWidget(QLabel("Process Priority:"))
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Normal", "High"])
        layout.addWidget(self.priority_combo)

        save_btn = QPushButton("Save Settings")
        save_btn.setStyleSheet("background-color: #1f538d; color: white; font-weight: bold; border-radius: 4px; padding: 6px;")
        save_btn.clicked.connect(self.accept)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def get_settings(self):
        return {
            "mode": self.mode_combo.currentText(),
            "priority": self.priority_combo.currentText()
        }