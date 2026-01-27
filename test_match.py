#!/usr/bin/env python3
import time

from fingerprint_sdk.pysgfplib import PYSGFPLib
from fingerprint_sdk.sgfdxdevicename import SGFDxDeviceName
from fingerprint_sdk.sgfdxerrorcode import SGFDxErrorCode
from fingerprint_sdk.sgfdxsecuritylevel import SGFDxSecurityLevel


def check(result, step_name):
    if result != SGFDxErrorCode.SGFDX_ERROR_NONE:
        raise RuntimeError(f"❌ {step_name} failed, error = {result}")
    print(f"✅ {step_name} OK")


def main():
    print("===================================")
    print(" SecuGen Fingerprint Test (Python) ")
    print("===================================")

    sgfplib = PYSGFPLib()

    # 1) Create object
    check(sgfplib.Create(), "CreateSGFPMObject")

    # 2) Init device (auto detect)
    check(sgfplib.Init(SGFDxDeviceName.SG_DEV_FDU05), "Init")

    # 3) Open device
    check(sgfplib.OpenDevice(0), "OpenDevice")

    # 4) Get image size
    width, height = sgfplib.GetImageSize()
    print(f"Image size : {width} x {height}")

    # Prepare image buffers
    image1 = bytearray(width * height)
    image2 = bytearray(width * height)

    print("\n👉 Scan #1 : Place finger on sensor")
    time.sleep(2)
    check(sgfplib.GetImage(image1), "GetImage #1")

    print("👉 Scan #2 : Place SAME finger again")
    time.sleep(2)
    check(sgfplib.GetImage(image2), "GetImage #2")

    # 5) Create templates (SG400 format)
    template1 = bytearray(400)
    template2 = bytearray(400)

    check(
        sgfplib.CreateSG400Template(image1, template1),
        "CreateTemplate #1"
    )
    check(
        sgfplib.CreateSG400Template(image2, template2),
        "CreateTemplate #2"
    )

    # 6) Match templates
    matched, score = sgfplib.MatchTemplate(
        template1,
        template2,
        SGFDxSecurityLevel.SL_NORMAL
    )

    print("\n========== RESULT ==========")
    print("Matched :", matched)
    print("Score   :", score)

    if matched:
        print("✅ Fingerprint MATCH")
    else:
        print("❌ Fingerprint NOT MATCH")

    # 7) Close device
    check(sgfplib.CloseDevice(), "CloseDevice")
    check(sgfplib.Terminate(), "DestroySGFPMObject")

    print("=========== DONE ============")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n💥 ERROR:", e)
