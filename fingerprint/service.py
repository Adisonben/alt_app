from .sgfplib import SGFPLib


class FingerprintService:
    def __init__(self):
        self.sdk = SGFPLib()

    def start(self):
        self.sdk.create()
        self.sdk.init_ex()
        self.sdk.open_device()

    def stop(self):
        self.sdk.close_device()
        self.sdk.terminate()

    def enroll(self):
        self.sdk.led(True)
        res, img = self.sdk.get_image()
        self.sdk.led(False)
        res, tmpl = self.sdk.create_template(img)
        return tmpl

    def verify(self, tmpl1, tmpl2):
        return self.sdk.match(tmpl1, tmpl2)
