from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QCheckBox, QTextEdit, QMessageBox
)

from core.parser import FetchThread

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("FitGirl Direct Downloader")
        self.resize(650, 550)

        layout = QVBoxLayout()

        # Row 1: URL Entry
        self.url_label = QLabel("<b>FitGirl Webpage URL:</b>")
        layout.addWidget(self.url_label)

        url_layout = QHBoxLayout()
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Paste FitGirl game URL here...")
        url_layout.addWidget(self.url_entry)

        self.fetch_btn = QPushButton("Fetch Links")
        self.fetch_btn.setStyleSheet("""
            QPushButton {
                background-color: #1f538d; 
                color: white; 
                padding: 6px 12px; 
                border-radius: 4px; 
                font-weight: bold;
            }
            QPushButton:hover { background-color: #14375e; }
        """)
        self.fetch_btn.clicked.connect(self.start_fetching)
        url_layout.addWidget(self.fetch_btn)
        layout.addLayout(url_layout)

        # Row 2: File Display
        self.file_label = QLabel("<b>Available Files:</b>")
        layout.addWidget(self.file_label)

        self.file_box = QTextEdit()
        self.file_box.setReadOnly(True)
        self.file_box.setPlaceholderText("Link results will appear here after fetching...")
        layout.addWidget(self.file_box)

        # Row 3: Checkboxes & Options
        self.chk_extract = QCheckBox("Auto-extract after download")
        self.chk_extract.setChecked(True)
        layout.addWidget(self.chk_extract)

        self.chk_setup = QCheckBox("Run setup.exe after completion")
        layout.addWidget(self.chk_setup)

        # Row 4: Action Button
        self.download_btn = QPushButton("Start Download")
        self.download_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745; 
                color: white; 
                padding: 10px; 
                font-size: 13px; 
                font-weight: bold; 
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #218838; }
        """)
        self.download_btn.clicked.connect(self.start_download)
        layout.addWidget(self.download_btn)

        self.setLayout(layout)

    def start_fetching(self):
        url = self.url_entry.text().strip()
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a FitGirl URL.")
            return

        # Disable button while fetching
        self.fetch_btn.setEnabled(False)
        self.file_box.setText("Fetching links, please wait...")

        # Start thread
        self.thread = FetchThread(url)
        self.thread.finished.connect(self.on_fetch_finished)
        self.thread.error.connect(self.on_fetch_error)
        self.thread.start()

    def on_fetch_finished(self, data):
        self.fetched_data = data
        self.fetch_btn.setEnabled(True)
        
        # Clear box and update view
        self.file_box.clear()
        
        output_text = "--- Base Files ---\n"
        for idx, item in enumerate(data['base'], 1):
            output_text += f"{idx:02d}. {item['name']}\n"
            
        if data['optional']:
            output_text += "\n--- Optional/Selective Files ---\n"
            for idx, item in enumerate(data['optional'], 1):
                output_text += f"{idx:02d}. {item['name']}\n"
                
        self.file_box.setPlainText(output_text)

    def on_fetch_error(self, message):
        self.fetch_btn.setEnabled(True)
        self.file_box.setText("Failed to fetch links.")
        QMessageBox.critical(self, "Error", message)

    def start_download(self):
        if not self.fetched_data['base']:
            QMessageBox.warning(self, "Warning", "No links to download. Please fetch a URL first.")
            return
        
        total_items = len(self.fetched_data['base'])
        extract_after = self.chk_extract.isChecked()
        setup_after = self.chk_setup.isChecked()
        
        # We will add the background downloader module here next!
        QMessageBox.information(
            self, 
            "Download Initialized", 
            f"Downloading {total_items} base files.\nExtract files: {extract_after}\nRun setup: {setup_after}"
        )


