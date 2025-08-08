from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock
from kivy.core.text import LabelBase
from datetime import datetime
from kivy.uix.image import Image
from kivy.animation import Animation
import random

# ✅ Register Thai font
LabelBase.register(name="THSarabunNew", fn_regular="fonts/THSarabunNew.ttf")

# ✅ Global Device Info
device_info = {
    "deviceId": "ALK-001",
    "status": "Online",
    "ping": "12ms",
    "ipAddress": "192.168.1.100",
    "version": "v2.1.3",
    "lastMaintenance": "2025-08-01"
}


# ✅ Device Info Widget
class DeviceInfoWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 5
        self.spacing = 2
        self.size_hint_y = None
        self.height = 140

        for key, value in device_info.items():
            label = Label(text=f"{key}: {value}", font_name="THSarabunNew", font_size=18, halign="left")
            self.add_widget(label)


# ✅ Step 1
class Step1Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(DeviceInfoWidget())

        # ✅ เพิ่มรูปภาพ
        img = Image(source='assets/fingerprint.png', size_hint=(1, 0.5))
        layout.add_widget(img)

        # ✅ ใส่ animation แบบ pulse
        anim = Animation(size_hint=(1.05, 0.55), duration=0.6) + Animation(size_hint=(1, 0.5), duration=0.6)
        anim.repeat = True
        anim.start(img)

        label = Label(text="ระบบตรวจวัดแอลกอฮอล์\nโปรดสแกนลายนิ้วมือเพื่อเริ่มต้น", font_name="THSarabunNew", font_size=30)
        layout.add_widget(label)

        btn = Button(text="จำลองการสแกน", font_name="THSarabunNew", font_size=26, size_hint=(1, 0.2))
        btn.bind(on_press=self.next_step)
        layout.add_widget(btn)

        self.add_widget(layout)

    def next_step(self, *args):
        self.manager.current = "step2"
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'step3'), 2)


# ✅ Step 2
class Step2Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(DeviceInfoWidget())

        img = Image(source='assets/user.png', size_hint=(1, 0.4))
        layout.add_widget(img)


        label = Label(text="ยืนยันตัวตน\n\nตรวจสอบสำเร็จ\nชื่อ: สมชาย ใจดี\nรหัส: EMP001234\nสถานะ: อนุมัติ",
                      font_name="THSarabunNew", font_size=28)
        layout.add_widget(label)

        loading = Label(text="กำลังเตรียมการตรวจวัด...", font_name="THSarabunNew", font_size=22)
        layout.add_widget(loading)

        self.add_widget(layout)


# ✅ Step 3
class Step3Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(DeviceInfoWidget())

        label = Label(text="เริ่มการตรวจวัด\n\nโปรดเป่าลมเข้าเครื่องวัดแอลกอฮอล์\nเป่าอย่างแรงและต่อเนื่อง", font_name="THSarabunNew", font_size=26)
        layout.add_widget(label)

        btn = Button(text="เริ่มการตรวจวัด", font_name="THSarabunNew", font_size=28, size_hint=(1, 0.2))
        btn.bind(on_press=self.start_test)
        layout.add_widget(btn)

        self.add_widget(layout)

    def start_test(self, *args):
        self.manager.current = "step4"
        Clock.schedule_once(self.finish_test, 10)

    def finish_test(self, dt):
        result = random.choice(["pass", "fail"])
        self.manager.get_screen("step5").set_result(result)
        self.manager.current = "step5"
        Clock.schedule_once(lambda dt: setattr(self.manager, "current", "step1"), 5)


# ✅ Step 4 - Loading
class Step4Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(DeviceInfoWidget())
        label = Label(text="กรุณาเป่า...\n\nกำลังตรวจวัด...", font_name="THSarabunNew", font_size=28)
        layout.add_widget(label)
        self.add_widget(layout)


# ✅ Step 5 - Result
class Step5Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.add_widget(DeviceInfoWidget())

        self.result_label = Label(text="", font_name="THSarabunNew", font_size=30)
        self.layout.add_widget(self.result_label)
        self.info_label = Label(text="", font_name="THSarabunNew", font_size=22)
        self.layout.add_widget(self.info_label)

        retry_btn = Button(text="ตรวจใหม่", font_name="THSarabunNew", font_size=28, size_hint=(1, 0.2))
        retry_btn.bind(on_press=self.retry)
        self.layout.add_widget(retry_btn)

        self.add_widget(self.layout)

    def set_result(self, result):
        is_pass = result == "pass"
        img = Image(source=f"assets/{'pass' if is_pass else 'fail'}.png", size_hint=(1, 0.4))
        self.layout.add_widget(img, index=1)  # index=1 เพื่อให้แทรกระหว่าง DeviceInfo กับข้อความ
        self.result_label.text = "ผ่าน" if is_pass else "ไม่ผ่าน"
        color = "[color=00AA00]" if is_pass else "[color=FF0000]"
        alcohol_level = "0.00 mg/L" if is_pass else "0.25 mg/L"
        self.info_label.text = (
            f"{color}ผลการตรวจวัด: {alcohol_level}[/color]\n"
            f"เกณฑ์: ≤ 0.05 mg/L\n"
            f"วันที่: {datetime.now().strftime('%d/%m/%Y')}\n"
            f"เวลา: {datetime.now().strftime('%H:%M:%S')}"
        )

    def retry(self, *args):
        self.manager.current = "step1"


# ✅ Main App
class AlcoholKioskApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(Step1Screen(name="step1"))
        sm.add_widget(Step2Screen(name="step2"))
        sm.add_widget(Step3Screen(name="step3"))
        sm.add_widget(Step4Screen(name="step4"))
        sm.add_widget(Step5Screen(name="step5"))
        return sm


if __name__ == '__main__':
    AlcoholKioskApp().run()
