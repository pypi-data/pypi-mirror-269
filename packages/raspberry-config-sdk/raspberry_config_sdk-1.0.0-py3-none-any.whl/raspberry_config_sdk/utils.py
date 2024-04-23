def is_running_bookworm() -> bool:
    try:
        # Open the file
        with open("/etc/os-release", "r") as file:
            # Read the contents
            file_contents = file.read()
            # Check if "bookworm" appears in the contents
            if "bookworm" in file_contents:
                return True
            return False
    except FileNotFoundError:
        print("Error: File '/etc/os-release' not found.")
        return False
