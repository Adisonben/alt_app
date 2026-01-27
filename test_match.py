#!/usr/bin/env python3
import time
from ctypes import c_ubyte

from fingerprint_sdk.pysgfplib import PYSGFPLib
from fingerprint_sdk.sgfdxdevicename import SGFDxDeviceName
from fingerprint_sdk.sgfdxerrorcode import SGFDxErrorCode


def check(result, step):
    if result != SGFDxErrorCode.SGFDX_ERROR_NONE:
        raise RuntimeError(f"{step} failed, error = {result}")
    print(f"✅ {step} OK")


def main():
    print("===================================")
    print(" SecuGen Fingerprint Test (Python) ")
    print("===================================")

    sgfplib = PYSGFPLib()

    # 1) Create
    check(sgfplib.Create(), "CreateSGFPMObject")

    # 2) Init (ระบุรุ่นตรง ๆ)
    check(sgfplib.Init(SGFDxDeviceName.SG_DEV_FDU05), "Init")

    # 3) OpenDevice (ห้ามลืม)
    check(sgfplib.OpenDevice(0), "OpenDevice")

    # 4) LED ON
    check(sgfplib.SetLedOn(True), "LED ON")

    # Hamster Pro 20 = 260x300
    width, height = 260, 300
    image = (c_ubyte * (width * height))()

    print("👉 Place finger on sensor")
    time.sleep(2)

    # 5) Get Image
    check(sgfplib.GetImage(image), "GetImage")

    # 6) LED OFF
    sgfplib.SetLedOn(False)

    # 7) Close
    check(sgfplib.CloseDevice(), "CloseDevice")
    check(sgfplib.Terminate(), "DestroySGFPMObject")

    print("=========== DONE ============")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n💥 ERROR:", e)
