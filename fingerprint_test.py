import ctypes
import numpy as np

dll_path = r"FDx_SDK\bin\x64\sgfplib.dll"
sgfplib = ctypes.WinDLL(dll_path)

# --- struct ---
class SGDeviceList(ctypes.Structure):
    _fields_ = [
        ("DevName", ctypes.c_ulong),
        ("DevID", ctypes.c_ulong),
    ]

class SGDeviceInfoParam(ctypes.Structure):
    _fields_ = [
        ("DeviceID", ctypes.c_uint32),
        ("DeviceSN", ctypes.c_ubyte * 15),
        ("Reserved", ctypes.c_ubyte),
        ("ImageWidth", ctypes.c_uint32),
        ("ImageHeight", ctypes.c_uint32),
        ("Contrast", ctypes.c_uint32),
        ("Brightness", ctypes.c_uint32),
        ("Gain", ctypes.c_uint32),
        ("ImageDPI", ctypes.c_uint32),
        ("FWVersion", ctypes.c_uint32),
    ]

# --- prototypes ---
sgfplib.SGFPM_Create.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
sgfplib.SGFPM_Create.restype  = ctypes.c_long

sgfplib.SGFPM_EnumerateDevice.argtypes = [
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.c_ulong),
    ctypes.POINTER(ctypes.POINTER(SGDeviceList)),
]
sgfplib.SGFPM_EnumerateDevice.restype = ctypes.c_long

sgfplib.SGFPM_Init.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
sgfplib.SGFPM_Init.restype  = ctypes.c_long

sgfplib.SGFPM_OpenDevice.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
sgfplib.SGFPM_OpenDevice.restype  = ctypes.c_long

sgfplib.SGFPM_GetDeviceInfo.argtypes = [ctypes.c_void_p,
                                        ctypes.POINTER(SGDeviceInfoParam)]
sgfplib.SGFPM_GetDeviceInfo.restype  = ctypes.c_long

sgfplib.SGFPM_GetImageEx.argtypes = [ctypes.c_void_p,
                                     ctypes.POINTER(ctypes.c_ubyte),
                                     ctypes.c_long,
                                     ctypes.c_void_p,
                                     ctypes.c_int]
sgfplib.SGFPM_GetImageEx.restype  = ctypes.c_long

# --- flow ---
hFPM = ctypes.c_void_p()
rc = sgfplib.SGFPM_Create(ctypes.byref(hFPM))
print("Create rc =", rc)

ndevs = ctypes.c_ulong()
devlist = ctypes.POINTER(SGDeviceList)()
rc = sgfplib.SGFPM_EnumerateDevice(hFPM, ctypes.byref(ndevs), ctypes.byref(devlist))
print("Enumerate rc =", rc, "count =", ndevs.value)

if ndevs.value > 0:
    devname = devlist[0].DevName
    print("Using DevName =", devname)

    rc = sgfplib.SGFPM_Init(hFPM, devname)
    print("Init rc =", rc)

    # --- enumerate ได้ devlist ---
    dev_id = devlist[0].DevID
    print("Using DevID =", dev_id)

    USB_AUTO_DETECT = ctypes.c_ulong(1)
    rc = sgfplib.SGFPM_OpenDevice(hFPM, USB_AUTO_DETECT)
    # rc = sgfplib.SGFPM_OpenDevice(hFPM, ctypes.c_ulong(dev_id))
    print("OpenDevice rc =", rc)
    # for dev_id in [0,1,2,255]:
    #     rc = sgfplib.SGFPM_OpenDevice(hFPM, ctypes.c_uint32(dev_id))
    #     print("Try OpenDevice with", dev_id, "→ rc =", rc)
    #     if rc == 0:
    #         break


    dev_info = SGDeviceInfoParam()
    rc = sgfplib.SGFPM_GetDeviceInfo(hFPM, ctypes.byref(dev_info))
    print("DeviceInfo rc =", rc)
    print("Width =", dev_info.ImageWidth, "Height =", dev_info.ImageHeight)

    img_size = dev_info.ImageWidth * dev_info.ImageHeight
    img_buffer = (ctypes.c_ubyte * img_size)()
    rc = sgfplib.SGFPM_GetImageEx(hFPM, img_buffer, 10000, None, 80)  
    print("GetImageEx rc =", rc)

    if rc == 0:
        img_array = np.frombuffer(img_buffer, dtype=np.uint8).reshape(
            (dev_info.ImageHeight, dev_info.ImageWidth)
        )
        print("Fingerprint captured, shape =", img_array.shape)
    else:
        print("❌ Capture failed, rc =", rc)

    sgfplib.SGFPM_CloseDevice(hFPM)
    sgfplib.SGFPM_Terminate(hFPM)
