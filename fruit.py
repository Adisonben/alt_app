import kivy
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.text import LabelBase
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp


LabelBase.register(
    name="THSarabunNewBold",
    fn_regular="fonts/THSarabunNew.ttf"  
)

kivy.require('2.0.0')

# Class สำหรับเนื้อหา Dialog สรุปผล
class FinalResultsContent(MDBoxLayout):
    final_score = NumericProperty(0)

class CuteTimeUpContent(MDBoxLayout):

    
    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=dp(15),
            padding=dp(20),
            size_hint_y=None,
            **kwargs
        )

        # หัวข้อใหญ่
        self.title = MDLabel(
            text="หมดเวลา!",
            halign="center",
            font_name="THSarabunNewBold",
            font_size="50sp",
            theme_text_color="Custom",
            text_color=(1, 0.3, 0.3, 1),
            size_hint_y=None,
            markup=True
        )
        self.title.bind(texture_size=lambda inst, val: setattr(inst, "height", val[1]))

        # คำอธิบาย
        self.desc = MDLabel(
            text="คุณจะต้องตอบคำถามถัดไป",
            halign="center",
            font_name="THSarabunNewBold",
            font_size="40sp",
            theme_text_color="Custom",
            text_color=(1, 0.6, 0.2, 1),
            size_hint_y=None,
            markup=True
        )
        self.desc.bind(texture_size=lambda inst, val: setattr(inst, "height", val[1]))

        self.add_widget(self.title)
        self.add_widget(self.desc)

        # ทำให้ layout ขยายตาม content
        self.bind(minimum_height=self.setter("height"))

class FinalResultsContent(MDBoxLayout):
    final_score = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=dp(15),
            padding=dp(20),
            size_hint_y=None,
            **kwargs
        )

        self.title = MDLabel(
            text="ยินดีด้วย! คุณตอบคำถามครบแล้ว",
            halign="center",
            font_name="THSarabunNewBold",
            font_size="50sp",
            theme_text_color="Custom",
            text_color=(1, 0.3, 0.3, 1),
            size_hint_y=None,
            markup=True
        )
        self.title.bind(texture_size=lambda inst, val: setattr(inst, "height", val[1]))

        self.score_label = MDLabel(
            text=f"คะแนนทั้งหมด : {self.final_score}",
            halign="center",
            font_name="THSarabunNewBold",
            font_size="45sp",
            theme_text_color="Custom",
            text_color=(1, 0.6, 0.2, 1),
            size_hint_y=None,
            markup=True
        )
        self.score_label.bind(texture_size=lambda inst, val: setattr(inst, "height", val[1]))

        self.add_widget(self.title)
        self.add_widget(self.score_label)

        self.bind(minimum_height=self.setter("height"))


