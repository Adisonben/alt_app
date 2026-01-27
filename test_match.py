#!/usr/bin/env python3
import time

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

    check(sgfplib.Create(), "CreateSGFPMObject")
    check(sgfplib.Init(SGFDxDeviceName.SG_DEV_FDU05), "Init")

    print("👉 LED ON")
    sgfplib.SetLedOn(True)

    width, height = 260, 300
    image = bytearray(width * height)

    print("👉 Place finger on sensor")
    time.sleep(2)
    check(sgfplib.GetImage(image), "GetImage")

    sgfplib.SetLedOn(False)

    check(sgfplib.Terminate(), "DestroySGFPMObject")
    print("=========== DONE ============")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n💥 ERROR:", e)
