/*************************************************************
 * File: finger_scan.cpp
 * Description: Fingerprint scan and output template as Base64
 * Based on SecuGen SDK example
 *************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "sgfplib.h"

LPSGFPM sgfplib = NULL;

int getPIVQuality(int quality)
{
    if (quality <= 20) return 20;
    if (quality <= 40) return 40;
    if (quality <= 60) return 60;
    if (quality <= 80) return 80;
    return 100;
}

int main(int argc, char **argv)
{
    long err;
    DWORD templateSize, templateSizeMax;
    DWORD quality;
    BYTE *imageBuffer;
    BYTE *templateBuffer;
    SGDeviceInfoParam deviceInfo;
    SGFingerInfo fingerInfo;

    // Create SGFPM object
    err = CreateSGFPMObject(&sgfplib);
    if (!sgfplib)
    {
        fprintf(stderr, "ERROR: Unable to create SGFPM object.\n");
        return 1;
    }

    // Initialize with auto-detect device
    err = sgfplib->Init(SG_DEV_AUTO);
    if (err != SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "ERROR: Unable to initialize device. Error: %ld\n", err);
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Open device
    err = sgfplib->OpenDevice(0);
    if (err != SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "ERROR: Unable to open device. Error: %ld\n", err);
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Get device info
    deviceInfo.DeviceID = 0;
    err = sgfplib->GetDeviceInfo(&deviceInfo);
    if (err != SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "ERROR: Unable to get device info. Error: %ld\n", err);
        sgfplib->CloseDevice();
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Allocate image buffer
    imageBuffer = (BYTE*)malloc(deviceInfo.ImageHeight * deviceInfo.ImageWidth);
    if (!imageBuffer)
    {
        fprintf(stderr, "ERROR: Memory allocation failed.\n");
        sgfplib->CloseDevice();
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Turn on LED to indicate ready
    sgfplib->SetLedOn(true);

    fprintf(stderr, "Please place finger on sensor...\n");

    // Capture image with quality check (timeout 10 seconds, min quality 50%)
    DWORD timeout = 10000;
    DWORD minQuality = 50;
    err = sgfplib->GetImageEx(imageBuffer, timeout, NULL, minQuality);

    if (err != SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "ERROR: Failed to capture fingerprint. Error: %ld\n", err);
        sgfplib->SetLedOn(false);
        free(imageBuffer);
        sgfplib->CloseDevice();
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Turn off LED
    sgfplib->SetLedOn(false);

    // Get image quality
    err = sgfplib->GetImageQuality(deviceInfo.ImageWidth, deviceInfo.ImageHeight, imageBuffer, &quality);
    if (err != SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "WARNING: Could not get image quality.\n");
        quality = 50;
    }

    fprintf(stderr, "Image quality: %ld%%\n", quality);

    // Set template format to SG400 (SecuGen proprietary format)
    err = sgfplib->SetTemplateFormat(TEMPLATE_FORMAT_SG400);
    if (err != SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "ERROR: Failed to set template format. Error: %ld\n", err);
        free(imageBuffer);
        sgfplib->CloseDevice();
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Get max template size
    err = sgfplib->GetMaxTemplateSize(&templateSizeMax);
    if (err != SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "ERROR: Failed to get max template size. Error: %ld\n", err);
        free(imageBuffer);
        sgfplib->CloseDevice();
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Allocate template buffer
    templateBuffer = (BYTE*)malloc(templateSizeMax);
    if (!templateBuffer)
    {
        fprintf(stderr, "ERROR: Memory allocation failed.\n");
        free(imageBuffer);
        sgfplib->CloseDevice();
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Create template
    fingerInfo.FingerNumber = SG_FINGPOS_UK;
    fingerInfo.ViewNumber = 0;
    fingerInfo.ImpressionType = SG_IMPTYPE_LP;
    fingerInfo.ImageQuality = getPIVQuality(quality);

    err = sgfplib->CreateTemplate(&fingerInfo, imageBuffer, templateBuffer);
    if (err != SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "ERROR: Failed to create template. Error: %ld\n", err);
        free(templateBuffer);
        free(imageBuffer);
        sgfplib->CloseDevice();
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Get actual template size
    err = sgfplib->GetTemplateSize(templateBuffer, &templateSize);
    if (err != SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "ERROR: Failed to get template size. Error: %ld\n", err);
        free(templateBuffer);
        free(imageBuffer);
        sgfplib->CloseDevice();
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    fprintf(stderr, "Template size: %ld bytes\n", templateSize);

    // Convert to Base64
    // Base64 output size is approximately (input_size + 2) / 3 * 4 + 1
    DWORD base64Size = ((templateSize + 2) / 3) * 4 + 1;
    LPTSTR base64Buffer = (LPTSTR)malloc(base64Size);
    if (!base64Buffer)
    {
        fprintf(stderr, "ERROR: Memory allocation failed.\n");
        free(templateBuffer);
        free(imageBuffer);
        sgfplib->CloseDevice();
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    err = sgfplib->ByteToText(templateBuffer, templateSize, base64Buffer);
    if (err != SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "ERROR: Failed to convert to Base64. Error: %ld\n", err);
        free(base64Buffer);
        free(templateBuffer);
        free(imageBuffer);
        sgfplib->CloseDevice();
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Output Base64 to stdout
    printf("%s\n", (char*)base64Buffer);

    // Cleanup
    free(base64Buffer);
    free(templateBuffer);
    free(imageBuffer);
    sgfplib->CloseDevice();
    DestroySGFPMObject(sgfplib);

    return 0;
}
