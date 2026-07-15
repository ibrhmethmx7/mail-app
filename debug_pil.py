import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")
print("sys.path:")
for p in sys.path:
    print(f"  {p}")

try:
    import PIL
    print(f"PIL imported successfully. File: {PIL.__file__}")
    from PIL import Image, ImageTk
    print("Image, ImageTk imported successfully.")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
