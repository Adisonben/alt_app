#!/usr/bin/env python3
import time
from ctypes import c_ubyte

from fingerprint_sdk.pysgfplib import PYSGFPLib
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

    # 2) InitEx (สำคัญที่สุด)
    check(sgfplib.InitEx(260, 300, 500), "InitEx")

    # 3) OpenDevice
    check(sgfplib.OpenDevice(0), "OpenDevice")

    # 4) LED ON
    sgfplib.SetLedOn(True)

    image = (c_ubyte * (260 * 300))()

    print("👉 Place finger on sensor")
    time.sleep(2)

    check(sgfplib.GetImage(image), "GetImage")

    sgfplib.SetLedOn(False)

    check(sgfplib.CloseDevice(), "CloseDevice")
    check(sgfplib.Terminate(), "DestroySGFPMObject")

    print("=========== DONE ===========")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n💥 ERROR:", e)
