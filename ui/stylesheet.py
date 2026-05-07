"""
Global stylesheet for FitGirl Downloader.
All color/spacing decisions live here — nowhere else.
"""

DARK = """
/* ── Base ─────────────────────────────────────────── */
* {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 13px;
    color: #e0e0e0;
}
QWidget { background-color: #161616; }
QDialog { background-color: #1c1c1c; }

/* ── Header bar ───────────────────────────────────── */
#header {
    background-color: #0f0f0f;
    border-bottom: 1px solid #252525;
}
#headerTitle {
    font-size: 14px;
    font-weight: 700;
    color: #4a9eff;
    letter-spacing: 0.4px;
}
#gearBtn {
    background: transparent;
    border: none;
    color: #555;
    font-size: 17px;
    padding: 5px 8px;
    border-radius: 5px;
}
#gearBtn:hover { background: #222; color: #bbb; }

/* ── Inputs ───────────────────────────────────────── */
QLineEdit {
    background-color: #202020;
    border: 1px solid #2e2e2e;
    border-radius: 5px;
    padding: 7px 10px;
    color: #e0e0e0;
    selection-background-color: #1e4f8c;
}
QLineEdit:focus { border-color: #2e6bc4; }
QLineEdit::placeholder { color: #707070; }

/* ── Section labels ───────────────────────────────── */
#sectionLabel {
    color: #555;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.9px;
}

/* ── Buttons ──────────────────────────────────────── */
QPushButton {
    border-radius: 5px;
    padding: 7px 16px;
    font-weight: 600;
    border: none;
    outline: none;
}
#primaryBtn {
    background-color: #1a4f8c;
    color: #e8e8e8;
}
#primaryBtn:hover  { background-color: #1f5fa8; }
#primaryBtn:disabled { background-color: #1c1c1c; color: #404040; }

#secondaryBtn {
    background-color: #252525;
    color: #aaa;
    border: 1px solid #303030;
}
#secondaryBtn:hover { background-color: #2e2e2e; color: #ccc; }

#downloadBtn {
    background-color: #1a5c38;
    color: #e8e8e8;
    font-size: 13px;
    font-weight: 700;
    border-radius: 6px;
    letter-spacing: 0.3px;
}
#downloadBtn:hover    { background-color: #217044; }
#downloadBtn:disabled { background-color: #1c1c1c; color: #404040; }

#dangerBtn {
    background-color: #5c1a1a;
    color: #e88;
    border: 1px solid #6e2222;
}
#dangerBtn:hover { background-color: #6e2222; color: #faa; }

/* ── Group boxes ──────────────────────────────────── */
QGroupBox {
    border: 1px solid #252525;
    border-radius: 7px;
    margin-top: 10px;
    padding-top: 6px;
    font-weight: 700;
    color: #505050;
    font-size: 11px;
    letter-spacing: 0.6px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 5px;
}

/* ── List widgets ─────────────────────────────────── */
QListWidget {
    background-color: #1c1c1c;
    border: none;
    border-radius: 5px;
    padding: 4px;
    outline: none;
}
QListWidget::item {
    padding: 5px 8px;
    border-radius: 4px;
    color: #c0c0c0;
}
QListWidget::item:alternate { background-color: #202020; }
QListWidget::item:hover { background-color: #242424; }

/* ── Checkboxes ───────────────────────────────────── */
QCheckBox { spacing: 8px; color: #aaa; }
QCheckBox::indicator {
    width: 15px;
    height: 15px;
    border: 2px solid #383838;
    border-radius: 3px;
    background: #1e1e1e;
}
QCheckBox::indicator:checked {
    background-color: #1a4f8c;
    border-color: #2e6bc4;
    image: none;
}
QCheckBox::indicator:hover { border-color: #2e6bc4; }

/* ── Combo box ────────────────────────────────────── */
QComboBox {
    background: #202020;
    border: 1px solid #2e2e2e;
    border-radius: 5px;
    padding: 6px 10px;
    color: #e0e0e0;
    min-height: 20px;
}
QComboBox:hover { border-color: #383838; }
QComboBox::drop-down {
    border: none;
    width: 22px;
    subcontrol-position: right center;
}
QComboBox::down-arrow { color: #555; }
QComboBox QAbstractItemView {
    background: #202020;
    border: 1px solid #2e2e2e;
    border-radius: 4px;
    selection-background-color: #1a4f8c;
    outline: none;
    padding: 4px;
}

/* ── Download cards ───────────────────────────────── */
#downloadCard {
    background-color: #1c1c1c;
    border: 1px solid #252525;
    border-radius: 7px;
}

#cardFilename {
    color: #d8d8d8;
    font-weight: 600;
    font-size: 12px;
}
#cardSizeLabel {
    color: #484848;
    font-size: 11px;
}

#cardProgress {
    background-color: #252525;
    border: none;
    border-radius: 3px;
}
#cardProgress::chunk {
    background-color: #2e6bc4;
    border-radius: 3px;
}
#cardProgressDone::chunk {
    background-color: #28a85a;
    border-radius: 3px;
}

/* ── Status badges ────────────────────────────────── */
#badgeQueued {
    background: #1e1e1e;
    color: #484848;
    border: 1px solid #2a2a2a;
    border-radius: 4px;
    padding: 2px 0px;
    font-size: 11px;
    font-weight: 600;
}
#badgeActive {
    background: #0e2340;
    color: #4a9eff;
    border: 1px solid #1a3a6a;
    border-radius: 4px;
    padding: 2px 0px;
    font-size: 11px;
    font-weight: 600;
}
#badgeDone {
    background: #0e2a1a;
    color: #3dc878;
    border: 1px solid #1a4a2a;
    border-radius: 4px;
    padding: 2px 0px;
    font-size: 11px;
    font-weight: 600;
}
#badgeError {
    background: #2a0e0e;
    color: #e05555;
    border: 1px solid #4a1a1a;
    border-radius: 4px;
    padding: 2px 0px;
    font-size: 11px;
    font-weight: 600;
}

/* ── Counter label ────────────────────────────────── */
#counterLabel {
    font-size: 14px;
    font-weight: 700;
    color: #d0d0d0;
}
#counterSub {
    font-size: 11px;
    color: #484848;
}

/* ── Scroll bars ──────────────────────────────────── */
QScrollArea  { border: none; background: transparent; }
QScrollBar:vertical {
    background: transparent;
    width: 7px;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background: #2e2e2e;
    border-radius: 3px;
    min-height: 28px;
}
QScrollBar::handle:vertical:hover { background: #404040; }
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical { background: none; }

/* ── Tooltip ──────────────────────────────────────── */
QToolTip {
    background: #202020;
    border: 1px solid #303030;
    color: #ccc;
    padding: 4px 8px;
    border-radius: 4px;
}
"""
