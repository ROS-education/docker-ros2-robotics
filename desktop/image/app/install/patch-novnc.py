#!/usr/bin/env python3
"""
Patch noVNC to ensure immediate resizing and proper 1080p fallback
"""
import sys

def patch_ui():
    path = '/usr/share/novnc/app/ui.js'
    try:
        with open(path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Skipping ui.js patch: {e}")
        return

    # 1. Listen to 'input' event in addition to 'change' so options trigger immediately upon selection
    t1 = "settingElem.addEventListener('change', changeFunc);"
    r1 = "settingElem.addEventListener('change', changeFunc);\n        settingElem.addEventListener('input', changeFunc);"

    # 2. Update applyResizeMode to immediately act and restore 1080p when switching away from remote
    t2 = """    applyResizeMode() {
        if (!UI.rfb) return;

        UI.rfb.scaleViewport = UI.getSetting('resize') === 'scale';
        UI.rfb.resizeSession = UI.getSetting('resize') === 'remote';
    },"""

    r2 = """    applyResizeMode() {
        if (!UI.rfb) return;

        const ctrl = document.getElementById('noVNC_setting_resize');
        const mode = ctrl ? ctrl.value : UI.getSetting('resize');

        UI.rfb.scaleViewport = mode === 'scale';
        UI.rfb.resizeSession = mode === 'remote';

        if (mode === 'remote') {
            UI.rfb._requestRemoteResize();
        } else if (UI.rfb._supportsSetDesktopSize && (UI.rfb._fbWidth !== 1920 || UI.rfb._fbHeight !== 1080)) {
            UI.rfb._pendingRemoteResize = true;
            RFB.messages.setDesktopSize(UI.rfb._sock, 1920, 1080, UI.rfb._screenID, UI.rfb._screenFlags);
        }
    },"""

    if t1 in content:
        content = content.replace(t1, r1)
    if t2 in content:
        content = content.replace(t2, r2)

    with open(path, 'w') as f:
        f.write(content)
    print("Patched /usr/share/novnc/app/ui.js")

def patch_rfb():
    path = '/usr/share/novnc/core/rfb.js'
    try:
        with open(path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Skipping rfb.js patch: {e}")
        return

    t_rfb = """        this._updateContinuousUpdates();

        // Keep this size until browser client size changes"""

    r_rfb = """        this._updateContinuousUpdates();

        if (this._sock) {
            RFB.messages.fbUpdateRequest(this._sock, false, 0, 0, this._fbWidth, this._fbHeight);
        }

        // Keep this size until browser client size changes"""

    if t_rfb in content:
        content = content.replace(t_rfb, r_rfb)
        with open(path, 'w') as f:
            f.write(content)
        print("Patched /usr/share/novnc/core/rfb.js")

if __name__ == '__main__':
    patch_ui()
    patch_rfb()

