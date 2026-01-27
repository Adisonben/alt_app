from ctypes import *

# โหลด C SDK ตัวจริง
LIB_PATH = "/usr/local/lib/libsgfplib.so"


class SGFPLib:
    def __init__(self):
        self.lib = CDLL(LIB_PATH)

        # --- function signatures ---
        self.lib.SGFPM_Create.restype = c_ulong

        self.lib.SGFPM_Terminate.restype = c_ulong

        self.lib.SGFPM_InitEx.argtypes = [c_ulong, c_ulong, c_ulong]
        self.lib.SGFPM_InitEx.restype  = c_ulong

        self.lib.SGFPM_OpenDevice.argtypes = [c_ulong]
        self.lib.SGFPM_OpenDevice.restype  = c_ulong

        self.lib.SGFPM_CloseDevice.restype = c_ulong

        self.lib.SGFPM_SetLedOn.argtypes = [c_bool]
        self.lib.SGFPM_SetLedOn.restype  = c_ulong

        self.lib.SGFPM_GetImage.argtypes = [POINTER(c_ubyte)]
        self.lib.SGFPM_GetImage.restype  = c_ulong

        self.lib.SGFPM_CreateSG400Template.argtypes = [
            POINTER(c_ubyte),
            POINTER(c_ubyte)
        ]
        self.lib.SGFPM_CreateSG400Template.restype = c_ulong

        self.lib.SGFPM_MatchTemplate.argtypes = [
            POINTER(c_ubyte),
            POINTER(c_ubyte),
            c_ulong,
            POINTER(c_bool)
        ]
        self.lib.SGFPM_MatchTemplate.restype = c_ulong

        self.lib.SGFPM_GetMatchingScore.argtypes = [
            POINTER(c_ubyte),
            POINTER(c_ubyte),
            POINTER(c_ulong)
        ]
        self.lib.SGFPM_GetMatchingScore.restype = c_ulong

    # --- wrappers ---
    def create(self):
        return self.lib.SGFPM_Create()

    def terminate(self):
        return self.lib.SGFPM_Terminate()

    def init_ex(self, w=260, h=300, dpi=500):
        return self.lib.SGFPM_InitEx(w, h, dpi)

    def open_device(self, idx=0):
        return self.lib.SGFPM_OpenDevice(idx)

    def close_device(self):
        return self.lib.SGFPM_CloseDevice()

    def led(self, on=True):
        return self.lib.SGFPM_SetLedOn(on)

    def get_image(self):
        buf = (c_ubyte * (260 * 300))()
        res = self.lib.SGFPM_GetImage(buf)
        return res, buf

    def create_template(self, image):
        tmpl = (c_ubyte * 400)()
        res = self.lib.SGFPM_CreateSG400Template(image, tmpl)
        return res, tmpl

    def match(self, t1, t2, level=3):
        matched = c_bool()
        score = c_ulong()

        self.lib.SGFPM_MatchTemplate(t1, t2, level, byref(matched))
        self.lib.SGFPM_GetMatchingScore(t1, t2, byref(score))

        return matched.value, score.value
# --- end of SGFPLib ---