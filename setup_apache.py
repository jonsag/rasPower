#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which(name) is not None

def is_root():
    import os
    
    return os.geteuid() == 0

def apache2_setup():
    import sys
    
    # check if root
    print("Checking if root...")
    if is_root() == 0:
        print("Must be run as root")
        sys.exit(0)
    else:
        print("Checking if apache2 is installed...")
        if is_tool("apache2") == 0:
            print("Please install apache2")
            sys.exit(0)
        else:
            import os
            
            if os.path.isdir('/var/www/rasPower'):
                print("Web directory exists")
            else:
                print("Creating web directory...")
                os.mkdir("/var/www/rasPower") 

            import shutil

            print("Creating site config...")
            shutil.copy("rasPower.conf", "/etc/apache2/sites-available/rasPower.conf")
            
            import re
            
            print("Checking for listening directive...")
            pattern8080 = re.compile("Listen 8080($|\ )")
            pattern80 = re.compile("Listen 80($|\ )")
            with open("/etc/apache2/ports.conf", "r+") as file:
                for line in file:
                    if pattern8080.match(line):
                        print("Already listening to port 8080")
                        break
                else: # not found, we are at the eof
                    print("Adding directive...")#file.write(needle) # append missing data
                    with open("/etc/apache2/ports.conf", "r") as in_file:
                        buf = in_file.readlines()

                    with open("/etc/apache2/ports.conf", "w") as out_file:
                        for line in buf:
                            if pattern80.match(line):
                                line = line + "Listen 8080\n"
                            out_file.write(line)
        
            import subprocess
            
            print("Enabling site...")
            subprocess.run(["a2ensite", "rasPower.conf"])
            
            print("Disabling mpm_event...")
            subprocess.run(["a2dismod", "mpm_event"])
        
            print("Enabling mpm_prefork and cgi...")
            subprocess.run(["a2enmod", "mpm_prefork", "cgi"])
            
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
                        
            print("Restarting apache2...")
            subprocess.run(["systemctl", "restart", "apache2"])
                           
if __name__ == "__main__" : 
    apache2_setup()