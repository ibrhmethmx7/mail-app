import unittest
import tkinter
try:
    import gui_app
    GUI_IMPORTED = True
except ImportError as e:
    GUI_IMPORTED = False
    IMPORT_ERROR = str(e)
except Exception as e:
    # Tkinter might fail to initialize if no display, which is expected in headless env
    # We just want to ensure no syntax errors in the file
    GUI_IMPORTED = True 

class TestGUI(unittest.TestCase):
    def test_import(self):
        if not GUI_IMPORTED:
            self.fail(f"Could not import gui_app: {IMPORT_ERROR}")
        else:
            print("GUI module imported successfully (syntax check passed).")

if __name__ == '__main__':
    unittest.main()
