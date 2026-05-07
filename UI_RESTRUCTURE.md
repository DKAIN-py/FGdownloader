# FitGirl Downloader - UI Restructuring Documentation

## Overview

The UI has been completely restructured from a monolithic `MainWindow` class into a **component-based architecture** with a professional dark theme and improved user experience.

---

## 📁 New File Structure

```
ui/
├── __init__.py
├── stylesheet.py           # ⭐ Centralized styling
├── components.py           # ⭐ Reusable input sections
├── file_list.py           # ⭐ File selection lists
├── download_card.py       # ⭐ Individual download progress
├── downloads_page.py      # ⭐ Downloads overview page
├── settings.py            # Settings dialog
└── window.py              # Main multi-page window
```

---

## 🎨 Key Improvements

### 1. **Centralized Styling**
- All colors, spacing, and theme definitions in `stylesheet.py`
- Single source of truth for visual consistency
- Easy to switch themes or adjust colors globally
- Professional dark theme with proper contrast

### 2. **Component-Based Architecture**
Instead of everything in `MainWindow`, we now have:

| Component | Purpose | File |
|-----------|---------|------|
| `URLInputSection` | URL input + fetch button | components.py |
| `DirectoryInputSection` | Directory picker | components.py |
| `DownloadOptionsSection` | Extract/setup checkboxes | components.py |
| `FileListGroup` | Base/optional file lists | file_list.py |
| `DownloadCard` | Single file progress card | download_card.py |
| `DownloadsProgressPage` | All downloads overview | downloads_page.py |
| `SettingsDialog` | Settings (now styled) | settings.py |
| `MainWindow` | Multi-page coordinator | window.py |

### 3. **Multi-Page Layout**
- **Page 0**: Input & Selection (clean, organized)
- **Page 1**: Download Progress (all files shown simultaneously)

```
┌─────────────────────────────────────┐
│  [Title] ⚙ Settings              │ Header
├─────────────────────────────────────┤
│                                     │
│  PAGE 0 (Input):                    │
│  ┌─────────────────────────────┐   │
│  │ URL Input [Fetch Links]     │   │
│  ├─────────────────────────────┤   │
│  │ Directory [Browse]          │   │
│  ├─────────────────────────────┤   │
│  │ Files: [Required] [Optional]│   │
│  ├─────────────────────────────┤   │
│  │ ☑ Auto-extract             │   │
│  │ ☑ Run setup.exe            │   │
│  ├─────────────────────────────┤   │
│  │ [START DOWNLOAD] ➜ PAGE 1  │   │
│  └─────────────────────────────┘   │
│                                     │
│  PAGE 1 (Progress):                 │
│  ┌────────── 5 / 7 Files ──────┐   │
│  │ Downloading...               │   │
│  │ ┌────────────────────────┐   │   │
│  │ │ file1.iso  [Active]    │   │   │
│  │ │ 250.5 MB / 500.0 MB   │   │   │
│  │ │ ████████░░ 50%        │   │   │
│  │ ├────────────────────────┤   │   │
│  │ │ file2.zip  [Queued]    │   │   │
│  │ │ 0 MB / 200.0 MB       │   │   │
│  │ │ ░░░░░░░░░░ 0%         │   │   │
│  │ └────────────────────────┘   │   │
│  └──────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

### 4. **Separate Download Progress**
**Problem Solved**: No more single progress bar switching between files
- **Before**: One progress bar, confusing when downloading multiple files asynchronously
- **After**: Individual cards for each download, plus a counter showing progress

```
Downloaded: 3 / 10 files
┌─────────────────────────┐
│ game-base.iso [Active]  │ ← Shows active downloads
│ 500 MB / 1000 MB        │
│ ████████░░ 50%          │
├─────────────────────────┤
│ audio-pack.zip [Queued] │ ← Shows queued files
│ 0 MB / 500 MB           │
│ ░░░░░░░░░░ 0%           │
├─────────────────────────┤
│ bonus-content [Done] ✓  │ ← Shows completed files
│ 300 MB / 300 MB         │
│ ██████████ 100%         │
└─────────────────────────┘
```

---

## 🚀 Component Usage

### URLInputSection
```python
url_input = URLInputSection()
url_input.fetch_btn.clicked.connect(callback)
url = url_input.get_url()
```

### DirectoryInputSection
```python
dir_input = DirectoryInputSection()
dir_input.browse_btn.clicked.connect(callback)
path = dir_input.get_directory()
dir_input.set_directory(path)
```

### FileListGroup
```python
file_list = FileListGroup("Required Files")
file_list.add_item("file.iso", {"name": "file.iso", "url": "..."}, checkable=False)
file_list.add_item("optional.zip", {...}, checkable=True)
checked = file_list.get_checked_items()
```

### DownloadCard
```python
card = DownloadCard("game-base.iso")
card.update_progress(500_000_000, 1_000_000_000)  # 500MB / 1000MB
card.set_status("Active")
card.set_completed()  # When done
```

### DownloadsProgressPage
```python
page = DownloadsProgressPage()
page.add_download("file1.iso")
page.update_progress("file1.iso", current_bytes, total_bytes)
page.mark_completed("file1.iso")
page.set_status_message("All downloads complete!")
```

---

## 🎯 Design Principles Applied

1. **Separation of Concerns**: Each component has one responsibility
2. **Reusability**: Components can be used independently
3. **Maintainability**: Changes to one component don't affect others
4. **Scalability**: Easy to add new components or features
5. **Consistency**: Centralized stylesheet ensures uniform appearance

---

## 🔄 Signal Flow

```
MainWindow.start_download()
    ↓
DownloadWorker (in QThread)
    ↓
worker.progress_update → MainWindow._on_download_progress()
    ↓
DownloadsProgressPage.update_progress()
    ↓
DownloadCard.update_progress() ← Individual cards update
```

---

## 📝 Settings Dialog

Now integrated with the global stylesheet:
- Clean layout with section labels
- Centered buttons with proper sizing
- Uses stylesheet variables for consistency

---

## 🎨 Stylesheet Features

The `DARK` stylesheet includes:
- **Base colors**: Dark background (#161616), light text (#e0e0e0)
- **Interactive elements**: Buttons, inputs with hover states
- **Status indicators**: Badge styles for Queued, Active, Done, Error
- **Progress bars**: Different colors for in-progress vs completed
- **Scroll bars**: Subtle, non-intrusive design

---

## ✅ Testing Checklist

- [x] All Python files compile without syntax errors
- [x] Window imports successfully with dependencies
- [x] Components are properly encapsulated
- [x] Multi-page switching logic implemented
- [x] Stylesheet is centralized
- [ ] Visual testing in application (needs Qt environment)
- [ ] Download progress updates correctly
- [ ] Settings dialog appears and saves

---

## 🔮 Future Enhancements

1. Add back button on download progress page
2. Download pause/resume functionality
3. Speed metrics display
4. Download history/logs
5. Drag-and-drop file support
6. Theme switcher (light/dark)

