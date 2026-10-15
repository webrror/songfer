import os
from ui.theme import color
import constants

def clear_screen():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def print_not_valid_choice():
    print()
    print(" Not a valid choice! Try again")

def print_to_go_back(letter="e"):
    print()
    print(f" Press any '{letter}' key to go back ....")
    print()

def print_instructions():
    """Prints setup instructions with 1-based indexing."""
    for idx, instruction in enumerate(constants.INSTRUCTIONS, 1):
        print(f" {idx}] {instruction}")

def print_menu(menus):
    """Prints menu options with 1-based indexing."""
    for idx, menu in enumerate(menus, 1):
        print(f" {idx} - {menu}")

def format_comma_separated_maps(result_array):
    """Returns comma-separated names from a list of dicts with 'name' key (e.g. artists)."""
    if not result_array:
        return ""
    return ", ".join(item.get("name", "") for item in result_array if "name" in item)

def format_comma_separated_list(result_array):
    """Returns comma-separated string from a list of strings (e.g. genres)."""
    if not result_array:
        return ""
    return ", ".join(str(item) for item in result_array)

def display_user_header(user):
    """Prints the welcome banner and Spotify user profile info."""
    product = constants.FREE if user.get('product') == "open" else f"{color.GREEN}{user.get('product', '').capitalize()}{color.END}"
    followers = user.get('followers', {}).get('total', 0)
    display_name = user.get('display_name', 'User')

    print()
    print(" ---------------------------------------------- ")
    print()
    print(f" Welcome {color.BOLD}{display_name}{color.END}!")
    print(f" You have {followers} followers.")
    print(f" {product} User")
    print()
    print(" ---------------------------------------------- ")

def display_devices(devices):
    """Prints active and available Spotify playback devices with emojis."""
    if not devices or 'devices' not in devices or not devices['devices']:
        return

    print(" Devices :")
    print()
    for device in devices['devices']:
        device_name = device.get('name', 'Unknown')
        device_type = device.get('type', 'Unknown')

        if device_type.lower() == "smartphone":
            emoji = "📱"
        elif device_type.lower() == "computer":
            emoji = "💻"
        else:
            emoji = "🔊"

        display_name = f"{emoji} {device_name}"
        if device.get('is_active'):
            print(f"     {color.BOLD}{display_name} ({device_type}) ✅{color.END}")
        else:
            print(f"     {display_name} ({device_type})")
    print()
