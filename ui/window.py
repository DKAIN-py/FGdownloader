"""
Main application window with multi-page layout.
Page 1: Input & Selection
Page 2: Download Progress
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QPushButton,
    QFileDialog, QMessageBox, QScrollArea
)
from PySide6.QtCore import Qt, QThread

from pathlib import Path

from core.parser import FetchThread
from core.downloader import DownloadWorker, check_internet_speed_mbps
from core.extractor import ExtractWorker
from ui.stylesheet import DARK
from ui.components import URLInputSection, DirectoryInputSection, DownloadOptionsSection
from ui.file_list import FileListGroup
from ui.settings import SettingsDialog
from ui.downloads_page import DownloadsProgressPage
from config import DETECTION_SPEED

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.current_settings = {
            "mode": "Auto-Detect (Default)",
            "priority": "Normal"
        }
        self.fetched_data = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("FitGirl Direct Downloader")
        self.resize(900, 700)
        self.setStyleSheet(DARK)
        
        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header bar
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Stacked widget for pages
        self.pages = QStackedWidget()
        self.page_input = self._create_input_page()
        self.page_downloads = DownloadsProgressPage()
        
        self.pages.addWidget(self.page_input)      # Page 0
        self.pages.addWidget(self.page_downloads)  # Page 1
        self.pages.setCurrentIndex(0)
        
        main_layout.addWidget(self.pages)
        self.setLayout(main_layout)
    
    def _create_header(self):
        """Create the header bar with title and settings button."""
        header = QWidget()
        header.setObjectName("header")
        header.setMaximumHeight(50)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)
        
        title = QLabel("FitGirl Downloader")
        title.setObjectName("headerTitle")
        layout.addWidget(title)
        
        layout.addStretch()
        
        settings_btn = QPushButton("⚙")
        settings_btn.setObjectName("gearBtn")
        settings_btn.setMaximumWidth(40)
        settings_btn.clicked.connect(self.open_settings)
        layout.addWidget(settings_btn)
        
        header.setLayout(layout)
        return header
    
    def _create_input_page(self):
        """Create the input/selection page."""
        page = QWidget()
        
        # Use scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(16)
        
        # URL Input
        self.url_input = URLInputSection()
        self.url_input.fetch_btn.clicked.connect(self.start_fetching)
        content_layout.addWidget(self.url_input)
        
        # Directory Input
        self.dir_input = DirectoryInputSection()
        self.dir_input.browse_btn.clicked.connect(self.browse_directory)
        content_layout.addWidget(self.dir_input)
        
        # File Lists
        files_layout = QHBoxLayout()
        files_layout.setSpacing(16)
        
        self.base_list = FileListGroup("Required Files (Always Included)")
        self.optional_list = FileListGroup("Optional / Selective Files")
        
        files_layout.addWidget(self.base_list)
        files_layout.addWidget(self.optional_list)
        
        content_layout.addLayout(files_layout)
        
        # Download Options
        self.options = DownloadOptionsSection()
        content_layout.addWidget(self.options)
        
        content_layout.addStretch()
        
        # Download button
        download_btn = QPushButton("Start Download")
        download_btn.setObjectName("downloadBtn")
        download_btn.setMinimumHeight(44)
        download_btn.setStyleSheet("""
            #downloadBtn {
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }
        """)
        download_btn.clicked.connect(self.start_download)
        content_layout.addWidget(download_btn)
        
        content.setLayout(content_layout)
        scroll.setWidget(content)
        
        page_layout = QVBoxLayout()
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)
        page.setLayout(page_layout)
        
        return page
    
    def browse_directory(self):
        """Open folder selector dialog."""
        directory = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        if directory:
            self.dir_input.set_directory(directory)
    
    def open_settings(self):
        """Open the Settings dialog."""
        dialog = SettingsDialog(self)
        if dialog.exec() == 1:  # QDialog.Accepted
            self.current_settings = dialog.get_settings()
    
    def start_fetching(self):
        """Fetch download links from URL."""
        url = self.url_input.get_url()
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a FitGirl URL.")
            return
        
        self.url_input.fetch_btn.setEnabled(False)
        self.base_list.clear()
        self.optional_list.clear()
        self.base_list.add_item("Fetching links, please wait...")
        
        self.fetch_thread = FetchThread(url)
        self.fetch_thread.finished.connect(self.on_fetch_finished)
        self.fetch_thread.error.connect(self.on_fetch_error)
        self.fetch_thread.start()
    
    def on_fetch_finished(self, data):
        """Handle successful fetch."""
        self.fetched_data = data
        self.url_input.fetch_btn.setEnabled(True)
        self.base_list.clear()
        self.optional_list.clear()
        
        # Add base items
        for item in data['base']:
            self.base_list.add_item(item['name'], item)
        
        # Add optional items with checkboxes
        for item in data['optional']:
            self.optional_list.add_item(item['name'], item, checkable=True)
    
    def on_fetch_error(self, message):
        """Handle fetch error."""
        self.url_input.fetch_btn.setEnabled(True)
        self.base_list.clear()
        self.optional_list.clear()
        QMessageBox.critical(self, "Error", message)
    
    def start_download(self):
        """Initialize and start downloads."""
        # Validate
        save_dir = self.dir_input.get_directory()
        if not save_dir:
            QMessageBox.warning(self, "Path Error", "Please select a download directory first.")
            return
        
        if not self.fetched_data:
            QMessageBox.warning(self, "Warning", "Please fetch links first.")
            return
        
        # Build selected links list
        selected_links = list(self.fetched_data['base'])  # Always include base files
        selected_links.extend(self.optional_list.get_checked_items())
        
        if not selected_links:
            QMessageBox.warning(self, "Warning", "No files selected to download.")
            return
        
        # Determine async mode
        strategy_mode = self.current_settings.get("mode", "Auto-Detect (Default)")
        priority_class = self.current_settings.get("priority", "Normal")
        detected_speed = 30.0
        
        if strategy_mode == "Force Synchronous (Sync)":
            use_async = False
        elif strategy_mode == "Force Asynchronous (Async)":
            use_async = True
        else:
            detected_speed = check_internet_speed_mbps()
            use_async = detected_speed > DETECTION_SPEED
        
        # Get execution options (extract, setup)
        opts = self.options.get_options()
        
        # Switch stack index to download page dashboard
        self.pages.setCurrentIndex(1)
        
        # Initialize worker
        self.worker = DownloadWorker(
            links=selected_links,
            download_dir=save_dir,
            internet_speed_mbps=detected_speed,
            priority=priority_class,
            use_async=use_async
        )
        
        self.download_thread = QThread()
        self.worker.moveToThread(self.download_thread)
        
        # Connect signals for core runtime tracking
        self.download_thread.started.connect(self.worker.start)
        self.worker.progress_update.connect(self._on_download_progress)
        self.worker.status_update.connect(self._on_status_update)
        self.worker.paused.connect(self._on_file_paused)
        self.worker.resumed.connect(self._on_file_resumed)
        
        # PIPELINE LINK: Intercept finished slot to run extraction/setup choices via lambda
        self.worker.download_finished.connect(lambda: self._on_download_finished(opts))
        
        # Thread lifetime cleanup rules
        self.worker.download_finished.connect(self.download_thread.quit)
        self.worker.download_finished.connect(self.worker.deleteLater)
        self.download_thread.finished.connect(self.download_thread.deleteLater)
        
        # Add tracking cards to the download page
        for link in selected_links:
            self.page_downloads.add_download(link['name'])
        
        # Connect individual row layout tracking card buttons
        # The fname=filename default argument prevents the closure bug inside loops!
        for filename, card in self.page_downloads.downloads.items():
            card.pause_clicked.connect(lambda fname=filename: self.worker.pause_file(fname))
            card.resume_clicked.connect(lambda fname=filename: self.worker.resume_file(fname))
        
        # Connect global control dashboard action signals
        self.page_downloads.pause_all_clicked.connect(
            self.worker.pause_all, Qt.ConnectionType.DirectConnection
        )
        self.page_downloads.resume_all_clicked.connect(
            self.worker.resume_all, Qt.ConnectionType.DirectConnection
        )
        
        # Fire background execution loop thread
        self.download_thread.start()
    
    def _on_download_progress(self, filename, current, total):
        """Handle download progress update."""
        self.page_downloads.update_progress(filename, current, total)
    
    def _on_status_update(self, message):
        """Handle status update."""
        self.page_downloads.set_status_message(message)
    
    def _on_file_paused(self, filename):
        """Handle file pause."""
        if filename in self.page_downloads.downloads:
            self.page_downloads.downloads[filename].set_paused(True)
    
    def _on_file_resumed(self, filename):
        """Handle file resume."""
        if filename in self.page_downloads.downloads:
            self.page_downloads.downloads[filename].set_paused(False)
    
    def _on_download_finished(self, opts):
        """Fires when downloading is complete and handles downstream options."""
        self._on_status_update("All downloads completed successfully!")
        
        base_dir = Path(self.dir_input.get_directory().strip())
        
        # 1. Handle Automatic Extraction
        if opts["extract"]:
            # Find the first .rar volume part
            first_part = None
            for item in self.fetched_data['base']:
                name = item['name']
                if ".part1.rar" in name or ".part01.rar" in name or (name.endswith(".rar") and ".part" not in name):
                    first_part = name
                    break
            
            if first_part:
                full_archive_path = base_dir / first_part
                extract_destination = base_dir / "Extracted_Game"
                
                self._on_status_update("Preparing automated extraction...")
                self.run_extraction_pipeline(full_archive_path, extract_destination, opts["setup"])
                return  # Exit here; extraction routine will take over launching setup.exe
            else:
                QMessageBox.warning(self, "Extraction Error", "Could not locate the main .part1.rar archive volume.")

       
        
    def run_extraction_pipeline(self, archive_path, destination_path, launch_setup_after):
        """Spins up the extraction worker in a separate background thread."""
        
        self.extractor_worker = ExtractWorker(archive_path, destination_path, "GameInstaller")
        self.extractor_thread = QThread()
        self.extractor_worker.moveToThread(self.extractor_thread)
        
        self.extractor_thread.started.connect(self.extractor_worker.start_extraction)
        
        # Update progress label or bar with extraction percentages
        self.extractor_worker.progress_update.connect(
            lambda msg, percent: self._on_status_update(f"{msg} ({percent}%)")
        )
        
        # Cleanup and chaining triggers
        self.extractor_worker.extraction_finished.connect(self.extractor_thread.quit)
        self.extractor_worker.extraction_finished.connect(self.extractor_worker.deleteLater)
        self.extractor_thread.finished.connect(self.extractor_thread.deleteLater)
        
        # If setup is true, hook it up to run immediately when extraction finishes
        if launch_setup_after:
            self.extractor_worker.extraction_finished.connect(
                lambda: self.launch_setup_installer(destination_path)
            )
        else:
            self.extractor_worker.extraction_finished.connect(
                lambda: QMessageBox.information(self, "Done", "Extraction finished successfully!")
            )
            
        self.extractor_thread.start()

        


