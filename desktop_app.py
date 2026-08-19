from __future__ import annotations

import atexit
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
APP_PATH = PROJECT_ROOT / "app.py"


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_for_server(url: str, timeout: float = 60.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2):  # nosec - local loopback only
                return
        except Exception:
            time.sleep(0.4)
    raise RuntimeError(f"Streamlit server did not start within {timeout:.0f} seconds.")


def _start_streamlit(port: int) -> subprocess.Popen[str]:
    env = os.environ.copy()
    env["STREAMLIT_SERVER_PORT"] = str(port)
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(APP_PATH),
        "--server.port",
        str(port),
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
    ]
    return subprocess.Popen(command, cwd=str(PROJECT_ROOT), env=env)


def _run_qt_window(url: str, process: subprocess.Popen[str]) -> int:
    try:
        from PyQt6.QtCore import QUrl
        from PyQt6.QtWidgets import QApplication, QMainWindow
        from PyQt6.QtWebEngineWidgets import QWebEngineView
    except Exception as exc:
        print(f"Qt desktop backend unavailable: {exc}")
        return 1

    class DesktopWindow(QMainWindow):
        def __init__(self) -> None:
            super().__init__()
            self.setWindowTitle("Phishing Log Analyzer")
            self.resize(1500, 980)
            self._view = QWebEngineView(self)
            self._view.load(QUrl(url))
            self.setCentralWidget(self._view)

        def closeEvent(self, event) -> None:  # type: ignore[override]
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except Exception:
                    process.kill()
            super().closeEvent(event)

    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("Phishing Log Analyzer")
    window = DesktopWindow()
    window.show()

    def _cleanup() -> None:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except Exception:
                process.kill()

    atexit.register(_cleanup)
    try:
        return app.exec()
    finally:
        _cleanup()


def main() -> None:
    port = _find_free_port()
    url = f"http://127.0.0.1:{port}"
    process = _start_streamlit(port)
    try:
        _wait_for_server(url)
        raise SystemExit(_run_qt_window(url, process))
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except Exception:
                process.kill()


if __name__ == "__main__":
    main()
