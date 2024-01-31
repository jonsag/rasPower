#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import sys

from setup_apache import apache2_setup

def is_root():
    import os
    
    return os.geteuid() == 0

def install_rasPower():
    # check if root
    print("Checking if root...")
    if is_root() == 0:
        print("Must be run as root")
        sys.exit(1)
    else:
        import os, shutil
        
        print("Creating web site...")
        if os.path.isdir('/var/www/rasPower'):
            print("Web directory exists.")
            shutil.rmtree('/var/www/rasPower')

        shutil.copytree(os.path.join(os.getcwd(), 'www'), '/var/www/rasPower')
        if os.path.isfile(os.path.join(os.getcwd(), 'config.ini')):
            shutil.copy(os.path.join(os.getcwd(), 'config.ini'), '/var/www/rasPower/config.ini')
        else:
            print("No 'config.ini' found.\nPlease edit 'config.ini.template' and save as 'config.ini'.")
            sys.exit(2)

        print("Creating site config...")
        shutil.copy("rasPower.conf", "/etc/apache2/sites-available/rasPower.conf")
        
        from pwd import getpwnam
        from grp import getgrnam
        
        print("Changing ownership and setting scripts executable...")
        for dir_path, dirs, files in os.walk("/var/www/rasPower"):
            for dir in dirs:
                os.chown(os.path.join(dir_path, dir), getpwnam('www-data').pw_uid, getgrnam('www-data').gr_gid)
            for file in files:
                os.chown(os.path.join(dir_path, file), getpwnam('www-data').pw_uid, getgrnam('www-data').gr_gid)
                if os.path.join(dir_path, file).endswith('.py'):
                    os.chmod(os.path.join(dir_path, file), 0o755)
                    
        apache2_setup()

if __name__ == "__main__" : 
    install_rasPower()