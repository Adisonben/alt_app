from fingerprint.service import FingerprintService
import time

fp = FingerprintService()
fp.start()

print("Scan #1")
time.sleep(2)
t1 = fp.enroll()

print("Scan #2")
time.sleep(2)
t2 = fp.enroll()

matched, score = fp.verify(t1, t2)

print("MATCH :", matched)
print("SCORE :", score)

fp.stop()
