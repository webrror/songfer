import os
import sys
import subprocess
import tempfile

def render_album_art(art_url: str):
    """
    Downloads album art to a temporary file and renders it in the terminal
    using viu if supported by the terminal emulator.
    """
    if not art_url:
        return

    if not (sys.platform == 'darwin' or sys.platform == 'linux'):
        return

    term_prog = os.environ.get("TERM_PROGRAM", "")
    if term_prog in ('iTerm.app', 'vscode', 'WezTerm', 'ghostty'):
        temp_art = os.path.join(tempfile.gettempdir(), "songfer_art.jpg")
        subprocess.run(["curl", "-s", "-o", temp_art, art_url])

        if term_prog == 'ghostty':
            subprocess.run(["viu", "-x", "1", "-w", "20", "-h", "0", temp_art])
            print()
            print()
        else:
            subprocess.run(["viu", "-x", "1", "-w", "20", temp_art])
            print()

        try:
            import termios
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
        except Exception:
            pass
