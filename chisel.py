#
# Chisel Reverse tunnel Configuration Script
# Author: github.com/Azumi67
# This is for educational use and my own learning, please provide me with feedback if possible
# There maybe some erros , please forgive me as i have worked on it while i was studying.
# This script is designed to simplify the configuration of Chisel Tunnel.
#
# Supported operating systems: Ubuntu 20, Debian 12
## I use the same imports and other stuff to speed up in creating the script
# you should only install colorama & netifaces
# Usage:
#   Run the script with root privileges.
#   Follow the on-screen prompts to install, configure, or uninstall the tunnel.
#
#
# Disclaimer:
# This script comes with no warranties or guarantees. Use it at your own risk.
import sys
import os
import time
import colorama
from colorama import Fore, Style
import subprocess
from time import sleep
import readline
import random
import string
import shutil
import netifaces as ni
import urllib.request
import zipfile


if os.geteuid() != 0:
    print("\033[91mThis script must be run as root. Please use sudo -i.\033[0m")
    sys.exit(1)


def display_progress(total, current):
    width = 40
    percentage = current * 100 // total
    completed = width * current // total
    remaining = width - completed

    print('\r[' + '=' * completed + '>' + ' ' * remaining + '] %d%%' % percentage, end='')


def display_checkmark(message):
    print('\u2714 ' + message)


def display_error(message):
    print('\u2718 Error: ' + message)


def display_notification(message):
    print('\u2728 ' + message)


def display_loading():
    duration = 3
    end_time = time.time() + duration
    ball_width = 10
    ball_position = 0
    ball_direction = 1

    while time.time() < end_time:
        sys.stdout.write('\r\033[93mLoading, Please wait... [' + ' ' * ball_position + 'o' + ' ' * (ball_width - ball_position - 1) + ']')
        sys.stdout.flush()

        if ball_position == 0:
            ball_direction = 1
        elif ball_position == ball_width - 1:
            ball_direction = -1

        ball_position += ball_direction
        time.sleep(0.1)
    
    sys.stdout.write('\r' + ' ' * (len('Loading, Please wait...') + ball_width + 4) + '\r')
    sys.stdout.flush()
    display_notification("\033[96mIt might take a while...\033[0m")

    
def display_logo2():
    colorama.init()
    logo2 = colorama.Style.BRIGHT + colorama.Fore.GREEN + """
     _____       _     _      
    / ____|     (_)   | |     
   | |  __ _   _ _  __| | ___ 
   | | |_ | | | | |/ _` |/ _ \\
   | |__| | |_| | | (_| |  __/
    \_____|\__,_|_|\__,_|\___|
""" + colorama.Style.RESET_ALL
    print(logo2)
    
def display_logo():
    colorama.init()  
    logo = """ 
\033[1;96m
                  ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣯⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⣿⣿
                ⢺⣽⡿⣅⠹⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⡻⣿⣻⣿⣿⣿⣁⣴⢟⡻⠻⣯⣌⣿
          ⠔⢫⠆⣾⡿⢷⣮⣥⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠯⠝⠛⠉⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⣏⣀⣙⡄⢿⣿⣿⣿⣿⣿⣿⣿⢟
       ⢀⠳⢒⣷⣿⣿⢱⡂⠜⣿⣿⣿⣿⣿⣿⣿⡿⢛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡱⠟⢀⡇⠸⣶⣿
       ⠈⢩⣣⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⠏⡰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢻⣿⣭⡽⠟⠫⠅⣿⡿⢶⣿⠿⣻⣿⣿⣿⣿
         ⢠⣿⣿⣿⣿⣿⣉⠻⣿⣿⣿⣿⢏⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢤⠢⣀⣀⠤⢞⢟⣟⣒⣣⠼⡯⡟⢻⡥⡒⠘⣿
        ⢠⠋⣴⡿⡿⣿⡔⠻⣿⣿⣿⣿⣏⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡀⣆⣐⣥⣴⣾⣿⣿⣿⣶⠊⣼⣀⣸⣧⣿⣿⣿⣽
       ⣠⣿⣾⡟⣤⣇⠘⣿⣷⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠄⢻⣿⣿⣿⣿⣿⣿⣽⣻⣿⣿⣿⣿⢿⡍⢻⣿⣿⡇
      ⣰⠏⣾⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⠃⠀⣀⠠⠤⠐⠒⠒⠓⠒⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠐⠒⠒⠒⠤⠤⣀⠀⠘⣿⣿⣿⣿⣿⣿⣷⡟⢰⡿⠻⣟⡚⠻⣷⣿
     ⣰⠃⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠔⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⢿⣿⣿⣿⣿⣿⢙⢲⡞⢀⡄⠈⡗⣲⣾⣿⣿⡟⠁
⠀   ⢠⠇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\033[1;96m⠀⠀⠀⠀⣀⣀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣾⣿⣷⣯⣼⣿⣿⣿⣿⣿⣿⣿⠀
   ⢀⡎⠀⠀⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏\033[1;91m⡀⠀⣎⣁⣤⣼⣖⣶⣦⣬⣑⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠖⣈⣭⣤⣴⣮⣭⣴⡦\033[1;96m⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⠿
⠀  ⡼⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇\033[1;91m⢧⣤⣾⡿⣿⣿⣿⣿⣯⣽⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⣰⣾⢿⣿⣿⣿⣿⣙\033[1;96m⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡱⣎⡟⠀
  ⢰⠇⠀⠀⢸⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\033[1;91m⡠⣾⣿⠟⠀⣿⣿⠛⢽⣿⡿⢿⣿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠋⠧⣾⣿⡟⠻ ⣿⣿\033[1;96m⢿⣿⡟⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣾⣾⣿
⠀⠀⣿⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆\033[1;91m⠀⠙⠆⠀⠙⡘⠢⡘⠿⢃⡞⡾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣫⠳⡙⢿⠃⡚⣻\033[1;96m⢻⣿⣿⣿⣿⠴⠐⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⢸⡇⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢺⡄\033[1;91m⠀⠀⢢⡀⠙⠢⢀⣀⠡⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠦⣄⣀⣁⠮⠃\033[1;96m⣸⣏⣺⣿⣿⠹⡎⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⣼⡇⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠣⣷⠀\033[1;91m⠀⠉⠙⠛⠦⠲⠒⠂⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠲⠦⠴⠶⠶⠊\033[1;96m⣿⠇⣼⣿⣿⡩⢛⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⣿⡇⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡘⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠀⣿⣿⡏⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢞⣿⠀\033[1;92mAuthor: github.com/Azumi67  \033[1;96m  ⠀⠀⠀⠀
  \033[96m  ______   \033[1;94m _______  \033[1;92m __    \033[1;93m  _______     \033[1;91m    __      \033[1;96m  _____  ___  
 \033[96m  /    " \  \033[1;94m|   __ "\ \033[1;92m|" \  \033[1;93m  /"      \    \033[1;91m   /""\     \033[1;96m (\"   \|"  \ 
 \033[96m // ____  \ \033[1;94m(. |__) :)\033[1;92m||  |  \033[1;93m|:        |   \033[1;91m  /    \   \033[1;96m  |.\\   \    |
 \033[96m/  /    ) :)\033[1;94m|:  ____/ \033[1;92m|:  |  \033[1;93m|_____/   )   \033[1;91m /' /\  \   \033[1;96m |: \.   \\  |
\033[96m(: (____/ // \033[1;94m(|  /     \033[1;92m|.  | \033[1;93m //       /   \033[1;91m //  __'  \  \033[1;96m |.  \    \ |
 \033[96m\        / \033[1;94m/|__/ \   \033[1;92m/\  |\ \033[1;93m |:  __   \  \033[1;91m /   /  \\   \ \033[1;96m |    \    \|
 \033[96m \"_____ / \033[1;94m(_______) \033[1;92m(__\_|_)\033[1;93m |__|  \___) \033[1;91m(___/    \___) \033[1;96m\___|\____\)
"""
    print(logo)
