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

Boot up the RPi, and connect via ssh.

### Prerequisites

#### Install Packages

>$ sudo apt install apache2 git mariadb-server python3-pip

#### Install Python modules

>$ sudo apt install python3-pymysql python3-getpass

OR if you want to use pip

>$ pip install PyMySQL pwinput

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
Select 'Y'

## Misc

### MySQL debugging

#### General Query Log

>$ sudo mkdir /var/log/mariadb
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
