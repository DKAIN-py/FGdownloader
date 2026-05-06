from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QCheckBox, QMessageBox,
    QListWidget, QAbstractItemView, QListWidgetItem,
    QGroupBox, QGridLayout, QFileDialog, QDialog
)

from PySide6.QtCore import Qt
from core.parser import FetchThread
from core.downloader import DownloadWorker, check_internet_speed_mbps
from ui.settings import SettingsDialog

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.current_settings = {
            "mode": "Auto-Detect (Default)",
            "priority": "Normal"
        }
        self.initUI()

    def initUI(self):
        self.setWindowTitle("FitGirl Direct Downloader")
        self.resize(700, 650)

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

        # Row 1.2: Directory Selector
        self.dir_label = QLabel("<b>Download Directory:</b>")
        layout.addWidget(self.dir_label)

        dir_layout = QHBoxLayout()
        self.dir_entry = QLineEdit()
        self.dir_entry.setPlaceholderText("Select where to save files...")
        dir_layout.addWidget(self.dir_entry)

        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d; 
                color: white; 
                padding: 6px 10px; 
                border-radius: 4px; 
            }
            QPushButton:hover { background-color: #5a6268; }
        """)
        self.browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(self.browse_btn)
        layout.addLayout(dir_layout)

        # Settings Button Row
        self.settings_btn = QPushButton("⚙ Network & Download Settings")
        self.settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #495057;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #343a40; }
        """)
        self.settings_btn.clicked.connect(self.open_settings)
        layout.addWidget(self.settings_btn)

        # Row 2: Split Lists using separate Group Boxes
        grid_layout = QGridLayout()

        # Required Files Group
        base_group = QGroupBox("Required Base Files (Always Included)")
        base_layout = QVBoxLayout()
        self.base_list = QListWidget()
        self.base_list.setSelectionMode(QAbstractItemView.NoSelection)
        base_layout.addWidget(self.base_list)
        base_group.setLayout(base_layout)
        grid_layout.addWidget(base_group, 0, 0)

        # Optional Files Group
        optional_group = QGroupBox("Optional / Selective Files")
        optional_layout = QVBoxLayout()
        self.optional_list = QListWidget()
        self.optional_list.setSelectionMode(QAbstractItemView.NoSelection)
        optional_layout.addWidget(self.optional_list)
        optional_group.setLayout(optional_layout)
        grid_layout.addWidget(optional_group, 0, 1)

        layout.addLayout(grid_layout)

        # Row 3: Options
        options_frame = QHBoxLayout()
        self.chk_extract = QCheckBox("Auto-extract after download")
        self.chk_extract.setChecked(True)
        options_frame.addWidget(self.chk_extract)

        self.chk_setup = QCheckBox("Run setup.exe after completion")
        options_frame.addWidget(self.chk_setup)
        layout.addLayout(options_frame)

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

    def browse_directory(self):
        """Opens a folder selector dialog"""
        directory = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        if directory:
            self.dir_entry.setText(directory)
            return directory

    def open_settings(self):
        """Opens the Settings dialog and saves values to main memory."""
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.current_settings = dialog.get_settings()
            QMessageBox.information(self, "Settings Saved", f"Strategy: {self.current_settings['mode']}")

    def start_fetching(self):
        url = self.url_entry.text().strip()
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a FitGirl URL.")
            return

        self.fetch_btn.setEnabled(False)
        self.base_list.clear()
        self.optional_list.clear()
        
        # Show placeholder text in required box while loading
        self.base_list.addItem("Fetching links, please wait...")

        self.thread = FetchThread(url)
        self.thread.finished.connect(self.on_fetch_finished)
        self.thread.error.connect(self.on_fetch_error)
        self.thread.start()

    def on_fetch_finished(self, data):
        self.fetched_data = data
        self.fetch_btn.setEnabled(True)
        self.base_list.clear()
        self.optional_list.clear()

        # Add base items (Always included, no checkboxes needed)
        for item in data['base']:
            item_widget = QListWidgetItem(item['name'])
            # Do not make it checkable; it's always included
            self.base_list.addItem(item_widget)

        # Add optional items with checkbox support
        for item in data['optional']:
            item_widget = QListWidgetItem(item['name'])
            item_widget.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item_widget.setCheckState(Qt.Unchecked) # Unchecked by default
            self.optional_list.addItem(item_widget)

    def on_fetch_error(self, message):
        self.fetch_btn.setEnabled(True)
        self.base_list.clear()
        self.optional_list.clear()
        QMessageBox.critical(self, "Error", message)

    def start_download(self):
        # 0. Check if save directory is provided
        save_dir = self.dir_entry.text().strip()
        if not save_dir:
            QMessageBox.warning(self, "Path Error", "Please select a download directory first.")
            return

        selected_links = []

        # 1. Base files are always selected
        selected_links.extend(self.fetched_data['base'])

        # 2. Add optional items if checked
        for index in range(self.optional_list.count()):
            item = self.optional_list.item(index)
            if item.checkState() == Qt.Checked:
                name = item.text()
                match = next((x for x in self.fetched_data['optional'] if x['name'] == name), None)
                if match:
                    selected_links.append(match)

        if not selected_links:
            QMessageBox.warning(self, "Warning", "No files selected to download.")
            return

        # 3. Read from dynamically updated self.current_settings
        strategy_mode = self.current_settings.get("mode", "Auto-Detect (Default)")
        priority_class = self.current_settings.get("priority", "Normal")

        detected_speed = 30.0  # Default fallback speed

        print(strategy_mode, priority_class)
        if strategy_mode == "Force Synchronous (Sync)":
            use_async = False
        elif strategy_mode == "Force Asynchronous (Async)":
            use_async = True
        else:
            # Auto-Detect mode: run our network speed function
            detected_speed = check_internet_speed_mbps()
            use_async = detected_speed > 25

        extract_after = self.chk_extract.isChecked()
        setup_after = self.chk_setup.isChecked()

        # 4. Initialize Worker with these evaluated parameters
        self.worker = DownloadWorker(
            links=selected_links,
            download_dir=save_dir,
            internet_speed_mbps=detected_speed,
            priority=priority_class, # Added priority to worker parameters
            use_async=use_async
        )

        self.worker.start()

        QMessageBox.information(
            self, 
            "Download Initialized", 
            f"Saving to: {save_dir}\n"
            f"Mode: {'Async' if use_async else 'Sync'}\n"
            f"Priority: {priority_class}\n\n"
            f"Items to process: {len(selected_links)}"
        )

        