def main_menu():
    try:
        while True:
            display_logo()
            border = "\033[93m+" + "="*70 + "+\033[0m"
            content = "\033[93m║            ▌║█║▌│║▌│║▌║▌█║ \033[92mMain Menu\033[93m  ▌│║▌║▌│║║▌█║▌                  ║"
            footer = " \033[92m            Join Opiran Telegram \033[34m@https://t.me/OPIranClub\033[0m "

            border_length = len(border) - 2
            centered_content = content.center(border_length)

            print(border)
            print(centered_content)
            print(border)
            

            print(border)
            print(footer)
            print(border)
            print("0. \033[92mStatus Menu\033[0m")
            print("15.\033[94mStop | Restart Service \033[0m")
            print("16.\033[91mUninstall\033[0m")
            print("\033[93m─────────────────────────────────────────── \033[0m")
            display_notification("\033[93mSingle Server\033[0m")
            print("\033[93m─────────────────────────────────────────── \033[0m")
            print("1. \033[96mChisel \033[92mTCP \033[96m[IPV4]\033[0m")
            print("2. \033[96mChisel \033[92mUDP \033[96m[IPV4]\033[0m") 
           
            print("3. \033[93mChisel \033[92mTCP\033[93m [IPV6]\033[0m")            
            print("4. \033[93mChisel \033[92mUDP\033[93m [IPV6]\033[0m")
            print(border)
            print("\033[93m─────────────────────────────────────────── \033[0m")
            display_notification("\033[92m[5] \033[96mKharej \033[92m[1] \033[93mIRAN\033[0m")
            print("\033[93m─────────────────────────────────────────── \033[0m")
            print("5. \033[96mChisel \033[92mTCP \033[96m[IPV4] \033[92m[5] \033[96mKHAREJ\033[92m [1] \033[96mIRAN")
            print("\033[97m6. \033[96mChisel \033[92mUDP \033[96m[IPV4] \033[92m[5] \033[96mKHAREJ\033[92m [1] \033[96mIRAN")
            
            print("\033[97m7. \033[93mChisel \033[92mTCP \033[93m[IPV6] \033[92m[5] \033[93mKHAREJ\033[92m [1] \033[93mIRAN")
            print("\033[97m8. \033[93mChisel \033[92mUDP \033[93m[IPV6] \033[92m[5] \033[93mKHAREJ\033[92m [1] \033[93mIRAN")
            print(border)
            
            display_notification("\033[92m[5] \033[96mIRAN \033[92m[1] \033[93mKharej\033[0m")
            print("\033[93m─────────────────────────────────────────── \033[0m")
            print("\033[97m9. \033[96mChisel \033[92mTCP \033[96m[IPV4] \033[92m[5] \033[96mIRAN\033[92m [1] \033[96mKHAREJ\033[0m")
            print("\033[97m10.\033[96mChisel \033[92mUDP \033[96m[IPV4] \033[92m[5] \033[96mIRAN\033[92m [1] \033[96mKHAREJ\033[0m")  
            
            print("\033[97m11.\033[93mChisel \033[92mTCP \033[93m[IPV6] \033[92m[5] \033[93mIRAN\033[92m [1] \033[93mKHAREJ\033[0m")
            print("\033[97m12.\033[93mChisel \033[92mUDP \033[93m[IPV6] \033[92m[5] \033[93mIRAN\033[92m [1] \033[93mKHAREJ\033[0m")
            print(border)
            print("\033[93m─────────────────────────────────────────── \033[0m")
            display_notification("\033[92mPrivate IP \033[0m")
            print("\033[93m─────────────────────────────────────────── \033[0m")
            print("13.\033[96mChisel \033[92mTCP\033[96m [Private IP]\033[0m")
            print("14.\033[93mChisel \033[92mUDP\033[93m [Private IP]\033[0m")
           
            print("q. Exit")
            print("\033[93m╰─────────────────────────────────────────────────────────────────────╯\033[0m")

            choice = input("\033[5mEnter your choice Please: \033[0m")
            
            if choice == '0':
                chisel_status()
            elif choice == '1':
                chisel_tcp_ip4()
            elif choice == '2':
                chisel_udp_ip4()
            elif choice == '3':
                chisel_tcp_ip6()
            elif choice == '4':
                chisel_udp_ip6()
            elif choice == '5':
                kharej5_t()
            elif choice == '6':
                kharej5_u()
            elif choice == '7':
                kharej5_t6()
            elif choice == '8':
                kharej5_u6()
            elif choice == '9':
                iran5_t()
            elif choice == '10':
                iran5_u()
            elif choice == '11':
                iran5_t6()
            elif choice == '12':
                iran5_u6()
            elif choice == '13':
                chisel_pri_tcp()
            elif choice == '14':
                chisel_pri_udp()
            elif choice == '15':
                start_serv()
            elif choice == '16':
                uni_menu() 
            elif choice == 'q':
                print("Exiting...")
                break
            else:
                print("Invalid choice.")

            input("Press Enter to continue...")

    except KeyboardInterrupt:
        display_error("\033[91m\nProgram interrupted. Exiting...\033[0m")
        sys.exit()
 

        
