/*************************************************************
 * File: match_template.cpp
 * Description: Match two fingerprint templates (Base64 input)
 * Usage: ./match_template <base64_template1> <base64_template2>
 * Returns: 1 (match) or 0 (no match) to stdout
 * Exit code: 0 on success, 1 on error
 * Based on SecuGen SDK example
 *************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "sgfplib.h"

LPSGFPM sgfplib = NULL;

int main(int argc, char **argv)
{
    long err;
    BOOL matched;
    DWORD score;
    BYTE *templateBuffer1 = NULL;
    BYTE *templateBuffer2 = NULL;
    DWORD templateSize1, templateSize2;

    // Check command line arguments
    if (argc != 3)
    {
        fprintf(stderr, "Usage: %s <base64_template1> <base64_template2>\n", argv[0]);
        fprintf(stderr, "Returns: 1 (match) or 0 (no match) to stdout\n");
        return 1;
    }

    // Create SGFPM object
    err = CreateSGFPMObject(&sgfplib);
    if (!sgfplib)
    {
        fprintf(stderr, "ERROR: Unable to create SGFPM object.\n");
        return 1;
    }

    // Initialize with auto-detect device (required for matching algorithm)
    err = sgfplib->Init(SG_DEV_AUTO);
    if (err != SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "ERROR: Unable to initialize. Error: %ld\n", err);
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Set template format to SG400 (must match the format used for scanning)
    err = sgfplib->SetTemplateFormat(TEMPLATE_FORMAT_SG400);
    if (err != SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "ERROR: Failed to set template format. Error: %ld\n", err);
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Get max template size for buffer allocation
    DWORD templateSizeMax;
    err = sgfplib->GetMaxTemplateSize(&templateSizeMax);
    if (err != SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "ERROR: Failed to get max template size. Error: %ld\n", err);
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Allocate buffers for templates
    templateBuffer1 = (BYTE*)malloc(templateSizeMax);
    templateBuffer2 = (BYTE*)malloc(templateSizeMax);
    if (!templateBuffer1 || !templateBuffer2)
    {
        fprintf(stderr, "ERROR: Memory allocation failed.\n");
        if (templateBuffer1) free(templateBuffer1);
        if (templateBuffer2) free(templateBuffer2);
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Decode Base64 template 1
    templateSize1 = templateSizeMax;
    err = sgfplib->TextToByte((LPTSTR)argv[1], templateBuffer1, &templateSize1);
    if (err != SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "ERROR: Failed to decode Base64 template 1. Error: %ld\n", err);
        free(templateBuffer1);
        free(templateBuffer2);
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Decode Base64 template 2
    templateSize2 = templateSizeMax;
    err = sgfplib->TextToByte((LPTSTR)argv[2], templateBuffer2, &templateSize2);
    if (err != SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "ERROR: Failed to decode Base64 template 2. Error: %ld\n", err);
        free(templateBuffer1);
        free(templateBuffer2);
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Match templates using NORMAL security level
    err = sgfplib->MatchTemplate(templateBuffer1, templateBuffer2, SL_NORMAL, &matched);
    if (err != SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "ERROR: Failed to match templates. Error: %ld\n", err);
        free(templateBuffer1);
        free(templateBuffer2);
        DestroySGFPMObject(sgfplib);
        return 1;
    }

    // Get matching score for debug info
    err = sgfplib->GetMatchingScore(templateBuffer1, templateBuffer2, &score);
    if (err == SGFDX_ERROR_NONE)
    {
        fprintf(stderr, "Matching score: %ld\n", score);
    }

    // Output result: 1 for match, 0 for no match
    if (matched)
    {
        printf("1\n");
        fprintf(stderr, "Result: MATCH\n");
    }
    else
    {
        printf("0\n");
        fprintf(stderr, "Result: NO MATCH\n");
    }

    // Cleanup
    free(templateBuffer1);
    free(templateBuffer2);
    DestroySGFPMObject(sgfplib);

    return 0;
}
