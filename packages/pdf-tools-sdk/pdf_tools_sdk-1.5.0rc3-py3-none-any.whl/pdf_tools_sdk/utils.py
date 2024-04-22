import os
import platform
from ctypes import *

def load_library():
    # Define the library name
    lib_name = "PdfToolsSdk"

    # Get the current platform
    current_platform = platform.system().lower()
    if current_platform == "linux":
        lib_name = "lib" + lib_name + ".so"
    elif current_platform == "darwin":
        lib_name = "lib" + lib_name + ".dylib"
    elif current_platform == "windows":
        lib_name += ".dll"

    # Get the current architecture
    current_arch = platform.machine()

    # Map the platform and architecture to the corresponding folder
    folder_map = {
        "linux": {
            "x86_64": "linux-x64"
        },
        "darwin": {
            "x86_64": "osx-x64",
            "arm64": "osx-arm64"
        },
        "windows": {
            "AMD64": "win-x64",
            "x86": "win-x86"
        }
    }

    # Get the platform and architecture specific folder
    folder = folder_map.get(current_platform, {}).get(current_arch, "")

    # Get the directory of the current file
    dir_path = os.path.dirname(os.path.abspath(__file__))

    # Construct the library path
    lib_path = os.path.join(dir_path, "lib", folder, lib_name)

    # Load the library
    try:
        lib = CDLL(lib_path)
        print(f"Successfully loaded library from {lib_path}")
        return lib
    except OSError as e:
        print(f"Failed to load library from {lib_path}: {e}")
        return None