def kharej5_t():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[96mKharej \033[93mIPV4 \033[92mTCP\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('1. \033[93mKharej\033[92m [1] \033[0m')
    print('2. \033[93mKharej\033[92m [2] \033[0m')
    print('3. \033[93mKharej\033[92m [3] \033[0m')
    print('4. \033[93mKharej\033[92m [4] \033[0m')
    print('5. \033[93mKharej\033[92m [5] \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('6. \033[96mIRAN \033[0m')
    print('0. \033[92mBack to main menu \033[0m')

    print("\033[93m───────────────────────────────────────\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipv4()
            break
        elif server_type == '2':
            kharej_ipv4()
            break
        elif server_type == '3':
            kharej_ipv4()
        elif server_type == '4':
            kharej_ipv4()
            break
        elif server_type == '5':
            kharej_ipv4()
            break
        elif server_type == '6':
            iran_ipv4()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.') 

def kharej5_t6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[96mKharej \033[93mIPV6 \033[92mTCP\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('1. \033[93mKharej\033[92m [1] \033[0m')
    print('2. \033[93mKharej\033[92m [2] \033[0m')
    print('3. \033[93mKharej\033[92m [3] \033[0m')
    print('4. \033[93mKharej\033[92m [4] \033[0m')
    print('5. \033[93mKharej\033[92m [5] \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('6. \033[96mIRAN \033[0m')
    print('0. \033[92mBack to main menu \033[0m')

    print("\033[93m───────────────────────────────────────\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipv6()
            break
        elif server_type == '2':
            kharej_ipv6()
            break
        elif server_type == '3':
            kharej_ipv6()
        elif server_type == '4':
            kharej_ipv6()
            break
        elif server_type == '5':
            kharej_ipv6()
            break
        elif server_type == '6':
            iran_ipv6()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.') 

def kharej5_u():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[96mKharej \033[93mIPV4 \033[92mUDP\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('1. \033[93mKharej\033[92m [1] \033[0m')
    print('2. \033[93mKharej\033[92m [2] \033[0m')
    print('3. \033[93mKharej\033[92m [3] \033[0m')
    print('4. \033[93mKharej\033[92m [4] \033[0m')
    print('5. \033[93mKharej\033[92m [5] \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('6. \033[96mIRAN \033[0m')
    print('0. \033[92mBack to main menu \033[0m')

    print("\033[93m───────────────────────────────────────\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipv4_udp()
            break
        elif server_type == '2':
            kharej_ipv4_udp()
            break
        elif server_type == '3':
            kharej_ipv4_udp()
            break
        elif server_type == '4':
            kharej_ipv4_udp()
            break
        elif server_type == '5':
            kharej_ipv4_udp()
            break
        elif server_type == '6':
            iran_ipv4_udp()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.') 

def kharej5_u6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[96mKharej \033[93mIPV6 \033[92mUDP\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('1. \033[93mKharej\033[92m [1] \033[0m')
    print('2. \033[93mKharej\033[92m [2] \033[0m')
    print('3. \033[93mKharej\033[92m [3] \033[0m')
    print('4. \033[93mKharej\033[92m [4] \033[0m')
    print('5. \033[93mKharej\033[92m [5] \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('6. \033[96mIRAN \033[0m')
    print('0. \033[92mBack to main menu \033[0m')

    print("\033[93m───────────────────────────────────────\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipv6_udp()
            break
        elif server_type == '2':
            kharej_ipv6_udp()
            break
        elif server_type == '3':
            kharej_ipv6_udp()
            break
        elif server_type == '4':
            kharej_ipv6_udp()
            break
        elif server_type == '5':
            kharej_ipv6_udp()
            break
        elif server_type == '6':
            iran_ipv6_udp()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')
            
def iran5_t():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[96mIRAN \033[93mIPV4 \033[92mTCP\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('1. \033[93mIRAN\033[92m[1] \033[0m')
    print('2. \033[93mIRAN\033[92m[2] \033[0m')
    print('3. \033[93mIRAN\033[92m[3] \033[0m')
    print('4. \033[93mIRAN\033[92m[4] \033[0m')
    print('5. \033[93mIRAN\033[92m[5] \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('6. \033[96mKharej \033[0m')
    print('0. \033[92mBack to main menu \033[0m')

    print("\033[93m───────────────────────────────────────\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            iran_ipv4()
            break
        elif server_type == '2':
            iran_ipv4()
            break
        elif server_type == '3':
            iran_ipv4()
        elif server_type == '4':
            iran_ipv4()
            break
        elif server_type == '5':
            iran_ipv4()
            break
        elif server_type == '6':
            config_kharej()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.') 

def iran5_t6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[96mIRAN \033[93mIPV6 \033[92mTCP\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('1. \033[93mIRAN\033[92m[1] \033[0m')
    print('2. \033[93mIRAN\033[92m[2] \033[0m')
    print('3. \033[93mIRAN\033[92m[3] \033[0m')
    print('4. \033[93mIRAN\033[92m[4] \033[0m')
    print('5. \033[93mIRAN\033[92m[5] \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('6. \033[96mKharej \033[0m')
    print('0. \033[92mBack to main menu \033[0m')

    print("\033[93m───────────────────────────────────────\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            iran_ipv6()
            break
        elif server_type == '2':
            iran_ipv6()
            break
        elif server_type == '3':
            iran_ipv6()
        elif server_type == '4':
            iran_ipv6()
            break
        elif server_type == '5':
            iran_ipv6()
            break
        elif server_type == '6':
            config_kharej6()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.') 

def iran5_u():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[96mIRAN IPV4 \033[92mUDP\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('1. \033[93mIRAN\033[92m[1] \033[0m')
    print('2. \033[93mIRAN\033[92m[2] \033[0m')
    print('3. \033[93mIRAN\033[92m[3] \033[0m')
    print('4. \033[93mIRAN\033[92m[4] \033[0m')
    print('5. \033[93mIRAN\033[92m[5] \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('6. \033[96mKharej \033[0m')
    print('0. \033[92mBack to previous menu \033[0m')

    print("\033[93m───────────────────────────────────────\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            iran_ipv4_udp()
            break
        elif server_type == '2':
            iran_ipv4_udp()
            break
        elif server_type == '3':
            iran_ipv4_udp()
        elif server_type == '4':
            iran_ipv4_udp()
            break
        elif server_type == '5':
            iran_ipv4_udp()
            break
        elif server_type == '6':
            config_kha_udp()
            break
        elif server_type == '0':
            os.system("clear")
            iran5_menu()
            break
        else:
            print('Invalid choice.') 

def iran5_u6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[96mIRAN IPV6 \033[92mUDP\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('1. \033[93mIRAN\033[92m[1] \033[0m')
    print('2. \033[93mIRAN\033[92m[2] \033[0m')
    print('3. \033[93mIRAN\033[92m[3] \033[0m')
    print('4. \033[93mIRAN\033[92m[4] \033[0m')
    print('5. \033[93mIRAN\033[92m[5] \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('6. \033[96mKharej \033[0m')
    print('0. \033[92mBack to previous menu \033[0m')

    print("\033[93m───────────────────────────────────────\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            iran_ipv6_udp()
            break
        elif server_type == '2':
            iran_ipv6_udp()
            break
        elif server_type == '3':
            iran_ipv6_udp()
        elif server_type == '4':
            iran_ipv6_udp()
            break
        elif server_type == '5':
            iran_ipv6_udp()
            break
        elif server_type == '6':
            config_ud6()
            break
        elif server_type == '0':
            os.system("clear")
            iran5_menu()
            break
        else:
            print('Invalid choice.')     

            
 


        
def chisel_tcp_ip4():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Chisel \033[92mTCP\033[96m IPV4\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ \033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipv4()
            break
        elif server_type == '2':
            iran_ipv4()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')      

def chisel_udp_ip4():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Chisel \033[92mUDP\033[96m IPV4\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ \033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipv4_udp()
            break
        elif server_type == '2':
            iran_ipv4_udp()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')                 

def chisel_tcp_ip6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Chisel \033[92mTCP\033[96m IPV6\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ \033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipv6()
            break
        elif server_type == '2':
            iran_ipv6()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')   
            
def chisel_udp_ip6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Chisel \033[92mUDP\033[96m IPV6\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ \033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipv6_udp()
            break
        elif server_type == '2':
            iran_ipv6_udp()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')  

def chisel_pri_tcp():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Chisel \033[92mTCP\033[96m PrivateIP\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ \033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            khpri_ipv6()
            break
        elif server_type == '2':
            irpri_ipv6()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')  
            
def chisel_pri_udp():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Chisel \033[92mUDP\033[96m PrivateIP\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ \033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            khpri_ipv6_udp()
            break
        elif server_type == '2':
            irpri_ipv6_udp()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.') 
            
def forward():

    ipv4_forward_status = subprocess.run(["sysctl", "net.ipv4.ip_forward"], capture_output=True, text=True)
    if "net.ipv4.ip_forward = 0" not in ipv4_forward_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv4.ip_forward=1"])

    ipv6_forward_status = subprocess.run(["sysctl", "net.ipv6.conf.all.forwarding"], capture_output=True, text=True)
    if "net.ipv6.conf.all.forwarding = 0" not in ipv6_forward_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv6.conf.all.forwarding=1"])

    
def chisel_mnu():
    def stop_loading():
        display_error("\033[91mInstallation process interrupted..\033[0m")
        exit(1)
    display_loading()

    arch = subprocess.check_output('uname -m', shell=True).decode().strip()

    if arch in ['x86_64', 'amd64']:
        chisel_download_url = "https://github.com/jpillora/chisel/releases/download/v1.9.1/chisel_1.9.1_linux_amd64.gz"
        chisel_directory_name = "chisel"
    elif arch in ['aarch64', 'arm64']:
        chisel_download_url = "https://github.com/jpillora/chisel/releases/download/v1.9.1/chisel_1.9.1_linux_arm64.gz"
        chisel_directory_name = "chisel"
    else:
        display_error("\033[91mUnsupported CPU architecture: {}\033[0m".format(arch))
        return

    display_notification("\033[93mDownloading Chisel...\033[0m")
    download_result = subprocess.run(f"wget {chisel_download_url} -O {chisel_directory_name}.gz > /dev/null 2>&1", shell=True)
    if download_result.returncode != 0:
        display_error("\033[91mChisel download failed.\033[0m")
        return

    gunzip_result = subprocess.run(f"gunzip {chisel_directory_name}.gz", shell=True)
    if gunzip_result.returncode != 0:
        display_error("\033[91mFailed to extract !!\033[0m")
        return

    try:
        os.rename(chisel_directory_name, "chisel")
        subprocess.run(f"chmod +x chisel", shell=True)
    except Exception as e:
        display_error("\033[91mError occurred during Chisel installation !!: {}\033[0m".format(str(e)))
        return

    display_checkmark("\033[92mDownload Completed!\033[0m")
    
def chisel_key(key_path):
    keygen_command = f"./chisel server --keygen {key_path}"
    try:
        subprocess.run(keygen_command, shell=True, check=True)
        display_notification("\033[93mChisel key generated at {}\033[0m".format(key_path))

    except subprocess.CalledProcessError as e:
        display_notification("\033[91mFailed to generate key. Error: {}\033[0m".format(e.output))

def iran_tcp(host, key_path, port=443):
    service_name = "iran_1"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel server --keyfile {key_path} --reverse --port {port} --host {host} --keepalive 25s"

    service_content = f"""[Unit]
Description=Chisel Service IRAN
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(f"systemctl start {service_name}", shell=True, check=True)

        display_checkmark("\033[92mIRAN service started successfully!\033[0m")

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating IRAN service. Error: {}\033[0m".format(e.output))
      

def iran_ipv4():
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()
    forward()
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mIRAN\033[0m")
    print("\033[93m───────────────────────────\033[0m")

    key_directory = "/etc/chisel"
    try:
        if os.path.exists(key_directory):
            try:
                shutil.rmtree(key_directory)  
            except NotADirectoryError:
                os.remove(key_directory)  
    except Exception as e:
       display_error("An error occurred while removing: {}".format(str(e)))

    host = input("\033[93mEnter \033[92mIRAN\033[96m IPV4\033[93m address: \033[0m")
    port = input("\033[93mEnter  \033[92mTunnel Port \033[93m (default 443): \033[0m") or '443'

    try:
        os.makedirs(key_directory, exist_ok=True) 
        print("\033[93m────────────────────────\033[0m")        

        key_path = f"{key_directory}/chisel_key_1.key"

        chisel_key(key_path)
        iran_tcp(host, key_path, int(port))
    except Exception as e:
         display_error("An error occurred: {}".format(str(e)))

def kharej_tc(server_number, config_number, iran_ipv4, kharej_port, df_port=443):
    service_name = f"kharej_{server_number}_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 25s {iran_ipv4}:{df_port} R:localhost:{kharej_port}"

    service_content = f"""[Unit]
Description=Kharej Service {config_number} (Server {server_number})
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(f"systemctl start {service_name}", shell=True, check=True)
        display_checkmark(f"\033[92mKharej service {config_number} (Server {server_number}) started successfully!\033[0m")

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error(f"\033[91mFailed in creating Kharej service {config_number} (Server {server_number}). Error: {e.output}\033[0m")

def config_kharej():
    def kharej_ipv4(num_servers):
        if not os.path.isfile("/root/chisel"):
            chisel_mnu()
        forward()
        print("\033[93m───────────────────────────\033[0m")
        display_notification("\033[93mConfiguring \033[96mKHAREJ\033[0m")
        print("\033[93m───────────────────────────\033[0m")
        server_configs = []

        for i in range(1, num_servers + 1):
            print("\033[93m────────────────────────\033[0m") 
            print("\033[92m    --- Config {} ---\033[0m".format(i))
            print("\033[93m────────────────────────\033[0m")
            iran_ipv4 = input("\033[93mEnter \033[92mIRAN Server {} \033[96mIPV4\033[93m address: \033[0m".format(i))
            num_configs = int(input("\033[93mEnter the \033[93mnumber \033[93mof \033[96mKharej configs: \033[0m".format(i)))
            
            configs = []
            for j in range(1, num_configs + 1):
                kharej_port = input("\033[93mEnter \033[96mKharej \033[92mConfig {} port\033[93m: \033[0m".format(j))
                df_port = input("\033[93mEnter \033[96mTunnel Port\033[93m (default 443): \033[0m") or '443'
                configs.append((kharej_port, df_port))

            server_configs.append((iran_ipv4, configs))

            for j, (kharej_port, df_port) in enumerate(configs, start=1):
                kharej_tc(i, j, iran_ipv4, int(kharej_port), int(df_port))

            print("\033[93m╭──────────────────────────────────────────────────────────────────────╮\033[0m")
            for j, (kharej_port, df_port) in enumerate(configs, start=1):
                print(f"\033[93m| Server {i} - Config {j}: Your Address & Port: {iran_ipv4} : {kharej_port}  \033[0m")
            print("\033[93m╰──────────────────────────────────────────────────────────────────────╯\033[0m")

        return server_configs

    num_iran_servers = int(input("\033[93mEnter the number of \033[92mIRAN\033[93m servers:\033[0m "))
    if num_iran_servers > 0:
        kharej_ipv4(num_iran_servers)
    else:
        print("\033[91mNo Iran servers, so I'm giving up..\033[0m")
        
def kharej_tcp(config_number, iran_ipv4, kharej_port, tunnel_port=443):
    service_name = f"kharej_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 25s {iran_ipv4}:{tunnel_port} R:localhost:{kharej_port}"

    service_content = f"""[Unit]
Description=Kharej Service {config_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(f"systemctl start {service_name}", shell=True, check=True)

        display_checkmark("\033[92mKharej service {} started successfully!\033[0m".format(config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating Kharej service {}. Error: {}\033[0m".format(config_number, e.output))
        

        
def kharej_ipv4():
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()
    forward()
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mKHAREJ\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mKharej\033[93m Configs: \033[0m"))
    iran_ipv4 = input("\033[93mEnter \033[92mIRAN\033[96m IPV4\033[93m address: \033[0m")
    tunnel_port = input("\033[93mEnter \033[92mTunnel port\033[93m (default: 443): \033[0m") or "443"
    server_ports = []

    for i in range(1, num_configs + 1):
        print("\033[93m────────────────────────\033[0m") 
        print("\033[92m    --- Config {} ---\033[0m".format(i))
        print("\033[93m────────────────────────\033[0m")
        kharej_port = input("\033[93mEnter Kharej \033[92mConfig port\033[93m: \033[0m")
        server_ports.append(kharej_port)

        kharej_tcp(i, iran_ipv4, kharej_port, tunnel_port)

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    for i in range(num_configs):
        print(f"\033[93m| Config {i+1} - Your Address & Port: {iran_ipv4} : {server_ports[i]}  \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    return server_ports
        
def iran_tcp2(host, key_path, tunnel_port=443):
    service_name = "iran_1"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel server --keyfile {key_path} --reverse --port {tunnel_port} --host [{host}] --keepalive 25s"

    service_content = f"""[Unit]
Description=Chisel Service IRAN
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(f"systemctl start {service_name}", shell=True, check=True)

        display_checkmark("\033[92mIRAN service started successfully!\033[0m")

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating IRAN service. Error: {}\033[0m".format(e.output))

def iran_ipv6():
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()
    forward()
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mIRAN\033[0m")
    print("\033[93m───────────────────────────\033[0m")

    key_directory = "/etc/chisel"
    try:
        os.makedirs(key_directory, exist_ok=True)
    except Exception as e:
        display_error("An error occurred while creating the key dir: {}".format(str(e)))

    host = input("\033[93mEnter \033[92mIRAN\033[96m IPV6\033[93m address: \033[0m")
    tunnel_port = input("\033[93mEnter \033[92mTunnel port\033[93m (default: 443): \033[0m") or "443"

    print("\033[93m────────────────────────\033[0m")

    key_path = f"{key_directory}/chisel_key_1.key"
    chisel_key(key_path)
    iran_tcp2(host, key_path, tunnel_port)

def kharej_tc2(config_number, server_number, iran_ipv6, kharej_port, tunnel_port=443):
    service_name = f"kharej_{server_number}_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 25s [{iran_ipv6}]:{tunnel_port} R:localhost:{kharej_port}"

    service_content = f"""[Unit]
Description=Kharej Service {config_number} - Server {server_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(f"systemctl start {service_name}", shell=True, check=True)
        display_checkmark("\033[92mKharej service {}/{} started successfully!\033[0m".format(server_number, config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating Kharej service {}/{}. Error: {}\033[0m".format(server_number, config_number, e.output))

def config_kharej6():
    def kharej_ipv6():
        if not os.path.isfile("/root/chisel"):
            chisel_mnu()
        
        forward()
        print("\033[93m───────────────────────────\033[0m")
        display_notification("\033[93mConfiguring \033[96mKHAREJ\033[0m")
        print("\033[93m───────────────────────────\033[0m")
        
        num_servers = int(input("\033[93mEnter the number of \033[92mIRAN\033[93m servers:\033[0m "))
        server_configs = []

        for i in range(1, num_servers + 1):
            print("\033[93m────────────────────────\033[0m") 
            print("\033[92m    --- Server {} ---\033[0m".format(i))
            print("\033[93m────────────────────────\033[0m")
            
            num_configs = int(input("\033[93mEnter the \033[92mNumber \033[93mof \033[96mKharej Configs: \033[0m".format(i)))
            iran_ipv4 = input("\033[93mEnter \033[92mIRAN Server {}\033[96m IPV4\033[93m address: \033[0m".format(i))
            iran_ipv6 = input("\033[93mEnter \033[92mIRAN Server {}\033[96m IPV6\033[93m address: \033[0m".format(i))
            
            configs = []
            for j in range(1, num_configs + 1):
                kharej_port = input("\033[93mEnter Kharej \033[92mConfig port\033[93m for config {}: \033[0m".format(j))
                configs.append(kharej_port)

                tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m (default: 443): \033[0m") or "443"
                kharej_tc2(j, i, iran_ipv6, kharej_port, tunnel_port)

            print("\033[93m╭──────────────────────────────────────────────────────────────────────╮\033[0m")
            for j, config_port in enumerate(configs, start=1):
                print(f"\033[93m| Server {i} - Config {j}: Your Address & Port: {iran_ipv4} : {config_port}  \033[0m")
            print("\033[93m╰──────────────────────────────────────────────────────────────────────╯\033[0m")

            server_configs.append((iran_ipv4, configs))

        return server_configs

    server_configs = kharej_ipv6()

    return server_configs

        
def kharej_tcp2(config_number, iran_ipv6, kharej_port, tunnel_port=443):
    service_name = f"kharej_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 25s [{iran_ipv6}]:{tunnel_port} R:localhost:{kharej_port}"

    service_content = f"""[Unit]
Description=Kharej Service {config_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(f"systemctl start {service_name}", shell=True, check=True)

        display_checkmark("\033[92mKharej service {} started successfully!\033[0m".format(config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating Kharej service {}. Error: {}\033[0m".format(config_number, e.output))


def kharej_ipv6():
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()
    
    forward()
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mKHAREJ\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mKharej\033[93m Configs: \033[0m"))
    iran_ipv4 = input("\033[93mEnter \033[92mIRAN\033[96m IPV4\033[93m address: \033[0m")
    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[96m IPV6\033[93m address: \033[0m")
    tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m (default: 443): \033[0m") or '443'
    server_ports = []

    for i in range(1, num_configs + 1):
        print("\033[93m────────────────────────\033[0m") 
        print("\033[92m    --- Config {} ---\033[0m".format(i))
        print("\033[93m────────────────────────\033[0m")
        kharej_port = input("\033[93mEnter Kharej \033[92mConfig port\033[93m: \033[0m")
        server_ports.append(kharej_port)

        kharej_tcp2(i, iran_ipv6, kharej_port, tunnel_port)

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    for i in range(num_configs):
        print(f"\033[93m| Config {i+1} - Your Address & Port: {iran_ipv4} : {server_ports[i]}  \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    return server_ports
        
        
def iran_udp(host, key_path, tunnel_port=443):
    service_name = "iran_1"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel server --keyfile {key_path} --reverse --port {tunnel_port} --host {host} --keepalive 25s"

    service_content = f"""[Unit]
Description=Chisel Service IRAN
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(f"systemctl start {service_name}", shell=True, check=True)

        display_checkmark("\033[92mIRAN service started successfully!\033[0m")

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating IRAN service. Error: {}\033[0m".format(e.output))


def iran_ipv4_udp():
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()

    forward()
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mIRAN\033[0m")
    print("\033[93m───────────────────────────\033[0m")

    key_directory = "/etc/chisel"
    try:
        if os.path.exists(key_directory):
            try:
                shutil.rmtree(key_directory)
            except NotADirectoryError:
                os.remove(key_directory)
    except Exception as e:
        display_error("An error occurred while removing: {}".format(str(e)))

    try:
        os.makedirs(key_directory, exist_ok=True)
        print("\033[93m────────────────────────\033[0m")
        host = input("\033[93mEnter \033[92mIRAN\033[96m IPV4\033[93m address: \033[0m")
        tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m (default: 443): \033[0m") or '443'
        print("\033[93m────────────────────────\033[0m")

        key_path = f"{key_directory}/chisel_key_1.key"

        try:
            chisel_key(key_path)
            iran_udp(host, key_path, int(tunnel_port))
        except Exception as e:
            display_error("Failed to generate key: Error: {}".format(str(e)))
    except Exception as e:
        display_error("An error occurred while making dir: {}".format(str(e)))


def kharej_udp(config_number, iran_ipv4, kharej_port, tunnel_port=443):
    service_name = f"kharej_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 25s {iran_ipv4}:{tunnel_port} R:localhost:{kharej_port}/udp"

    service_content = f"""[Unit]
Description=Kharej Service {config_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(f"systemctl start {service_name}", shell=True, check=True)

        display_checkmark("\033[92mKharej service {} started successfully!\033[0m".format(config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating Kharej service {}. Error: {}\033[0m".format(config_number, e.output))
        

def kharej_ipv4_udp():
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()
    
    forward()
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mKHAREJ\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mKharej\033[93m Configs: \033[0m"))
    iran_ipv4 = input("\033[93mEnter \033[92mIRAN\033[96m IPV4\033[93m address: \033[0m")
    tunnel_port = input("\033[93mEnter \033[92mTunnel\033[96m port\033[93m [Default: 443]: \033[0m") or "443"
    server_ports = []

    for i in range(1, num_configs + 1):
        print("\033[93m────────────────────────\033[0m") 
        print("\033[92m    --- Config {} ---\033[0m".format(i))
        print("\033[93m────────────────────────\033[0m")
        kharej_port = input("\033[93mEnter Kharej \033[92mConfig port \033[93m[UDP]: \033[0m")
        server_ports.append(kharej_port)

        kharej_udp(i, iran_ipv4, kharej_port, tunnel_port)

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    for i in range(num_configs):
        print(f"\033[93m| Config {i+1} - Your Address & Port: {iran_ipv4} : {server_ports[i]}  \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    return server_ports

def kharej_ud6(config_number, server_number, iran_ipv6, kharej_port, tunnel_port):
    service_name = f"kharej_{server_number}_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 25s [{iran_ipv6}]:{tunnel_port} R:localhost:{kharej_port}/udp"

    service_content = f"""[Unit]
Description=Kharej Service {config_number} - Server {server_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(f"systemctl start {service_name}", shell=True, check=True)
        display_checkmark("\033[92mKharej service {}/{} started successfully!\033[0m".format(server_number, config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating Kharej service {}/{}. Error: {}\033[0m".format(server_number, config_number, e.output))


def config_ud6():
    def kharej_ipv6_udp():
        if not os.path.isfile("/root/chisel"):
            chisel_mnu()

        forward()
        print("\033[93m───────────────────────────\033[0m")
        display_notification("\033[93mConfiguring \033[96mKHAREJ\033[0m")
        print("\033[93m───────────────────────────\033[0m")

        num_servers = int(input("\033[93mEnter the number of \033[92mIRAN\033[93m servers:\033[0m "))
        server_configs = []

        for i in range(1, num_servers + 1):
            print("\033[93m────────────────────────\033[0m")
            print("\033[92m    --- Server {} ---\033[0m".format(i))
            print("\033[93m────────────────────────\033[0m")

            num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mKharej configs: \033[0m".format(i)))
            iran_ipv4 = input("\033[93mEnter \033[92mIRAN Server {}\033[96m IPV4\033[93m address: \033[0m".format(i))
            iran_ipv6 = input("\033[93mEnter \033[92mIRAN Server {}\033[96m IPV6\033[93m address: \033[0m".format(i))

            configs = []
            for j in range(1, num_configs + 1):
                kharej_port = input("\033[93mEnter \033[96mKharej \033[92mConfig {} port\033[93m: \033[0m".format(j))
                tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m (default: 443): \033[0m") or "443"

                configs.append(kharej_port)

                kharej_ud6(j, i, iran_ipv6, kharej_port, tunnel_port)

            print("\033[93m╭──────────────────────────────────────────────────────────────────────╮\033[0m")
            for j, config_port in enumerate(configs, start=1):
                print(f"\033[93m| Server {i} - Config {j}: Your Address & Port: {iran_ipv4} : {config_port}  \033[0m")
            print("\033[93m╰──────────────────────────────────────────────────────────────────────╯\033[0m")

            server_configs.append((iran_ipv4, configs))

        return server_configs

    server_configs = kharej_ipv6_udp()

    return server_configs
    
def kharej_ud(config_number, server_number, iran_ipv4, kharej_port, tunnel_port=443):
    service_name = f"kharej_{server_number}_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 25s {iran_ipv4}:{tunnel_port} R:localhost:{kharej_port}/udp"

    service_content = f"""[Unit]
Description=Kharej Service {config_number} - Server {server_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(f"systemctl start {service_name}", shell=True, check=True)
        display_checkmark("\033[92mKharej service {}/{} started successfully!\033[0m".format(server_number, config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating Kharej service {}/{}. Error: {}\033[0m".format(server_number, config_number, e.output))


def config_kha_udp():
    def kharej_ip4(num_servers, tunnel_port):
        if not os.path.isfile("/root/chisel"):
            chisel_mnu()
        forward()
        print("\033[93m───────────────────────────\033[0m")
        display_notification("\033[93mConfiguring \033[96mKHAREJ\033[0m")
        print("\033[93m───────────────────────────\033[0m")
        server_configs = []

        for i in range(1, num_servers + 1):
            print("\033[93m────────────────────────\033[0m") 
            print("\033[92m    --- Server {} ---\033[0m".format(i))
            print("\033[93m────────────────────────\033[0m")
            iran_ipv4 = input("\033[93mEnter \033[92mIRAN Server {} \033[96mIPV4\033[93m address: \033[0m".format(i))
            num_configs = int(input("\033[93mEnter the \033[93mnumber \033[93mof \033[96mKharej configs:\033[0m ".format(i)))
            
            configs = []
            for j in range(1, num_configs + 1):
                kharej_port = input("\033[93mEnter \033[96mKharej \033[92mConfig {} port\033[93m: \033[0m".format(j))
                configs.append(kharej_port)

            server_configs.append((iran_ipv4, configs))

            for j, config_port in enumerate(configs, start=1):
                kharej_ud(j, i, iran_ipv4, config_port, tunnel_port)

            print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────╮\033[0m")
            for j, config_port in enumerate(configs, start=1):
                print(f"\033[93m| Server {i} - Config {j}: Your Address & Port: {iran_ipv4} : {config_port}  \033[0m")
            print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────╯\033[0m")

        return server_configs

    num_iran_servers = int(input("\033[93mEnter the number of \033[92mIRAN\033[93m servers:\033[0m "))
    tunnel_port = int(input("\033[93mEnter \033[92mTunnel Port\033[93m (default: 443):\033[0m ") or 443)
    if num_iran_servers > 0:
        kharej_ip4(num_iran_servers, tunnel_port)
    else:
        print("\033[91mNo Iran servers, so I'm giving up..\033[0m")
        
def iran_udp2(host, key_path, tunnel_port=443):
    service_name = "iran_1"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel server --keyfile {key_path} --reverse --port {tunnel_port} --host [{host}] --keepalive 25s"

    service_content = f"""[Unit]
Description=Chisel Service IRAN
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(f"systemctl start {service_name}", shell=True, check=True)

        display_checkmark("\033[92mIRAN service started successfully!\033[0m")

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating IRAN service. Error: {}\033[0m".format(e.output))

def iran_ipv6_udp():
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()
        
    forward()
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mIRAN\033[0m")
    print("\033[93m───────────────────────────\033[0m")

    key_directory = "/etc/chisel"
    try:
        if os.path.exists(key_directory):
            try:
                shutil.rmtree(key_directory)
            except NotADirectoryError:
                os.remove(key_directory)
    except Exception as e:
        display_error("An error occurred while removing: {}".format(str(e)))

    try:
        os.makedirs(key_directory, exist_ok=True)  
        host = input("\033[93mEnter \033[92mIRAN\033[96m IPV6\033[93m address: \033[0m")
        tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m (default: 443):\033[0m ") or 443

        print("\033[93m────────────────────────\033[0m") 
        
        key_path = f"{key_directory}/chisel_key_1.key"
        chisel_key(key_path)
        iran_udp2(host, key_path, tunnel_port)

    except Exception as e:
        display_error("An error occurred: {}".format(str(e)))
        
def kharej_udp2(config_number, iran_ipv4, iran_ipv6, kharej_port, tunnel_port=443):
    service_name = f"kharej_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 25s [{iran_ipv6}]:{tunnel_port} R:localhost:{kharej_port}/udp"

    service_content = f"""[Unit]
Description=Kharej Service {config_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(f"systemctl start {service_name}", shell=True, check=True)

        display_checkmark("\033[92mKharej service {} started successfully!\033[0m".format(config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)

        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating Kharej service {}. Error: {}\033[0m".format(config_number, e.output))


def kharej_ipv6_udp():
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()

    forward()
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mKHAREJ\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mKharej\033[93m Configs: \033[0m"))

    iran_ipv4 = input("\033[93mEnter \033[92mIRAN\033[96m IPV4\033[93m address: \033[0m")
    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[96m IPV6\033[93m address: \033[0m")
    tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m [default: 443]: \033[0m") or "443"
    server_ports = []

    for i in range(1, num_configs + 1):
        print("\033[93m────────────────────────\033[0m")
        print("\033[92m    --- Config {} ---\033[0m".format(i))
        print("\033[93m────────────────────────\033[0m")
        kharej_port = input("\033[93mEnter Kharej \033[92mConfig port\033[93m [UDP]: \033[0m")
        server_ports.append(kharej_port)

        kharej_udp2(i, iran_ipv4, iran_ipv6, kharej_port, tunnel_port)

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    for i in range(num_configs):
        print(f"\033[93m| Config {i+1} - Your Address & Port: {iran_ipv4} : {server_ports[i]}  \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    return server_ports
        
        ## private
        
def add_cron_job():
    try:
        subprocess.run(
            "echo '@reboot /bin/bash /etc/chi.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)
        
def run_ping():
    try:
        print("\033[96mPlease Wait, Azumi is pinging...\033[0m")
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b63e:b481::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
 
def run_ping_iran():
    try:
        print("\033[96mPlease Wait, Azumi is pinging...\033[0m")
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b63e:b481::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def ping_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping.sh
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping.service'])
    subprocess.run(['systemctl', 'start', 'ping.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping.service'])
    
        

            
def kharej_private_menu():
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/chi.sh"):
        os.remove("/etc/chi.sh")

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumich", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumich", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "fd1d:fc98:b63e:b481::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumich"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumich mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumich up\n")
        f.write("ip addr add fd1d:fc98:b63e:b481::1/64 dev azumich\n")

    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")

    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping()
    sleep(1)


    script_content1 = '''#!/bin/bash


ip_address="fd1d:fc98:b63e:b481::2"


max_pings=3


interval=35


while true
do
   
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping.sh', 0o755)
    ping_service()
   



def iran_private_menu():

    print("\033[93m────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")
    
    if os.path.isfile("/etc/chi.sh"):
        os.remove("/etc/chi.sh")
    

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    
    
    subprocess.run(["ip", "tunnel", "add", "azumich", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumich", "up"], stdout=subprocess.DEVNULL)
    
    
    initial_ip = "fd1d:fc98:b63e:b481::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumich"], stdout=subprocess.DEVNULL)
    
    

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/chi.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumich mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumich up\n")
        f.write("ip addr add fd1d:fc98:b63e:b481::2/64 dev azumich\n")

    
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    


    add_cron_job()

    sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
   
    run_ping_iran()
    sleep(1)

    


    script_content = '''#!/bin/bash


ip_address="fd1d:fc98:b63e:b481::2"


max_pings=3


interval=43


while true
do

    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''


    with open('/etc/ping.sh', 'w') as script_file:
        script_file.write(script_content)


    os.chmod('/etc/ping.sh', 0o755)
    ping_service()

        
                      
        
def iran_tcp3(key_path, tunnel_port=443):
    service_name = "iran_1"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel server --keyfile {key_path} --reverse --port {tunnel_port} --host [fd1d:fc98:b63e:b481::2] --keepalive 25s"

    service_content = f"""[Unit]
Description=Chisel Service IRAN
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(f"systemctl start {service_name}", shell=True, check=True)

        display_checkmark("\033[92mIRAN service started successfully!\033[0m")

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)

        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating IRAN service. Error: {}\033[0m".format(e.output))


def irpri_ipv6():
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()

    forward()
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mIRAN\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    interface_check = subprocess.run(["ip", "link", "show", "azumich"], capture_output=True, text=True)
    if "azumich" in interface_check.stdout:
        print("\033[96mazumich interface is available.\033[0m")
    else:
        iran_private_menu()

    key_directory = "/etc/chisel"
    try:
        if os.path.exists(key_directory):
            try:
                shutil.rmtree(key_directory)
            except NotADirectoryError:
                os.remove(key_directory)
    except Exception as e:
        display_error("An error occurred while removing: {}".format(str(e)))

    try:
        os.makedirs(key_directory, exist_ok=True)

        print("\033[93m────────────────────────\033[0m")

        key_path = f"{key_directory}/chisel_key_1.key"
        chisel_key(key_path)

        tunnel_port = input("\033[93mEnter \033[92mTunnel port\033[93m [default: 443]: \033[0m") or "443"

        iran_tcp3(key_path, tunnel_port)
    except Exception as e:
        display_error("An error occurred: {}".format(str(e)))
        
        
        
def khpri_tcp2(config_number, kharej_port, tunnel_port=443):
    service_name = f"kharej_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 25s [fd1d:fc98:b63e:b481::2]:{tunnel_port} R:localhost:{kharej_port}"

    service_content = f"""[Unit]
Description=Kharej Service {config_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(f"systemctl start {service_name}", shell=True, check=True)

        display_checkmark("\033[92mKharej service {} started successfully!\033[0m".format(config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating Kharej service {}. Error: {}\033[0m".format(config_number, e.output))


def khpri_ipv6():
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()
    forward()
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mKHAREJ\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    interface_check = subprocess.run(["ip", "link", "show", "azumich"], capture_output=True, text=True)
    if "azumich" in interface_check.stdout:
        print("\033[96mazumich interface is available.\033[0m")
    else:
        kharej_private_menu()
    
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mKharej\033[93m Configs: \033[0m"))

    server_ports = []
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m [default=443]: \033[0m") or "443"

    for i in range(1, num_configs + 1):
        print("\033[93m────────────────────────\033[0m") 
        print("\033[92m    --- Config {} ---\033[0m".format(i))
        print("\033[93m────────────────────────\033[0m")
        kharej_port = input("\033[93mEnter Kharej \033[92mConfig port\033[93m: \033[0m")
        server_ports.append(kharej_port)

        khpri_tcp2(i, kharej_port, tunnel_port)

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    for i in range(num_configs):
        print(f"\033[93m| Config {i+1} - Your Address & Port: {remote_ip} : {server_ports[i]}  \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    return server_ports
        
		
        
        
def iran_udp3(key_path, tunnel_port=443):
    service_name = "iran_1"
    service_file = "/etc/systemd/system/iran.service"
    chisel_command = f"./chisel server --keyfile {key_path} --reverse --port {tunnel_port} --host [fd1d:fc98:b63e:b481::2] --keepalive 25s"

    service_content = f"""[Unit]
Description=Chisel Service IRAN
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(f"systemctl start {service_name}", shell=True, check=True)

        display_checkmark("\033[92mIRAN service started successfully!\033[0m")

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating IRAN service. Error: {}\033[0m".format(e.output))


def irpri_ipv6_udp():
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()

    forward()
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mIRAN\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    interface_check = subprocess.run(["ip", "link", "show", "azumich"], capture_output=True, text=True)
    if "azumich" in interface_check.stdout:
        print("\033[96mazumich interface is available.\033[0m")
    else:
        iran_private_menu()

    key_directory = "/etc/chisel"
    try:
        if os.path.exists(key_directory):
            try:
                shutil.rmtree(key_directory)
            except NotADirectoryError:
                os.remove(key_directory)
    except Exception as e:
        display_error("An error occurred while removing: {}".format(str(e)))

    try:
        os.makedirs(key_directory, exist_ok=True)

        print("\033[93m────────────────────────\033[0m")

        key_path = f"{key_directory}/chisel_key_1.key"
        chisel_key(key_path)

        tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m [default=443]: \033[0m") or "443"

        iran_udp3(key_path, tunnel_port)
    except Exception as e:
        display_error("An error occurred: {}".format(str(e)))
        
        
        
def kharej_udp3(config_number, kharej_port, tunnel_port=443):
    service_name = f"kharej_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 25s [fd1d:fc98:b63e:b481::2]:{tunnel_port} R:localhost:{kharej_port}/udp"

    service_content = f"""[Unit]
Description=Kharej Service {config_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=21600
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(f"systemctl start {service_name}", shell=True, check=True)

        display_checkmark("\033[92mKharej service {config_number} started successfully!\033[0m")

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating Kharej service {config_number}. Error: {e.output}\033[0m")
        

def khpri_ipv6_udp():
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()
    forward()
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mKHAREJ\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    interface_check = subprocess.run(["ip", "link", "show", "azumich"], capture_output=True, text=True)
    if "azumich" in interface_check.stdout:
        print("\033[96mazumich interface is available.\033[0m")
    else:
        kharej_private_menu()
    
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mKharej\033[93m Configs: \033[0m"))
    server_ports = []
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m [default=443]: \033[0m") or "443"
    for i in range(1, num_configs + 1):
        print("\033[93m────────────────────────\033[0m") 
        print("\033[92m    --- Config {} ---\033[0m".format(i))
        print("\033[93m────────────────────────\033[0m")
        kharej_port = input("\033[93mEnter Kharej \033[92mConfig port\033[93m[UDP]: \033[0m")
        server_ports.append(kharej_port)

        kharej_udp3(i, kharej_port, tunnel_port)

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    for i in range(num_configs):
        print(f"\033[93m| Config {i+1} - Your Address & Port: {remote_ip} : {server_ports[i]}  \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    return server_ports
        
        

def chisel_status():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mStatus Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mChisel Single Server \033[0m')
    print('2. \033[93m[1] IRAN [5] Kharej \033[0m')
    print('3. \033[96m[5] IRAN [1] Kharej \033[0m')
    print('4. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            chisel1_status()
            break
        elif server_type == '2':
            chisel4_status()
            break
        elif server_type == '3':
            chisel2_status()
            break
        elif server_type == '4':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')

def chisel2_status():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mChisel Kharej Status\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mConfigs\033[93m:\033[0m "))

    services = {
        'iran': 'iran',
        'kharej': 'kharej_1'
    }

    print("\033[93m            ╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m            ║                 \033[92mChisel Status\033[93m              ║\033[0m")
    print("\033[93m            ╠════════════════════════════════════════════╣\033[0m")

    for service, service_name in services.items():
        try:
            for i in range(num_configs):
                config_service_name = f"{service_name}_{i+1}.service"
                status_output = os.popen(f"systemctl is-active {config_service_name}").read().strip()

                if status_output == "active":
                    status = "\033[92m✓ Active     \033[0m"
                else:
                    status = "\033[91m✘ Inactive   \033[0m"

                if service == 'iran':
                    display_name = '\033[93mIRAN Server   \033[0m'
                elif service == 'kharej':
                    display_name = '\033[93mKharej Service\033[0m'
                else:
                    display_name = service

                print(f"           \033[93m ║\033[0m    {display_name} {i+1}:   |    {status:<10} \033[93m ║\033[0m")

        except OSError as e:
            print(f"Error in retrieving status for {service}: {e}")
            continue

    print("\033[93m            ╚════════════════════════════════════════════╝\033[0m")

def chisel4_status():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mChisel Status\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mConfigs\033[93m:\033[0m "))

    services = {
        'iran': 'iran',
        'kharej': 'kharej'
    }

    print("\033[93m            ╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m            ║                 \033[92mChisel Status\033[93m              ║\033[0m")
    print("\033[93m            ╠════════════════════════════════════════════╣\033[0m")

    for service, service_name in services.items():
        try:
            for i in range(num_configs):
                config_service_name = f"{service_name}_{i+1}.service"
                status_output = os.popen(f"systemctl is-active {config_service_name}").read().strip()

                if status_output == "active":
                    status = "\033[92m✓ Active     \033[0m"
                else:
                    status = "\033[91m✘ Inactive   \033[0m"

                if service == 'iran':
                    display_name = '\033[93mIRAN Server   \033[0m'
                elif service == 'kharej':
                    display_name = '\033[93mKharej Service\033[0m'
                else:
                    display_name = service

                print(f"           \033[93m ║\033[0m    {display_name} {i+1}:   |    {status:<10} \033[93m ║\033[0m")

        except OSError as e:
            print(f"Error in retrieving status for {service}: {e}")
            continue

    print("\033[93m            ╚════════════════════════════════════════════╝\033[0m")
    
def chisel1_status():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mChisel Status\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mConfigs\033[93m:\033[0m "))

    services = {
        'iran': 'iran',
        'kharej': 'kharej'
    }

    print("\033[93m            ╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m            ║                 \033[92mChisel Status\033[93m              ║\033[0m")
    print("\033[93m            ╠════════════════════════════════════════════╣\033[0m")

    for service, service_name in services.items():
        try:
            for i in range(num_configs):
                config_service_name = f"{service_name}_{i+1}.service"
                status_output = os.popen(f"systemctl is-active {config_service_name}").read().strip()

                if status_output == "active":
                    status = "\033[92m✓ Active     \033[0m"
                else:
                    status = "\033[91m✘ Inactive   \033[0m"

                if service == 'iran':
                    display_name = '\033[93mIRAN Server   \033[0m'
                elif service == 'kharej':
                    display_name = '\033[93mKharej Service\033[0m'
                else:
                    display_name = service

                print(f"           \033[93m ║\033[0m    {display_name} {i+1}:   |    {status:<10} \033[93m ║\033[0m")

        except OSError as e:
            print(f"Error in retrieving status for {service}: {e}")
            continue

    print("\033[93m            ╚════════════════════════════════════════════╝\033[0m")

def uni_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mUninstall Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mChisel Single Server \033[0m')
    print('2. \033[93mChisel Multiple Servers \033[0m')
    print('3. \033[96mChisel + privateIP \033[0m')
    print('4. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            remove_chisel()
            break
        elif server_type == '2':
            remove_chisel3()
            break
        elif server_type == '3':
            remove_chisel2()
            break
        elif server_type == '4':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')

def remove_chisel3():
    os.system("clear")
    display_notification("\033[93mRemoving \033[92mChisel\033[93m Multiple Servers\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /root/chisel", shell=True) == 0:
            subprocess.run("rm /root/chisel", shell=True)

        time.sleep(1)

        chisel_services = ["kharej" , "kharej_1" , "iran" , "kharej_2" , "kharej_3" , "kharej_4" , "kharej_5"]  

        num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mConfigs\033[93m:\033[0m "))

        for service_name in chisel_services:
            for i in range(1, num_configs + 1):
                service_name_with_num = f"{service_name}_{i}"
                subprocess.run(f"systemctl disable {service_name_with_num}.service > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl stop {service_name_with_num}.service > /dev/null 2>&1", shell=True)
                subprocess.run(f"rm /etc/systemd/system/{service_name_with_num}.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except Exception as e:
        print("An error occurred while uninstalling..:", str(e))
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def remove_chisel():
    os.system("clear")
    display_notification("\033[93mRemoving \033[92mChisel\033[93m ...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /root/chisel", shell=True) == 0:
            subprocess.run("rm /root/chisel", shell=True)

        time.sleep(1)

        chisel_services = ["kharej", "iran"]  

        num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mConfigs\033[93m:\033[0m "))

        for service_name in chisel_services:
            for i in range(1, num_configs + 1):
                service_name_with_num = f"{service_name}_{i}"
                subprocess.run(f"systemctl disable {service_name_with_num}.service > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl stop {service_name_with_num}.service > /dev/null 2>&1", shell=True)
                subprocess.run(f"rm /etc/systemd/system/{service_name_with_num}.service > /dev/null 2>&1", shell=True)
                time.sleep(1)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except Exception as e:
        print("An error occurred while uninstalling..:", str(e))
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def remove_private():
    display_notification("\033[93mRemoving \033[92mprivate IP addresses\033[93m...\033[0m")
    
    try:
        if subprocess.call("test -f /etc/chi.sh", shell=True) == 0:
            subprocess.run("rm /etc/chi.sh", shell=True)
            
        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/chi.sh\" | crontab -", shell=True)
        
        subprocess.run("sudo rm /etc/ping.sh", shell=True)
        
        time.sleep(1)
        subprocess.run("systemctl disable ping.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumich down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumich > /dev/null", shell=True)
        
        print("Progress: ", end="")
        
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 3  
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)
        
        display_checkmark("\033[92mUninstall completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def remove_chisel2():
    os.system("clear")
    display_notification("\033[93mRemoving Chisel + Private IP ...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    remove_private()
    try:
        if subprocess.call("test -f /root/chisel", shell=True) == 0:
            subprocess.run("rm /root/chisel", shell=True)

        time.sleep(1)

        chisel_services = ["kharej", "iran"]  
        print("\033[93m───────────────────────────────────────\033[0m")
        num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mConfigs\033[93m:\033[0m "))

        for service_name in chisel_services:
            for i in range(1, num_configs + 1):
                service_name_with_num = f"{service_name}_{i}"
                subprocess.run(f"systemctl disable {service_name_with_num}.service > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl stop {service_name_with_num}.service > /dev/null 2>&1", shell=True)
                subprocess.run(f"rm /etc/systemd/system/{service_name_with_num}.service > /dev/null 2>&1", shell=True)
                time.sleep(1)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except Exception as e:
        print("An error occurred while uninstalling..:", str(e))
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def start_serv():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m SERVICES\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mRestart SERVICES \033[0m')
    print('2. \033[93mStop SERVICES \033[0m')
    print('0. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            start_servv()
            break
        elif server_type == '2':
            stop_servv()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')
         
def start_servv():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Restart SERVICES\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92m[1] Kharej [5] IRAN \033[0m')
    print('2. \033[93m[5] Kharej [1] IRAN \033[0m')
    print('3. \033[96mSingle Server \033[0m')
    print('0. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            restart1()
            break
        elif server_type == '2':
            restart2()
            break
        elif server_type == '3':
            restart3()
            break
        elif server_type == '0':
            os.system("clear")
            start_serv()
            break
        else:
            print('Invalid choice.')

def restart3():
    os.system("clear")
    display_notification("\033[93mRestarting \033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        
        num_configs = int(input("\033[93mHow many \033[92mConfigs\033[93m do you have? \033[0m"))
        
        for i in range(1, num_configs+1):
            service_name = f"kharej_{i}.service"

            subprocess.run(f"systemctl restart {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)
        
        for i in range(1, num_configs+1):
            service_name = f"iran_{i}.service"
            subprocess.run(f"systemctl restart {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mRestart completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def restart2():
    os.system("clear")
    display_notification("\033[93mRestarting \033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        
        num_configs = int(input("\033[93mHow many \033[92mConfigs\033[93m do you have? \033[0m"))
        
        for i in range(1, num_configs+1):
            service_name = f"kharej_{i}.service"
            service_name2 = f"kharej_1_{i}.service"
            service_name3 = f"kharej_2_{i}.service"
            service_name4 = f"kharej_3_{i}.service"
            service_name5 = f"kharej_4_{i}.service"
            service_name6 = f"kharej_5_{i}.service"
            subprocess.run(f"systemctl restart {service_name} > /dev/null 2>&1", shell=True)
            subprocess.run(f"systemctl restart {service_name2} > /dev/null 2>&1", shell=True)
            subprocess.run(f"systemctl restart {service_name3} > /dev/null 2>&1", shell=True)
            subprocess.run(f"systemctl restart {service_name4} > /dev/null 2>&1", shell=True)
            subprocess.run(f"systemctl restart {service_name5} > /dev/null 2>&1", shell=True)
            subprocess.run(f"systemctl restart {service_name6} > /dev/null 2>&1", shell=True)
            time.sleep(1)
        
        for i in range(1, num_configs+1):
            service_name = f"iran_{i}.service"
            subprocess.run(f"systemctl restart {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mRestart completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def restart1():
    os.system("clear")
    display_notification("\033[93mRestarting \033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        
        num_configs = int(input("\033[93mHow many\033[92m Configs\033[93m do you have? \033[0m"))
        
        for i in range(1, num_configs+1):
            service_name = f"kharej_1_{i}.service"

            subprocess.run(f"systemctl restart {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)
        
        for i in range(1, num_configs+1):
            service_name = f"iran_{i}.service"
            subprocess.run(f"systemctl restart {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mRestart completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())

def stop_servv():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Stop SERVICES\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92m[1] Kharej [5] IRAN \033[0m')
    print('2. \033[93m[5] Kharej [1] IRAN \033[0m')
    print('3. \033[96mSingle Server \033[0m')
    print('0. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            stop1()
            break
        elif server_type == '2':
            stop2()
            break
        elif server_type == '3':
            stop3()
            break
        elif server_type == '0':
            os.system("clear")
            start_serv()
            break
        else:
            print('Invalid choice.')

def stop3():
    os.system("clear")
    display_notification("\033[93mStopping \033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        
        num_configs = int(input("\033[93mHow many \033[92mConfigs\033[93m do you have? \033[0m"))
        
        for i in range(1, num_configs+1):
            service_name = f"kharej_{i}.service"

            subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)
        
        for i in range(1, num_configs+1):
            service_name = f"iran_{i}.service"
            subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mService Stopped!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def stop2():
    os.system("clear")
    display_notification("\033[93mStopping \033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        
        num_configs = int(input("\033[93mHow many \033[92mConfigs\033[93m do you have? \033[0m"))
        
        for i in range(1, num_configs+1):
            service_name = f"kharej_{i}.service"
            service_name2 = f"kharej_1_{i}.service"
            service_name3 = f"kharej_2_{i}.service"
            service_name4 = f"kharej_3_{i}.service"
            service_name5 = f"kharej_4_{i}.service"
            service_name6 = f"kharej_5_{i}.service"
            subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
            subprocess.run(f"systemctl stop{service_name2} > /dev/null 2>&1", shell=True)
            subprocess.run(f"systemctl stop{service_name3} > /dev/null 2>&1", shell=True)
            subprocess.run(f"systemctl stop {service_name4} > /dev/null 2>&1", shell=True)
            subprocess.run(f"systemctl stop {service_name5} > /dev/null 2>&1", shell=True)
            subprocess.run(f"systemctl stop {service_name6} > /dev/null 2>&1", shell=True)
            time.sleep(1)
        
        for i in range(1, num_configs+1):
            service_name = f"iran_{i}.service"
            subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mService Stopped!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def stop1():
    os.system("clear")
    display_notification("\033[93mStopping \033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        
        num_configs = int(input("\033[93mHow many\033[92m Configs\033[93m do you have? \033[0m"))
        
        for i in range(1, num_configs+1):
            service_name = f"kharej_1_{i}.service"

            subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)
        
        for i in range(1, num_configs+1):
            service_name = f"iran_{i}.service"
            subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mService Stopped!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
main_menu()
