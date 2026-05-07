# Quick Reference - UI Components

## Component Overview & Usage

### 1. URLInputSection
**File**: `ui/components.py`
**Purpose**: URL input field with fetch button

```python
from ui.components import URLInputSection

url_input = URLInputSection()
url_input.fetch_btn.clicked.connect(lambda: fetch_url(url_input.get_url()))
```

**Methods**:
- `get_url()` → str: Returns trimmed URL
- `clear()`: Clears the input field
- `fetch_btn`: QPushButton for fetching

---

### 2. DirectoryInputSection
**File**: `ui/components.py`
**Purpose**: Directory picker with browse button

```python
dir_input = DirectoryInputSection()
dir_input.browse_btn.clicked.connect(browse_callback)
path = dir_input.get_directory()
dir_input.set_directory("/path/to/dir")
```

**Methods**:
- `get_directory()` → str: Returns selected path
- `set_directory(path)`: Sets the displayed path
- `browse_btn`: QPushButton for browsing

---

### 3. DownloadOptionsSection
**File**: `ui/components.py`
**Purpose**: Checkboxes for download options

```python
options = DownloadOptionsSection()
opts = options.get_options()
# opts = {"extract": True, "setup": False}
```

**Methods**:
- `get_options()` → dict: Returns {"extract": bool, "setup": bool}

---

### 4. FileListGroup
**File**: `ui/file_list.py`
**Purpose**: Organized list of files (base or optional)

```python
file_list = FileListGroup("Optional Files")

# Add non-checkable items (required files)
file_list.add_item("base-game.iso", {"url": "..."})

# Add checkable items (optional)
file_list.add_item("bonus-pack.zip", {"url": "..."}, checkable=True)

# Get checked items
checked = file_list.get_checked_items()
# [{"name": "bonus-pack.zip", "data": {"url": "..."}}]

# Get all items
all_items = file_list.get_all_items()

# Clear
file_list.clear()
```

**Methods**:
- `add_item(name, data=None, checkable=False)`: Add item to list
- `clear()`: Remove all items
- `get_checked_items()` → list: Returns only checked items
- `get_all_items()` → list: Returns all items
- `get_items_text()` → list: Returns item names only

---

### 5. DownloadCard
**File**: `ui/download_card.py`
**Purpose**: Individual file download progress display

```python
card = DownloadCard("game-base.iso")
card.update_progress(500_000_000, 1_000_000_000)  # 500MB / 1000MB
card.set_status("Active")  # "Queued", "Active", "Done", "Error"
card.set_completed()
card.set_error("Network timeout")
```

**Methods**:
- `update_progress(current_bytes, total_bytes)`: Update progress
- `set_status(status)`: Set status (updates badge color)
- `set_completed()`: Mark as done with green progress bar
- `set_error(msg)`: Mark as error

**Status Colors**:
- **Queued**: Gray
- **Active**: Blue
- **Done**: Green
- **Error**: Red

---

### 6. DownloadsProgressPage
**File**: `ui/downloads_page.py`
**Purpose**: Main downloads view with counter

```python
page = DownloadsProgressPage()

# Add downloads
page.add_download("file1.iso")
page.add_download("file2.zip")

# Update progress for a file
page.update_progress("file1.iso", current_bytes, total_bytes)

# Mark completed
page.mark_completed("file1.iso")

# Mark error
page.mark_error("file2.zip", "Connection lost")

# Update status message
page.set_status_message("Downloading at 10 MB/s...")

# Clear all
page.clear_all()
```

**Features**:
- Auto-updating counter (e.g., "3 / 7")
- Individual progress cards per file
- Status message display
- Scrollable area for many downloads

---

## Complete Flow Example

```python
from ui.window import MainWindow
from PySide6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

The MainWindow handles:
1. Creating both pages (input & progress)
2. Managing page transitions
3. Coordinating component interactions
4. Starting downloads with DownloadWorker
5. Updating progress via signals

---

## Signal Connections

```python
# Fetch signals
fetch_btn.clicked.connect(window.start_fetching)
fetch_thread.finished.connect(window.on_fetch_finished)
fetch_thread.error.connect(window.on_fetch_error)

# Download signals
download_btn.clicked.connect(window.start_download)
download_thread.started.connect(worker.start)
worker.progress_update.connect(window._on_download_progress)
worker.status_update.connect(window._on_status_update)
worker.download_finished.connect(window._on_download_finished)
```

---

## Stylesheet Usage

All components automatically use the stylesheet from `ui.stylesheet.DARK`.

To apply custom object names for styling:

```python
button = QPushButton("Download")
button.setObjectName("downloadBtn")  # Uses #downloadBtn CSS

label = QLabel("Status")
label.setObjectName("sectionLabel")  # Uses #sectionLabel CSS
```

**Available object names**:
- `#primaryBtn`, `#secondaryBtn`, `#downloadBtn`, `#dangerBtn`
- `#sectionLabel`
- `#downloadCard`, `#cardFilename`, `#cardProgress`
- `#badgeQueued`, `#badgeActive`, `#badgeDone`, `#badgeError`
- `#counterLabel`, `#counterSub`
- `#header`, `#headerTitle`, `#gearBtn`

