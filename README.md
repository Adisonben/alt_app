### ALT kiosk application

# System requirement
- java 1.8.0_65
- libusb-0.1-4

# install java on pi5 arm 32 os
- [Download java sdk](https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html)
- `sudo tar -xvzf jdk-8u202-linux-arm64-vfp-hflt.tar.gz -C /usr/lib`
- `sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk1.8.0_202/bin/java 1`
- `sudo update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/jdk1.8.0_202/bin/javac 1`

# Install SecuGen sdk for pi5 arm32 os
- cd to 'FDx_SDK_PRO_LINUX_PI_armv7l_3_8_8/lib/pi'
- `sudo cp libpysgfplib.so.1.0.1.fdu05_rename libpysgfplib.so | sudo ldconfig` หรือ `sudo ln -sf libpysgfplib.so.1.0.1.fdu03_rename libpysgfplib.so`
- `sudo cd ../...make uninstall install`

# installation
1. ติดตั้ง dependency
    - `sudo apt install libcairo2-dev pkg-config python3-dev` dependency ของ KivyMD ต้องใช้ pycairo
    - `sudo apt install build-essential meson ninja-build cmake` build tools ช่วยลดปัญหา package compile
1. สร้าง Virtual Environment (venv) ` python -m venv venv ` or `python3 -m venv venv --system-site-packages` และ activate
    - Linux / macOS / Raspberry Pi	`source venv/bin/activate`
    - Windows cmd `venv\Scripts\activate.bat`
    - freeze lib `pip freeze > requirements.txt`

2. ติดตั้ง lib อื่น ๆ :  `pip install -r requirements.txt`

Note:
Also you can install manually from sources. Just clone the project and run pip:
- `git clone https://github.com/kivymd/KivyMD.git --depth 1`
- `cd KivyMD`
- `pip install .`