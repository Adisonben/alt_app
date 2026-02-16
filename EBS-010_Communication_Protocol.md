# EBS-010 Breathalyzer Communication Protocol

## 1. Overview

This document describes the communication protocol between the EBS-010
Breathalyzer and a computer in PC mode.

------------------------------------------------------------------------

## 2. Communication Settings

### Serial Port Configuration

  Parameter   Value
  ----------- -------
  Baudrate    4800
  Data Bits   8
  Stop Bits   1
  Parity      None

------------------------------------------------------------------------

## 3. General Communication Rules

1.  All commands must be written in CAPITAL LETTERS.
2.  Each command must end with: 0x0D 0x0A (Carriage Return + Line Feed).
3.  Commands must be sent at defined intervals depending on the state.
4.  Some commands only work in specific device states.

Example command format:

\$START 0D 0A

------------------------------------------------------------------------

## 4. Device States

-   Ready
-   Recall
-   Warming Up
-   Standby
-   Sampling
-   Trigger
-   Result
-   Calibration Period

------------------------------------------------------------------------

## 5. Commands (Computer → EBS-010)

All commands must end with: 0x0D 0x0A

### \$START

-   Works only in state: \$END
-   Send once at the beginning of warm-up

### \$END

### \$WAIT

### \$STANBY

### \$BREATH

-   Activates breath sampling

### \$TRIGGER

### \$RESET

-   Turns the device OFF
-   Works only in state: \$STANBY

### \$RECALL

-   Checks the set value
-   Works only in state: \$END

### \$CALIBRATION

-   Calibration period: 1,000 tests

------------------------------------------------------------------------

## 6. Responses (EBS-010 → Computer)

### Flow Error

\$FLOW,ERR - Indicates incorrect breath sampling

### Result Format

\$RESULT,0.000-OK

-   "OK" or "HIGH"
-   Based on preset limit

Example: If preset limit = 0.30 g/L - Result \> 0.30 g/L → HIGH - Result
≤ 0.30 g/L → OK

### Detailed Result Format

\$U/B,L/000,H/000,T/0000

Where: - U: Measurement Unit (B=%BAC, G=g/L, M=mg/L) - L: LOW result -
H: HIGH result - T: Testing number (0000--9999)

------------------------------------------------------------------------

## 7. Calibration Information

-   Calibration required every 1,000 tests
