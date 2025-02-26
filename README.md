# rasPower

Read electricity price and use it accordingly.

## Installation

### Operating system

Download Imager from [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/).
Also download Raspberry Pi OS Lite 64 bookworm from [https://www.raspberrypi.com/software/operating-systems/](https://www.raspberrypi.com/software/operating-systems/), and unpack it.

>$ unxz 2023-12-11-raspios-bookworm-arm64-lite.img.xz

Run Imager and choose the img file.
Enter your preferences, ie SSID, user name and password etc.
Also enable ssh.

#### raspi-config

Boot up the RPi, and connect via ssh.  

>$ sudo raspi-config  

Make your miscellaneous settings, eg. localization, keyboard etc.  
Expand disk  
Enable SPI  

#### Update

>$ sudo apt update && sudo apt upgrade  

### Prerequisites

#### Install Packages

>$ sudo apt install apache2 git mariadb-server  
>$ sudo apt install libfreetype6-dev libjpeg-dev build-essential libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev

#### Install Python modules

>$ sudo apt install python3-dev python3-pip  
>$ pip install --break-system-packages luma.lcd numpy openmeteo_requests pandas pwinput pymysql requests-cache retry_requests rpi.gpio spidev sqlparse suncalc willow pyarrow  

At the moment openmeteo_sdk doesn't install correctly  

>$ wget https://github.com/open-meteo/sdk/archive/refs/tags/v1.10.0.tar.gz -O 'openmeteo-sdk-1.10.0.tar.gz'  
>$ tar zxvf openmeteo-sdk-1.10.0.tar.gz  
>$ sudo cp -R sdk-1.10.0/python/openmeteo_sdk /usr/local/lib/python3.11/dist-packages/  

### MariaDB setup

>$ sudo mysql_secure_installation

    Enter current password for root (enter for none):
Press 'Enter'

    Switch to unix_socket authentication [Y/n]
Select 'Y'

    Change the root password? [Y/n]
Select 'Y'

    New password:
Enter your new password twice

    Remove anonymous users? [Y/n]
Select 'Y'

    Disallow root login remotely? [Y/n]
Select 'Y'

    Remove test database and access to it? [Y/n]
Select 'Y'

    Reload privilege tables now? [Y/n]
Select 'Y'$ sudo apt install python3-dev python3-pip python3-numpy libfreetype6-dev libjpeg-dev build-essential
$ sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev

### Software

>$ git clone https://github.com/jonsag/rasPower.git  
>$ cd rasPower  
>$ python setup_db.py
>$ sudo ./install.py  

### Hardware

>$ sudo usermod -a -G i2c,spi,gpio www-data  

#### ST7735 OLED Screen

| Screen | Pin | GPIO   |
| ------ | --- | ------ |
| GND    | 6   | Ground |
| VCC    | 2   | +5V    |
| SCL    | 23  | 11     |
| SDA    | 19  | 10     |
| RES    | 18  | 24     |
| DC     | 16  | 23     |
| CS     | 24  | 8      |
| BL     | 12  | 18     |

#### ILI9341 TFT Touch Screen

| Screen          | Pin | GPIO  |      |
| --------------- | --- | ----- | ---- |
| VCC             | 1   | +3.3V |      |
| GND             | 6   | GND   |      |
| CS              | 24  | 8     | CE0  |
| RESET           | 18  | 24    |      |
| DC (A0)         | 22  | 25    |      |
| DSI (MOSI, SDA) | 19  | 10    | MOSI |
| SCK             | 23  | 11    | SCLK |
| LED             | 12  | 18    | BL   |
| SDO (MISO)      | NC  |       |      |

| Touch | Pin | GPIO |
| ----- | --- | ---- |
| T_CLK |     |      |
| T_CS  |     |      |
| T_DIN |     |      |
| T_DO  |     |      |
| T_IRQ |     |      |

>$ sudo pip install adafruit-circuitpython-rgb-display pillow  
>$ sudo apt install fonts-dejavu libopenjp2-7 libtiff6 libatlas-base-dev  

## Misc

### MySQL debugging

#### General Query Log

>$ sudo mkdir /var/log/mariadbsudo -H pip install -e .
>$ sudo touch /var/log/mariadb/general-query.log
>$ sudo chown mysql:mysql -R /var/log/mariadb
>MariaDB []> SET GLOBAL general_log_file /var/log/mysql/general-query.log;

Turn on General Query Log
>MariaDB []> SET GLOBAL general_log=1;

Turn off General Query Log
>MariaDB []> SET GLOBAL general_log=0;

Check values
>MariaDB []> SHOW VARIABLES LIKE "general_log%";

Read General Query Log
>$ tail -f /var/log/mysql/general-query.log

#### Error Log

View error log with journal
>$ journalctl -u mariadb.service

Check error log location
>MariaDB []> SHOW VARIABLES LIKE "log_error%";

Write error log to file
>$ sudo touch /var/log/mariadb/error.log
>$ sudo chown mysql:mysql -R /var/log/mariadb
>MariaDB []> SET GLOBAL log_error /var/log/mysql/error.log;

## Links

### ILI9341

* [https://github.com/ilbertt/XPT2046-Python](https://github.com/ilbertt/XPT2046-Python)
* [https://github.com/Georodin/xpt2046-touchcontroller-py](https://github.com/Georodin/xpt2046-touchcontroller-py)
* [https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display](https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display)
* [https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/python-wiring-and-setup](https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/python-wiring-and-setup)  

### Luma Core

* [https://luma-lcd.readthedocs.io/en/latest/intro.html](https://luma-lcd.readthedocs.io/en/latest/intro.html)

## My shortcuts

>$ rs-copy www/* jon@192.168.68.163:/var/www/rasPower  
>$ ssh jon@192.168.68.163 "sudo chmod g+w /var/www/rasPower/ -R"  
>$ ssh jon@192.168.68.163 "sudo usermod -a -G jon www-data"  

>$ rs-copy www/* jon@192.168.68.163:/var/www/rasPower  && ssh jon@192.168.68.163 "sudo chmod g+w /var/www/rasPower/ -R" && ssh jon@192.168.68.163 "sudo usermod -a -G jon www-data"  