class RootGameScreen(MDScreen):

    score = NumericProperty(0)
    WORD_LIST = [
        {"en": "Apple", "cn": "苹果", "pinyin": "píng guǒ", "img": 'images/apple.jpg'},
        {"en": "Orange", "cn": "橙子", "pinyin": "chéng zi", "img": 'images/orange.png'},
        {"en": "Banana", "cn": "香蕉", "pinyin": "xiāng jiāo", "img": 'images/banana.jpg'},
        {"en": "Grape", "cn": "葡萄", "pinyin": "pú táo", "img": 'images/grape.jpg'},
        {"en": "Mango", "cn": "芒果", "pinyin": "máng guǒ ", "img": 'images/mango.jpg'},
        {"en": "Watermelon", "cn": "西瓜", "pinyin": "xī guā", "img": 'images/watermelon.jpg'},
        {"en": "Strawberry", "cn": "草莓", "pinyin": "cǎo méi", "img": 'images/strawberry.jpg'},
    ]

    image_source = StringProperty('images/apple.jpg')
    word_en = StringProperty("Apple")
    word_cn = StringProperty("苹果")
    word_pinyin = StringProperty("píng guǒ")
    current_word_index = NumericProperty(0)

    image_x_pos = NumericProperty(0)
    game_over = BooleanProperty(False)

    timer_progress_value = NumericProperty(100)
    countdown_display = StringProperty("10 s")
    current_time_sec = NumericProperty(10.0)
    is_running = BooleanProperty(False)
    MAX_TIME = 10.0
    timer_event = None
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.MAX_TIME = 10
        self.timer_event = None
        Clock.schedule_once(self.start_timer_on_load, 0.5)

    def start_timer_on_load(self, dt):
        self.start_timer()

    def start_timer(self):
        if self.timer_event:
            self.timer_event.cancel()  # ← ยกเลิกตัวเก่าก่อนเริ่มใหม่ทุกครั้ง

        self.current_time_sec = self.MAX_TIME
        self.timer_progress_value = 100
        self.countdown_display = f"{self.MAX_TIME:.0f} s"
        self.timer_event = Clock.schedule_interval(self.update_timer, 1/60)


    def update_timer(self, dt):
        if self.current_time_sec > 0:
            self.current_time_sec -= dt
            self.timer_progress_value = (self.current_time_sec / self.MAX_TIME) * 100
            self.image_x_pos = 1.0 - (self.current_time_sec / self.MAX_TIME)
            self.countdown_display = f"{max(0, self.current_time_sec):.0f} s"
        else:
            self.stop_timer(finished=True)

    def stop_timer(self, finished=False):
        if self.timer_event:
            self.timer_event.cancel()
        self.is_running = False
        self.timer_progress_value = 0
        self.countdown_display = f"{0} s"
        self.image_x_pos = 1.0

        if finished:
            self.show_time_up_dialog()

    def show_time_up_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                type="custom",
                md_bg_color=(1, 0.96, 0.9, 1),
                radius=[40, 40, 40, 40],

                content_cls=CuteTimeUpContent(),

                buttons=[
                    MDFillRoundFlatButton(
                        text="ถัดไป",
                        on_release=self.go_to_next_word,
                        md_bg_color=(1, 0.7, 0.8, 1),
                        text_color=(1, 1, 1, 1),
                        font_name="THSarabunNewBold",
                        font_size="24sp",
                        size_hint=(None, None),
                        size=("180dp", "60dp")
                        # ❌ ลบ elevation ออกแล้ว
                    ),
                ],
            )
        self.dialog.open()




    def update_score(self, new_score):
        step = 0
        def animate(dt):
            nonlocal step
            if step < new_score:
                step += 1
                self.ids.score_bar.value = step
            else:
                Clock.unschedule(animate)
        Clock.schedule_interval(animate, 0.02)

    def go_to_next_word(self, instance):

        if self.timer_event:
            self.timer_event.cancel()  # ← stop ก่อนเปลี่ยนคำ

        if self.current_time_sec > 0:
            self.score += 1

        self.current_word_index += 1
        self.update_word_ui()

        if self.current_word_index >= len(self.WORD_LIST):
            self.show_final_dialog()
        else:
            self.start_timer()  # ← ปลอดภัยแล้ว เพราะ timer ตัวเก่าถูกยกเลิกแล้ว

        if self.dialog:
            self.dialog.dismiss()


    def update_word_ui(self):
        if 0 <= self.current_word_index < len(self.WORD_LIST):
            data = self.WORD_LIST[self.current_word_index]
            self.image_source = data["img"]
            self.word_en = data["en"]
            self.word_cn = data["cn"]
            self.word_pinyin = data["pinyin"]
            self.countdown_display = f"{int(self.current_time_sec)} s"

        else:
            # เคลียร์ทุกอย่าง
            self.word_en = ""
            self.word_cn = ""
            self.word_pinyin = ""
            self.image_source = ""
            self.countdown_display = ""

            # ปิดพื้นหลัง/หน้าจอเกม
            self.game_over = True   # ไปใช้เป็นตัวเช็กใน kv

            # แสดง dialog คะแนนแบบโปร่งใส (หรือเอาออกไปเลย)
            self.show_final_dialog()


    def show_final_dialog(self):
        content = FinalResultsContent(final_score=self.score)
        
        final_dialog = MDDialog(
            type="custom",
            md_bg_color=(1, 0.96, 0.9, 1),  # สีพื้นหลังอ่อน
            radius=[40, 40, 40, 40],        # มุมโค้ง
            content_cls=content,
            buttons=[
                MDFillRoundFlatButton(
                    text="ตกลง",
                    on_release=lambda x: final_dialog.dismiss(),
                    md_bg_color=(1, 0.7, 0.51, 1),  # สีส้มพีช
                    text_color=(1, 1, 1, 1),
                    font_name="THSarabunNewBold",
                    font_size="28sp",
                    size_hint=(None, None),
                    size=("100dp", "50dp")
                ),
            ],
        )
        final_dialog.open()

    def close_final_dialog(self, dialog):
        # ลูกเล่น: ขยายปุ่มก่อนปิด
        btn = dialog.buttons[0]
        anim = Animation(scale=1.2, duration=0.15) + Animation(scale=1.0, duration=0.15)
        anim.bind(on_complete=lambda *args: dialog.dismiss())
        anim.start(btn)


class LanguageGameApp(MDApp):
    def build(self):
        LabelBase.register(
            name="THSarabunNewBold",
            fn_regular="fonts/THSarabunNew.ttf"  
        )
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Light"
        Builder.load_file('fruit.kv')
        return RootGameScreen()


if __name__ == '__main__':
    LanguageGameApp().run()
