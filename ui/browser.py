import os
import sys
import subprocess
import webbrowser
import constants

POPULAR_BROWSERS = [
    ("default", "System Default"),
    ("Google Chrome", "Google Chrome"),
    ("Safari", "Safari"),
    ("Arc", "Arc"),
    ("Brave Browser", "Brave Browser"),
    ("Firefox", "Firefox"),
    ("Microsoft Edge", "Microsoft Edge"),
]

def get_preferred_browser() -> str:
    """Reads saved browser preference from user.yml. Defaults to 'default'."""
    if os.path.exists(constants.USER_YML) and os.path.getsize(constants.USER_YML) > 0:
        with open(constants.USER_YML, "r") as f:
            for line in f:
                key, sep, val = line.strip().partition(":")
                if key.strip() == "BROWSER":
                    return val.strip() or "default"
    return "default"

def get_preferred_browser_display_name() -> str:
    """Returns a user-friendly display name of the preferred browser."""
    current = get_preferred_browser()
    for raw, display in POPULAR_BROWSERS:
        if current.lower() == raw.lower():
            return display
    return current

def set_preferred_browser(browser_name: str):
    """Saves or updates the BROWSER key in user.yml."""
    lines = []
    found = False
    if os.path.exists(constants.USER_YML):
        with open(constants.USER_YML, "r") as f:
            lines = f.readlines()

    new_lines = []
    for line in lines:
        key, sep, _ = line.strip().partition(":")
        if key.strip() == "BROWSER":
            new_lines.append(f"BROWSER:{browser_name}\n")
            found = True
        else:
            new_lines.append(line if line.endswith("\n") else line + "\n")

    if not found:
        new_lines.append(f"BROWSER:{browser_name}\n")

    with open(constants.USER_YML, "w") as f:
        f.writelines(new_lines)

def open_in_browser(url: str):
    """Opens a URL in the user's preferred browser."""
    if not url:
        return

    browser = get_preferred_browser()

    if browser.lower() == "default":
        webbrowser.open(url)
    elif sys.platform == "darwin":
        # On macOS, launch via 'open -a <BrowserApp>'
        try:
            subprocess.run(["open", "-a", browser, url], check=True)
        except subprocess.CalledProcessError:
            # Fallback to system default if specified browser fails to open
            webbrowser.open(url)
    else:
        try:
            webbrowser.get(browser.lower()).open(url)
        except webbrowser.Error:
            webbrowser.open(url)

def choose_browser_menu():
    """Interactive menu to select and save preferred browser."""
    current = get_preferred_browser_display_name()
    print()
    print(" ---- BROWSER PREFERENCE ---- ")
    print(f" Current Browser: {current}")
    print()

    for idx, (_, display) in enumerate(POPULAR_BROWSERS, 1):
        is_current = " (Current)" if display.lower() == current.lower() else ""
        print(f" {idx} - {display}{is_current}")

    custom_idx = len(POPULAR_BROWSERS) + 1
    print(f" {custom_idx} - Other (Type custom app name)")
    print(f" e - Go back")
    print()

    choice = input(" Your choice : ").strip()
    if choice.lower() == "e":
        return

    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(POPULAR_BROWSERS):
            selected_raw, selected_display = POPULAR_BROWSERS[choice_num - 1]
            set_preferred_browser(selected_raw)
            print()
            print(f" ✅ Preferred browser saved: {selected_display}")
        elif choice_num == custom_idx:
            custom_name = input(" Enter application name (e.g. Opera, Vivaldi): ").strip()
            if custom_name:
                set_preferred_browser(custom_name)
                print()
                print(f" ✅ Preferred browser saved: {custom_name}")
        else:
            print("\n Not a valid choice! Try again")
    except ValueError:
        print("\n Not a valid choice! Try again")
