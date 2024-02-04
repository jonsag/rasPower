#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import sys

import re

import subprocess


def apache2_setup():

    print("Checking for listening directive...")

    pattern8080 = re.compile("Listen 8080($|\ )")
    pattern80 = re.compile("Listen 80($|\ )")

    with open("/etc/apache2/ports.conf", "r+") as file:
        for line in file:
            if pattern8080.match(line):
                print("Already listening to port 8080")
                break
        else:  # not found, we are at the eof
            # file.write(needle) # append missing data
            print("Adding directive...")
            with open("/etc/apache2/ports.conf", "r") as in_file:
                buf = in_file.readlines()

            with open("/etc/apache2/ports.conf", "w") as out_file:
                for line in buf:
                    if pattern80.match(line):
                        line = line + "Listen 8080\n"
                    out_file.write(line)

    print("Enabling site...")
    subprocess.run(["a2ensite", "rasPower.conf"])

    print("Disabling mpm_event...")
    subprocess.run(["a2dismod", "mpm_event"])

    print("Enabling mpm_prefork and cgi...")
    subprocess.run(["a2enmod", "mpm_prefork", "cgi"])

    print("Restarting apache2...")
    subprocess.run(["systemctl", "restart", "apache2"])


if __name__ == "__main__":
    apache2_setup()
