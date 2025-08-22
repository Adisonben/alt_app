### ALT kiosk application

# installation
1. สร้าง Virtual Environment (venv) ` python -m venv venv ` และ activate
    - Linux / macOS / Raspberry Pi	`source venv/bin/activate`
    - Windows cmd `venv\Scripts\activate.bat`
    - freeze lib `pip freeze > requirements.txt`

2. ติดตั้ง lib อื่น ๆ :  `pip install -r requirements.txt`


Note:
Also you can install manually from sources. Just clone the project and run pip:
- `git clone https://github.com/kivymd/KivyMD.git --depth 1`
- `cd KivyMD`
- `pip install`