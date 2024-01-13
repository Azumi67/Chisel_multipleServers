#
# 6to4 Configuration Script
# Author: github.com/Azumi67
# This is for educational use and my own learning, please provide me with feedback if possible
# This script is designed to simplify the configuration of 6to4 tunnels.
#
# Supported operating systems: Ubuntu 20, Debian 12
#
# Usage:
#   - Run the script with root privileges.
#   - Follow the on-screen prompts to install, configure, or uninstall the tunnel.
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
import netifaces as ni
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', errors='replace')

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
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    delay = 0.1
    duration = 5  

    end_time = time.time() + duration

    while time.time() < end_time:
        for frame in frames:
            print('\r[' + frame + '] Loading...  ', end='')
            time.sleep(delay)
            print('\r[' + frame + ']             ', end='')
            time.sleep(delay)

    
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
                 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⢀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⡀⠤⠒⠊⠉⠀⠀⠀⠀⠈⠁⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀\033[1;93m⠀⢀⠔⠉⠀⠀⠀⠀⢀⡠⠤⠐⠒⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⣀⡠⠤⠤⠀⠀⠂⠐\033[1;96m⠀⠠⢤⠎⢑⡭⣽⣳⠶⣖⡶⣤⣖⣬⡽⡭⣥⣄\033[1;93m⠒⠒⠀⠐⠁⠑⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⢀⠴⠊⠁⠀⠀⠀⠀⡀⠀\033[1;96m⣠⣴⡶⣿⢏⡿⣝⡳⢧⡻⣟⡻⣞⠿⣾⡽⣳⣯⣳⣞⡻⣦⡀⠀⠀\033[1;93m⠀⠈⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢨⠀⠀⠀⢀⠤⠂⠁\033[1;96m⢠⣾⡟⣧⠿⣝⣮⣽⢺⣝⣳⡽⣎⢷⣫⡟⡵⡿⣵⢫⡷⣾⢷⣭⢻⣦⡄\033[1;93m⠤⡸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠘⡄⠀⠀⠓⠂⠀\033[1;96m⣴⣿⢷⡿⣝⣻⣏⡷⣾⣟⡼⣣⢟⣼⣣⢟⣯⢗⣻⣽⣏⡾⡽⣟⣧⠿⡼⣿⣦\033[1;93m⣃⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢀⠇⠀⠀⠀⠀\033[1;96m⣼⣿⢿⣼⡻⣼⡟⣼⣧⢿⣿⣸⡧⠿⠃⢿⣜⣻⢿⣤⣛⣿⢧⣻⢻⢿⡿⢧⣛⣿⣧⠀\033[1;93m⠛⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⢸⠁⠀⠀⠀⠀\033[1;96m⣼⣻⡿⣾⣳⡽⣾⣽⡷⣻⣞⢿⣫⠕⣫⣫⣸⢮⣝⡇⠱⣏⣾⣻⡽⣻⣮⣿⣻⡜⣞⡿⣷\033[1;93m⢀⠀⠀⠑⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠘⣧⠀⠀⠀\033[1;96m⣼⣳⢯⣿⣗⣿⣏⣿⠆⣟⣿⣵⢛⣵⡿⣿⣏⣟⡾⣜⣻⠀⢻⡖⣷⢳⣏⡶⣻⡧⣟⡼⣻⡽⣇\033[1;93m⠁⠢⡀⠠⡀⠑⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠈⢦⠀\033[1;96m⣰⣯⣟⢯⣿⢾⣹⢾⡟⠰⣏⡾⣾⣟⡷⣿⣻⣽⣷⡶⣟⠿⡆⠀⢻⣝⣯⢷⣹⢧⣿⢧⡻⣽⣳⢽⡀\033[1;93m⠀⠈⠀⠈⠂⡼⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⡀⢵\033[1;96m⣟⣾⡟⣾⣿⣻⢽⣺⠇⠀⣿⡱⢿⡞⣵⡳⣭⣿⡜⣿⣭⣻⣷⠲⠤⢿⣾⢯⢯⣛⢿⣳⡝⣾⣿⢭⡇⠀\033[1;93m⠀⠀⠀⡰⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢀⠤⠊⠀\033[1;96m⣼⢻⣿⢞⣯⢿⡽⣸⣹⡆⠀⢷⣏⢯⣿⣧⣛⠶⣯⢿⣽⣷⣧⣛⣦⠀⠀⠙⢿⣳⣽⣿⣣⢟⡶⣿⣫⡇⠀⠀\033[1;93m⠀⠰⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⣠⠖⠁⠀⠀⡄\033[1;96m⡿⣯⣷⣻⡽⣞⡟⣿⣿⣟⠉⠈⢯⣗⣻⣕⢯⣛⡞⣯⢮⣷⣭⡚⠓⠋⠀⠀⠀⠈⠉⣿⡽⣎⠷⡏⡷⣷⠀⠀⠀\033[1;93m⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠐⣇⠀⠀⢀⠊\033[1;96m⣼⣇⣿⡗⣿⣽⣷⡿⣿⣱⡿⣆⠀⠀⠙⠒⠛⠓⠋⠉⠉⠀⠀⠀\033[1;91m⢠⣴⣯⣶⣶⣤⡀\033[1;96m ⠀⣿⣟⡼⣛⡇⣟⣿⡆\033[1;93m⡀⠀⢀⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠘⢤⠀⠃⠌\033[1;96m⣸⣿⢾⡽⣹⣾⠹⣞⡵⣳⣽⡽⣖⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;91m⣤⣖⣻⣾⣝⢿⡄\033[1;96m ⢸⣯⢳⣏⡿⣏⣾⢧\033[1;93m⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠘⠀⠈⠀\033[1;96m⡿⣿⣻⡽⣽⣿⢧⠌⠉\033[1;91m⠉⣴⣿⣿⣫⣅⡀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣛⠿⠿⢟⢙⡄⠙\033[1;96m ⠘⣯⢳⣞⡟⣯⢾⣻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⡇⠀⠀⠀\033[1;96m⡿⣿⣿⢵⣫⣿⣆⠁⠂\033[1;91m⣼⡿⢹⣿⡿⠽⠟⢢⠀⠀⠀⠀⠀⠀⠀⢹⠀⢄⢀⠀⡿⠀⠀\033[1;96m ⢰⣯⢷⣺⣏⣯⢻⡽⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⡇⠀⢀⠠\033[1;96m⣿⣿⢾⣛⡶⣽⠈⢓⠀\033[1;91m⢻⠁⢸⠇⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠑⠠⠤⠔⠂⠀⠀\033[1;96m ⢸⣿⢮⣽⠿⣜⣻⡝⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠑⠊⠁\033[1;96m⢠⡷⡇⣿⣿⢼⣹⡀⠀⠑⢄⠀\033[1;91m⠀⠃⠌⣁⠦⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠂⠀⠀\033[1;96m⢀⣿⢾⡝⣾⡽⣺⢽⣹⣽⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣻⢽⣻⡟⣮⣝⡷⢦⣄⣄⣢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣯⢿⡺⣟⢷⡹⢾⣷⡞⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣟⡿⣎⢿⡽⣳⢮⣿⣹⣾⣯⡝⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⣀⣴⡟⣿⢧⣏⢷⡟⣮⠝⢿⣹⣯⡽⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣯⡷⣏⣾⡳⣽⢺⣷⡹⣟⢶⡹⣾⡽⣷⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠔⣾⢯⣷⡇⣿⢳⣎⢿⡞⣽⢦⣼⡽⣧⢻⡽⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣟⢾⡷⣭⣿⢳⣭⢻⣷⡻⣜⣻⡵⣻⡼⣿⠾⠫\033[1;96m⣽⣟⣶⣶⣶⠒⠒⠂⠉⠀\033[1;96m⢸⣽⢺⡷⣷⣯⢗⣮⣟⢾⢧⣻⠼⡿⣿⢣⡟⣼⣆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⣝⣾⢳⢧⣟⡳⣎⣿⣿⣱⢏⣾⣽⣳⠟\033[1;92m⠁⠀⡌⠈\033[1;96m⢹⡯⠟⠛⠀⠀⠀⠀⠀⠈\033[1;96m⣷⢻⣼⣽⣿⡾⣼⣏⣾⣻⡜⣯⣷⢿⣟⣼⡳⣞⣦⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⢿⡸⣎⠿⣾⡏⣷⣉⣷⣿⢹⣎⡿\033[1;92m⠎⡎⠀⠀⠀⡇⠀⣾⠱⡀⠀⠀⠀⠀⠀⠀⠀⠈⣹⠉⡏⠀\033[1;96m⠹⣾⣏⢹⣶⢹⣶⢿⡾⣿⢶⣿⣸⠾⣇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣾⢫⣞⡽⣯⢿⣹⡟⣶⣹⢷⣻\033[1;92m⡷⠊⠀⡜⠀⠀⠀⠀⢱⠀⣿⡀⠈⠢⢀⣀⣀⠠⠄⠒⢈⡏⡰⠀⠀⠀\033[1;96m⠀⣿⡜⣮⢟⡼⣻⡵⣻⣗⠾⣟⣯⢻⣆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣴⣿⢣⣟⡾⣽⣯⢳⣿⡹⣖⣿⡳\033[1;92m⠋⠀⠀⡸⠀⠀⠀⠀⠀⢸⠀⢺⢂⠀⠀⠀⠀⠀⠀⠀⢠⡺⡱⠁⠀⠀⠀⠀\033[1;96m⢹⣧⣻⢮⡳⣝⡷⢧⣻⢯⢿⣻⣳⢞⡆⠀⠀⠀
⠀⠀⠀⠀⢀⡾⣽⣣⡿⣼⣏⡿⣼⣳⡯⢷⣹⣯⠇\033[1;92m⠀⠀⢠⠁⠀⠀⠀⠀⠀⠈⡆⠈⢹⡰⠤⡀⠀⠀⠀⢠⡼⢱⠁⠀⠀⠀⠀⠀⠀\033[1;96m⠹⣿⣿⣱⣻⣼⣏⢷⣯⣿⡳⣿⣎⢿⡀⠀⠀
⠀⠀⠀⠀⣾⣽⠷⣿⣵⡿⣼⡟⣭⣷⡟⣿⢯⡏⠀\033[1;92m⠀⠀⠘⠀⠀⠒⠈⢡⠀⠀⢗⢄⠀⠃⠀⠺⢁⢈⠥⠋⣀⠇⠀⠀⠀⠀⠀⠀⡀⠀\033[1;96m⠈⠙⢿⣳⢞⣽⢯⣞⣾⣯⡝⣿⡾⡇⠀⠀\033[1;92mAuthor: github.com/Azumi67  \033[1;96m  ⠀⠀

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
            print("1. \033[36mExtra Native IPV6\033[0m")
            print("2. \033[93mEdit \033[92mMTU\033[0m")
            print("3. \033[92mIPIP6\033[0m")
            print("4. \033[96mPrivate IP\033[0m")
            print("5. \033[93mGRE\033[0m")
            print("6. \033[92mGRE6\033[0m")
            print("7. \033[96m6TO4 \033[0m")
            print("8. \033[93m6TO4 \033[97m[Anycasnt] \033[0m")
            print("9. \033[91mUninstall\033[0m")
            print("0. Exit")
            print("\033[93m╰─────────────────────────────────────────────────────────────────────╯\033[0m")

            choice = input("\033[5mEnter your choice Please: \033[0m")
            print("choice:", choice)
            if choice == '1':
                Native_menu()
            elif choice == '2':
                mtu_menu()   
            elif choice == '4':
                private_ip()
            elif choice == '3':
                ipip_menu()
            elif choice == '5':
                gre_menu()
            elif choice == '6':
                gre6_menu()
            elif choice == '7':
                i6to4_no()
            elif choice == '8':
                i6to4_any()
            elif choice == '9':
                remove_menu()
            elif choice == '0':
                print("Exiting...")
                break
            else:
                print("Invalid choice.")

            input("Press Enter to continue...")

    except KeyboardInterrupt:
        display_error("\033[91m\nProgram interrupted. Exiting...\033[0m")
        sys.exit()

def mtu_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mEdit MTU Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mPrivate IP\033[0m')
    print('2. \033[93mIP6IP6 \033[0m')
    print('3. \033[96mGRE \033[0m')
    print('4. \033[92mGRE6 \033[0m')
    print('5. \033[93m6to4 \033[0m')
    print('6. \033[96m6to4 anycast \033[0m')
    print('0. \033[94mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            private_mtu()
            break
        elif server_type == '2':
            ipip_mtu()
            break
        elif server_type == '3':
            gre_mtu()
            break
        elif server_type == '4':
            gre6_mtu()
            break
        elif server_type == '5':
            i6to4_mtu()
            break        
        elif server_type == '6':
            i6to4any_mtu()
            break
        elif server_type == '0':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')

def private_mtu():
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mPrivate IP \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"

    if os.path.exists("/etc/private.sh"):
        with open("/etc/private.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumi mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumi mtu" not in line]

            with open("/etc/private.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/private.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def gre6_mtu():
    private_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mGRE6 \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumig6 mtu {mtu_value}\n"

    if os.path.exists("/etc/gre6.sh"):
        with open("/etc/gre6.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumig6 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumig6 mtu" not in line]

            with open("/etc/gre6.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/gre6.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def gre_mtu():
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mGRE \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumig mtu {mtu_value}\n"

    if os.path.exists("/etc/gre.sh"):
        with open("/etc/gre.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumig mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumig mtu" not in line]

            with open("/etc/gre.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/gre.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")
        
def i6to4_mtu():
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96m6to4 \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumi6 mtu {mtu_value}\n"

    if os.path.exists("/etc/6to4.sh"):
        with open("/etc/6to4.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumi6 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumi6 mtu" not in line]

            with open("/etc/6to4.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/6to4.sh", "a") as file:
            file.write(mtu_command)

        display_checkmark("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def i6to4any_mtu():
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96m6to4 anycast \033[93m]:\033[0m ")
    mtu_command = f"/sbin/ip -6 link set dev azumi6 mtu {mtu_value}\n"

    if os.path.exists("/etc/6to4.sh"):
        with open("/etc/6to4.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumi6 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumi6 mtu" not in line]

            with open("/etc/6to4.sh", "w") as file:
                file.writelines(sh_contents)

        with open("/etc/6to4.sh", "a") as file:
            file.write(mtu_command)

        display_checkmark("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def ipip_mtu():
    
    private_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mIP6IP6 \033[93m]:\033[0m ")
    mtu_command = f"/sbin/ip -6 link set dev azumip mtu {mtu_value}\n"

    if os.path.exists("/etc/ipip.sh"):
        with open("/etc/ipip.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumip mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumip mtu" not in line]

            with open("/etc/ipip.sh", "w") as file:
                file.writelines(sh_contents)

        with open("/etc/ipip.sh", "a") as file:
            file.write(mtu_command)

        display_checkmark("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")
                
def ip_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIPIP Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ip_menu()
            break
        elif server_type == '2':
            iran_ip_menu()
            break
        elif server_type == '3':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')

def ip_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip.service'])
	
def ip_ping_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
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

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
	
def ip_iran():
    remote_ipv4 = input("\033[93mEnter \033[92mKharej IPv4\033[93m address [Ping Service]: \033[0m")
    
    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    sleep(1)
    

    ip_address = remote_prefix
    max_pings = 3
    interval = 30
    ip_ping_script(ip_address, max_pings, interval)
    ping_result = subprocess.run(['ping6', '-c', '2', remote_prefix], capture_output=True, text=True).stdout.strip()
    
    print(ping_result)

    ip_service()

    print("\033[92mIPIP6 Configuration Completed!\033[0m")
	
def ip_kharej():
    remote_ipv4 = input("\033[93mEnter \033[92mIran IPv4\033[93m address [Ping Service]: \033[0m")
    
    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    sleep(1)
    

    ip_address = remote_prefix
    max_pings = 3
    interval = 40
    ip_ping_script(ip_address, max_pings, interval)
    ping_result = subprocess.run(['ping6', '-c', '2', remote_prefix], capture_output=True, text=True).stdout.strip()
    
    print(ping_result)

    ip_service()

    print("\033[92mIPIP6 Configuration Completed!\033[0m")
	
## kharej ip
def server_ipv4():

    command = "curl -s https://api.ipify.org"
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print("Error retrieving server's IPv4 address.")
        return None
    ipv4 = process.stdout.strip()
    return ipv4

def kharej_ip_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIPIP \033[92mKharej\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    file_path = '/etc/ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPv4 address: \033[0m")


    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")

 

    num_additional_ips = int(input("Enter the number of additional IPv6 addresses: "))
    

    command = f"echo '/sbin/modprobe sit' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip tunnel add azumii mode ipip remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip addr add {ipv6}/16 dev azumii' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    

    for i in range(2, num_additional_ips + 2):
        ip_address = f"{ipv6[:-1]}{i}/16"  
        command = f"echo 'ip addr add {ip_address} dev azumii' >> {file_path}"
        subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip link set azumii up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)


   
    config_file_path = '/etc/ip.sh'
 
    subprocess.run(f"(crontab -l | grep -v -F '{file_path}') | crontab -", shell=True, check=True)

   
    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)

    print("GRE tunnel created and configured successfully.")
    print("Configuration saved to /etc/ip.sh.")
    print("Cronjob added to execute /etc/ip.sh on every reboot.")

    ip_kharej()
	
# iran ip

def iran_ip_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIPIP \033[92mIRAN\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    file_path = '/etc/ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPv4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address: \033[0m")


    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")



    num_additional_ips = int(input("Enter the number of additional IPv6 addresses: "))
    
    command = f"echo '/sbin/modprobe sit' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip tunnel add azumii mode ipip remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip addr add {ipv6}/16 dev azumii' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    

    for i in range(2, num_additional_ips + 2):
        ip_address = f"{ipv6[:-1]}{i}/16" 
        command = f"echo 'ip addr add {ip_address} dev azumii' >> {file_path}"
        subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip link set azumii up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)


    config_file_path = '/etc/ip.sh'

    subprocess.run(f"(crontab -l | grep -v -F '{file_path}') | crontab -", shell=True, check=True)


    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)

    print("GRE tunnel created and configured successfully.")
    print("Configuration saved to /etc/ip.sh.")
    print("Cronjob added to execute /etc/ip.sh on every reboot.")
    ip_iran()
    
###menu ipip		
def ipip_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIPIP Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipip6_menu()
            break
        elif server_type == '2':
            iran_ipip6_menu()
            break
        elif server_type == '3':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')
            
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
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', errors='replace')

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
                 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⢀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⡀⠤⠒⠊⠉⠀⠀⠀⠀⠈⠁⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀\033[1;93m⠀⢀⠔⠉⠀⠀⠀⠀⢀⡠⠤⠐⠒⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⣀⡠⠤⠤⠀⠀⠂⠐\033[1;96m⠀⠠⢤⠎⢑⡭⣽⣳⠶⣖⡶⣤⣖⣬⡽⡭⣥⣄\033[1;93m⠒⠒⠀⠐⠁⠑⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⢀⠴⠊⠁⠀⠀⠀⠀⡀⠀\033[1;96m⣠⣴⡶⣿⢏⡿⣝⡳⢧⡻⣟⡻⣞⠿⣾⡽⣳⣯⣳⣞⡻⣦⡀⠀⠀\033[1;93m⠀⠈⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢨⠀⠀⠀⢀⠤⠂⠁\033[1;96m⢠⣾⡟⣧⠿⣝⣮⣽⢺⣝⣳⡽⣎⢷⣫⡟⡵⡿⣵⢫⡷⣾⢷⣭⢻⣦⡄\033[1;93m⠤⡸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠘⡄⠀⠀⠓⠂⠀\033[1;96m⣴⣿⢷⡿⣝⣻⣏⡷⣾⣟⡼⣣⢟⣼⣣⢟⣯⢗⣻⣽⣏⡾⡽⣟⣧⠿⡼⣿⣦\033[1;93m⣃⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢀⠇⠀⠀⠀⠀\033[1;96m⣼⣿⢿⣼⡻⣼⡟⣼⣧⢿⣿⣸⡧⠿⠃⢿⣜⣻⢿⣤⣛⣿⢧⣻⢻⢿⡿⢧⣛⣿⣧⠀\033[1;93m⠛⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⢸⠁⠀⠀⠀⠀\033[1;96m⣼⣻⡿⣾⣳⡽⣾⣽⡷⣻⣞⢿⣫⠕⣫⣫⣸⢮⣝⡇⠱⣏⣾⣻⡽⣻⣮⣿⣻⡜⣞⡿⣷\033[1;93m⢀⠀⠀⠑⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠘⣧⠀⠀⠀\033[1;96m⣼⣳⢯⣿⣗⣿⣏⣿⠆⣟⣿⣵⢛⣵⡿⣿⣏⣟⡾⣜⣻⠀⢻⡖⣷⢳⣏⡶⣻⡧⣟⡼⣻⡽⣇\033[1;93m⠁⠢⡀⠠⡀⠑⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠈⢦⠀\033[1;96m⣰⣯⣟⢯⣿⢾⣹⢾⡟⠰⣏⡾⣾⣟⡷⣿⣻⣽⣷⡶⣟⠿⡆⠀⢻⣝⣯⢷⣹⢧⣿⢧⡻⣽⣳⢽⡀\033[1;93m⠀⠈⠀⠈⠂⡼⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⡀⢵\033[1;96m⣟⣾⡟⣾⣿⣻⢽⣺⠇⠀⣿⡱⢿⡞⣵⡳⣭⣿⡜⣿⣭⣻⣷⠲⠤⢿⣾⢯⢯⣛⢿⣳⡝⣾⣿⢭⡇⠀\033[1;93m⠀⠀⠀⡰⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢀⠤⠊⠀\033[1;96m⣼⢻⣿⢞⣯⢿⡽⣸⣹⡆⠀⢷⣏⢯⣿⣧⣛⠶⣯⢿⣽⣷⣧⣛⣦⠀⠀⠙⢿⣳⣽⣿⣣⢟⡶⣿⣫⡇⠀⠀\033[1;93m⠀⠰⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⣠⠖⠁⠀⠀⡄\033[1;96m⡿⣯⣷⣻⡽⣞⡟⣿⣿⣟⠉⠈⢯⣗⣻⣕⢯⣛⡞⣯⢮⣷⣭⡚⠓⠋⠀⠀⠀⠈⠉⣿⡽⣎⠷⡏⡷⣷⠀⠀⠀\033[1;93m⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠐⣇⠀⠀⢀⠊\033[1;96m⣼⣇⣿⡗⣿⣽⣷⡿⣿⣱⡿⣆⠀⠀⠙⠒⠛⠓⠋⠉⠉⠀⠀⠀\033[1;91m⢠⣴⣯⣶⣶⣤⡀\033[1;96m ⠀⣿⣟⡼⣛⡇⣟⣿⡆\033[1;93m⡀⠀⢀⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠘⢤⠀⠃⠌\033[1;96m⣸⣿⢾⡽⣹⣾⠹⣞⡵⣳⣽⡽⣖⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;91m⣤⣖⣻⣾⣝⢿⡄\033[1;96m ⢸⣯⢳⣏⡿⣏⣾⢧\033[1;93m⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠘⠀⠈⠀\033[1;96m⡿⣿⣻⡽⣽⣿⢧⠌⠉\033[1;91m⠉⣴⣿⣿⣫⣅⡀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣛⠿⠿⢟⢙⡄⠙\033[1;96m ⠘⣯⢳⣞⡟⣯⢾⣻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⡇⠀⠀⠀\033[1;96m⡿⣿⣿⢵⣫⣿⣆⠁⠂\033[1;91m⣼⡿⢹⣿⡿⠽⠟⢢⠀⠀⠀⠀⠀⠀⠀⢹⠀⢄⢀⠀⡿⠀⠀\033[1;96m ⢰⣯⢷⣺⣏⣯⢻⡽⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⡇⠀⢀⠠\033[1;96m⣿⣿⢾⣛⡶⣽⠈⢓⠀\033[1;91m⢻⠁⢸⠇⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠑⠠⠤⠔⠂⠀⠀\033[1;96m ⢸⣿⢮⣽⠿⣜⣻⡝⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠑⠊⠁\033[1;96m⢠⡷⡇⣿⣿⢼⣹⡀⠀⠑⢄⠀\033[1;91m⠀⠃⠌⣁⠦⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠂⠀⠀\033[1;96m⢀⣿⢾⡝⣾⡽⣺⢽⣹⣽⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣻⢽⣻⡟⣮⣝⡷⢦⣄⣄⣢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣯⢿⡺⣟⢷⡹⢾⣷⡞⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣟⡿⣎⢿⡽⣳⢮⣿⣹⣾⣯⡝⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⣀⣴⡟⣿⢧⣏⢷⡟⣮⠝⢿⣹⣯⡽⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣯⡷⣏⣾⡳⣽⢺⣷⡹⣟⢶⡹⣾⡽⣷⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠔⣾⢯⣷⡇⣿⢳⣎⢿⡞⣽⢦⣼⡽⣧⢻⡽⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣟⢾⡷⣭⣿⢳⣭⢻⣷⡻⣜⣻⡵⣻⡼⣿⠾⠫\033[1;96m⣽⣟⣶⣶⣶⠒⠒⠂⠉⠀\033[1;96m⢸⣽⢺⡷⣷⣯⢗⣮⣟⢾⢧⣻⠼⡿⣿⢣⡟⣼⣆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⣝⣾⢳⢧⣟⡳⣎⣿⣿⣱⢏⣾⣽⣳⠟\033[1;92m⠁⠀⡌⠈\033[1;96m⢹⡯⠟⠛⠀⠀⠀⠀⠀⠈\033[1;96m⣷⢻⣼⣽⣿⡾⣼⣏⣾⣻⡜⣯⣷⢿⣟⣼⡳⣞⣦⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⢿⡸⣎⠿⣾⡏⣷⣉⣷⣿⢹⣎⡿\033[1;92m⠎⡎⠀⠀⠀⡇⠀⣾⠱⡀⠀⠀⠀⠀⠀⠀⠀⠈⣹⠉⡏⠀\033[1;96m⠹⣾⣏⢹⣶⢹⣶⢿⡾⣿⢶⣿⣸⠾⣇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣾⢫⣞⡽⣯⢿⣹⡟⣶⣹⢷⣻\033[1;92m⡷⠊⠀⡜⠀⠀⠀⠀⢱⠀⣿⡀⠈⠢⢀⣀⣀⠠⠄⠒⢈⡏⡰⠀⠀⠀\033[1;96m⠀⣿⡜⣮⢟⡼⣻⡵⣻⣗⠾⣟⣯⢻⣆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣴⣿⢣⣟⡾⣽⣯⢳⣿⡹⣖⣿⡳\033[1;92m⠋⠀⠀⡸⠀⠀⠀⠀⠀⢸⠀⢺⢂⠀⠀⠀⠀⠀⠀⠀⢠⡺⡱⠁⠀⠀⠀⠀\033[1;96m⢹⣧⣻⢮⡳⣝⡷⢧⣻⢯⢿⣻⣳⢞⡆⠀⠀⠀
⠀⠀⠀⠀⢀⡾⣽⣣⡿⣼⣏⡿⣼⣳⡯⢷⣹⣯⠇\033[1;92m⠀⠀⢠⠁⠀⠀⠀⠀⠀⠈⡆⠈⢹⡰⠤⡀⠀⠀⠀⢠⡼⢱⠁⠀⠀⠀⠀⠀⠀\033[1;96m⠹⣿⣿⣱⣻⣼⣏⢷⣯⣿⡳⣿⣎⢿⡀⠀⠀
⠀⠀⠀⠀⣾⣽⠷⣿⣵⡿⣼⡟⣭⣷⡟⣿⢯⡏⠀\033[1;92m⠀⠀⠘⠀⠀⠒⠈⢡⠀⠀⢗⢄⠀⠃⠀⠺⢁⢈⠥⠋⣀⠇⠀⠀⠀⠀⠀⠀⡀⠀\033[1;96m⠈⠙⢿⣳⢞⣽⢯⣞⣾⣯⡝⣿⡾⡇⠀⠀\033[1;92mAuthor: github.com/Azumi67  \033[1;96m  ⠀⠀

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
            display_notification("\033[92m[7] \033[96mKharej \033[92m[1] \033[93mIRAN\033[0m")
            print("\033[93m─────────────────────────────────────────── \033[0m")
            print("5. \033[96mChisel \033[92mTCP \033[96m[IPV4] \033[92m[7] \033[96mKHAREJ\033[92m [1] \033[96mIRAN")
            print("\033[97m6. \033[96mChisel \033[92mUDP \033[96m[IPV4] \033[92m[7] \033[96mKHAREJ\033[92m [1] \033[96mIRAN")
            
            print("\033[97m7. \033[93mChisel \033[92mTCP \033[93m[IPV6] \033[92m[7] \033[93mKHAREJ\033[92m [1] \033[93mIRAN")
            print("\033[97m8. \033[93mChisel \033[92mUDP \033[93m[IPV6] \033[92m[7] \033[93mKHAREJ\033[92m [1] \033[93mIRAN")
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
    print('6. \033[93mKharej\033[92m [6] \033[0m')
    print('7. \033[93mKharej\033[92m [7] \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('8. \033[96mIRAN \033[0m')
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
            kharej_ipv4()
            break
        elif server_type == '7':
            kharej_ipv4()
            break
        elif server_type == '8':
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
    print('6. \033[93mKharej\033[92m [6] \033[0m')
    print('7. \033[93mKharej\033[92m [7] \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('8. \033[96mIRAN \033[0m')
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
            kharej_ipv6()
            break
        elif server_type == '7':
            kharej_ipv6()
            break
        elif server_type == '8':
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
    print('6. \033[93mKharej\033[92m [6] \033[0m')
    print('7. \033[93mKharej\033[92m [7] \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('8. \033[96mIRAN \033[0m')
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
            kharej_ipv4_udp()
            break
        elif server_type == '7':
            kharej_ipv4_udp()
            break
        elif server_type == '8':
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
    print('6. \033[93mKharej\033[92m [6] \033[0m')
    print('7. \033[93mKharej\033[92m [7] \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('8. \033[96mIRAN \033[0m')
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
            kharej_ipv6_udp()
            break
        elif server_type == '7':
            kharej_ipv6_udp()
            break
        elif server_type == '8':
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

    display_loading()

    display_notification("\033[93mDownloading Chisel...\033[0m")
    download_result = subprocess.run(f"wget --quiet --show-progress {chisel_download_url} -O {chisel_directory_name}.gz", shell=True)
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
        display_error("\033[91mError occurred during Chisel installation: {}\033[0m".format(str(e)))
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
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

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
    res_chisel2()

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
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

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
            res_chisel3()
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
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

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
    res_chisel1()
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
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

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
    res_chisel2()
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
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)
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
            res_chisel3()
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
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

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
    res_chisel1()
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
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

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
    res_chisel2()
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
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

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
    res_chisel1()
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
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)
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
            res_chisel3()
            print("\033[93m╭──────────────────────────────────────────────────────────────────────╮\033[0m")
            for j, config_port in enumerate(configs, start=1):
                print(f"\033[93m| Server {i} - Config {j}: Your Address & Port: {iran_ipv4} : {config_port}  \033[0m")
            print("\033[93m╰──────────────────────────────────────────────────────────────────────╯\033[0m")

            server_configs.append((iran_ipv4, configs))

        return server_configs

    server_configs = kharej_ipv6_udp()

    return server_configs
    
def res_chisel3():
    delete_cron()
    if subprocess.call("test -f /etc/reschisel.sh", shell=True) == 0:
        subprocess.call("rm /etc/reschisel.sh", shell=True)

    with open("/etc/reschisel.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("systemctl daemon-reload\n")
        f.write("sudo sync; echo 1 > /proc/sys/vm/drop_caches\n")
        f.write("sudo journalctl --vacuum-size=1M\n")
        print("\033[93m────────────────────────\033[0m") 
        num_configs = int(input("\033[93mEnter\033[92m number of configs\033[93m[For 2 Hours Reset timer]:\033[0m "))
        for i in range(1, num_configs + 1):
            f.write(f"systemctl restart kharej_1_{i}\n")  
            f.write(f"systemctl restart kharej_2_{i}\n") 
            f.write(f"systemctl restart kharej_3_{i}\n")
            f.write(f"systemctl restart kharej_4_{i}\n")
            f.write(f"systemctl restart kharej_5_{i}\n")            

    subprocess.call("chmod +x /etc/reschisel.sh", shell=True)
    hours = "2"
    cron_entry = f"0 */{hours} * * * /etc/reschisel.sh"
    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        display_error("\033[91mNo existing cron found!\033[0m")

    new_crontab = f"{existing_crontab.rstrip()}\n{cron_entry}"
    try:
        subprocess.check_output(f'echo "{new_crontab}" | crontab -', shell=True)
        print("Cron entry added successfully!")
    except subprocess.CalledProcessError as e:
        display_error(f"Failed to add cron entry. Error: {e}")
        
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
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)
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
            res_chisel3()
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

def res_chisel2():
    delete_cron()
    if subprocess.call("test -f /etc/reschisel.sh", shell=True) == 0:
        subprocess.call("rm /etc/reschisel.sh", shell=True)

    with open("/etc/reschisel.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart iran_1\n")
        f.write("sudo sync; echo 1 > /proc/sys/vm/drop_caches\n")
        f.write("sudo journalctl --vacuum-size=1M\n")

    subprocess.call("chmod +x /etc/reschisel.sh", shell=True)
    hours = "2"
    cron_entry = f"0 */{hours} * * * /etc/reschisel.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        display_error("\033[91mNo existing cron found!\033[0m")

    new_crontab = f"{existing_crontab.rstrip()}\n{cron_entry}"
    try:
        subprocess.check_output(f'echo "{new_crontab}" | crontab -', shell=True)
        print("Cron entry added successfully!")
    except subprocess.CalledProcessError as e:
        display_error(f"Failed to add cron entry. Error: {e}")
        
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
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

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
    res_chisel2()

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
    
        
def res_chisel1():
    delete_cron()
    if subprocess.call("test -f /etc/reschisel.sh", shell=True) == 0:
        subprocess.call("rm /etc/reschisel.sh", shell=True)

    with open("/etc/reschisel.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("systemctl daemon-reload\n")
        f.write("sudo sync; echo 1 > /proc/sys/vm/drop_caches\n")
        f.write("sudo journalctl --vacuum-size=1M\n")
        print("\033[93m────────────────────────\033[0m") 
        num_configs = int(input("\033[93mEnter\033[92m number of configs\033[93m[For 2 Hours Reset timer]:\033[0m "))
        for i in range(1, num_configs + 1):
            config_name = f"kharej_{i}"
            f.write(f"systemctl restart {config_name}\n")

    subprocess.call("chmod +x /etc/reschisel.sh", shell=True)
    hours = "2"
    cron_entry = f"0 */{hours} * * * /etc/reschisel.sh"
    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        display_error("\033[91mNo existing cron found!\033[0m")

    new_crontab = f"{existing_crontab.rstrip()}\n{cron_entry}"
    try:
        subprocess.check_output(f'echo "{new_crontab}" | crontab -', shell=True)
        print("Cron entry added successfully!")
    except subprocess.CalledProcessError as e:
        display_error(f"Failed to add cron entry. Error: {e}")
        
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
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

        display_checkmark("\033[92mKharej service {} started successfully!\033[0m".format(config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)

        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating Kharej service {}. Error: {}\033[0m".format(config_number, e.output))

def delete_cron():
    entries_to_delete = [
        "0 */2 * * * /etc/reschisel.sh"
    ]

    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        display_error("\033[91mNo existing cron found!\033[0m")
        return

    new_crontab = existing_crontab
    for entry in entries_to_delete:
        if entry in existing_crontab:
            new_crontab = new_crontab.replace(entry, "")

    if new_crontab != existing_crontab:
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_notification("\033[92mDeleting Previous Crons..\033[0m")
    else:
        print("\033[91mCron doesn't exists, moving on..!\033[0m")        
        
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
    res_chisel1()
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
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping.service'])
    subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/ping.service'])
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
    with open("/etc/chi.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumich mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumich up\n")
        f.write("ip addr add fd1d:fc98:b63e:b481::1/64 dev azumich\n")
        f.write("ip -6 route add fd1d:fc98:b63e:b481::2/64 dev azumich\n")

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
        f.write("ip -6 route add fd1d:fc98:b63e:b481::1/64 dev azumich\n")

    
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
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

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
    res_chisel2()
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
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

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
    res_chisel1()
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    for i in range(num_configs):
        print(f"\033[93m| Config {i+1} - Your Address & Port: {remote_ip} : {server_ports[i]}  \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    return server_ports
        
		
        
        
def iran_udp3(key_path, tunnel_port=443):
    service_name = "iran_1"
    service_file = "/etc/systemd/system/iran_1.service"
    chisel_command = f"./chisel server --keyfile {key_path} --reverse --port {tunnel_port} --host [fd1d:fc98:b63e:b481::2] --keepalive 25s"

    service_content = f"""[Unit]
Description=Chisel Service IRAN
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

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
    res_chisel2()
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
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

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
    res_chisel1()
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
        'kharej': 'kharej_1',
        'kharej': 'kharej_2',
        'kharej': 'kharej_3',
        'kharej': 'kharej_4',
        'kharej': 'kharej_5'
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
    delete_cron()

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
    delete_cron()

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
    delete_cron()
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



   
#sit kharej
def kharej_ipip6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IPIP6 \033[92mKharej\033[93m server\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "fd1d:fc98:b73e:b481::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip addr add fd1d:fc98:b73e:b481::1/64 dev azumi\n")
        f.write("ip -6 route add fd1d::/16 dev azumi\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    


    sleep(1)
    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping()
    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="fd1d:fc98:b73e:b481::2"

max_pings=3

interval=40

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

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()
    
    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip_kharej()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")



    
 ##### IRAN IPIP6
def iran_ping():
    try:
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b73e:b481::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
    
	
def display_iran_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "fd1d:fc98:b73e:b481::2"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    
		

##ipip6 iran


def iran_ipip_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip.service'])


def ipip6_iran_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/ipip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as f:
        f.write('/sbin/modprobe ipip\n')
        f.write(f'ip -6 tunnel add azumip mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255\n')
        f.write('ip -6 addr add 2002:0db8:1234:a220::2/64 dev azumip\n')
        f.write('ip link set azumip up\n')
        f.write('ip -6 route add 2002::/16 dev azumip\n')
        created_ips = []
        for i in range(2, num_additional_ips + 2):
            ip_address = f'2002:0db8:1234:a22{i}::2'
            created_ips.append(ip_address)
            f.write(f'ip -6 addr add {ip_address}/64 dev azumip\n')

        

    command = f'chmod +x {file_path}'
    subprocess.run(command, shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [IP6IP6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumip mtu {mtu_value}'
        with open('/etc/ipip.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(command, shell=True, check=True)

    subprocess.run(f'bash {file_path}', shell=True, check=True)
    


    print('\033[93mCreated IPv6 Addresses:\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')
    print('\033[92m' + '| 2002:0db8:1234:a220::1    |' + '\033[0m')
    for ip_address in created_ips:
        print('\033[92m' + f'| {ip_address}    |' + '\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')



def ipip_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/ipip.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/ipip.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)


def iran_ping_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
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

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def ipip_iran():
    remote_ip = "fd1d:fc98:b73e:b481::1" #kharej-ip
    local_ip = "fd1d:fc98:b73e:b481::2"   #iran ip
    num_additional_ips = int(input("\033[93mHow many \033[92madditional ips\033[93m do you need? \033[0m"))
    ipip6_iran_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:0db8:1234:a220::1" #kharejip
    max_pings = 3
    interval = 60
    iran_ping_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_ipip_service()

    ipip_cronjob()
   
    display_checkmark("\033[92mIPIP6 Configuration Completed!\033[0m")

   
#sit iran
def iran_ipip6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IPIP6 \033[92mIran\033[93m server\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "fd1d:fc98:b73e:b481::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip addr add fd1d:fc98:b73e:b481::2/64 dev azumi\n")
        f.write("ip -6 route add fd1d::/16 dev azumi\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    


    sleep(1)
    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping()


    script_content1 = '''#!/bin/bash


ip_address="fd1d:fc98:b73e:b481::1"

max_pings=3

interval=38

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

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()

    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip_iran()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")


    
    
    ##### PRIVATE & NATIVE
    
       
def private_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mPrivate IP Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_private_menu()
            break
        elif server_type == '2':
            iran_private_menu()
            break
        elif server_type == '3':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')
        
def add_cron_job():
    try:
        subprocess.run(
            "echo '@reboot /bin/bash /etc/private.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)
        
def run_ping():
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b73e:b481::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
 
def run_ping_iran():
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b73e:b481::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def ping_v6_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v6.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_v6.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v6.service'])
    subprocess.run(['systemctl', 'start', 'ping_v6.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_v6.service'])
    
        

            
def kharej_private_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Kharej server\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  There is also a cronjob and a ping service that automatically installs")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "fd1d:fc98:b73e:b481::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "fd1d::/16", "dev", "azumi"], stdout=subprocess.DEVNULL)

    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"fd1d:fc98:b73e:b48{ip_suffix}::1/64"

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip addr add fd1d:fc98:b73e:b481::1/64 dev azumi\n")
        f.write("ip -6 route add fd1d::/16 dev azumi\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"fd1d:fc98:b73e:b48{ip_suffix}::1/64"
            f.write(f"ip addr add {ip_addr} dev azumi\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")

    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"fd1d:fc98:b73e:b48{ip_suffix}::1"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")


    script_content1 = '''#!/bin/bash


ip_address="fd1d:fc98:b73e:b481::2"


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

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()

    
    print("\033[92mKharej Server Configuration Completed!\033[0m")

def iran_private_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Iran server\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  There is also a cronjob and a ping service that automatically installs")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")
    
    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")
    

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    
    
    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)
    
    
    initial_ip = "fd1d:fc98:b73e:b481::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "fd1d::/16", "dev", "azumi"], stdout=subprocess.DEVNULL)
    
   
    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
    
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"fd1d:fc98:b73e:b48{ip_suffix}::2/64"
        

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi"], stdout=subprocess.DEVNULL)
    

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip addr add fd1d:fc98:b73e:b481::2/64 dev azumi\n")
        f.write("ip -6 route add fd1d::/16 dev azumi\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"fd1d:fc98:b73e:b48{ip_suffix}::2/64"
            f.write(f"ip addr add {ip_addr} dev azumi\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    


    add_cron_job()

    sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
   
    run_ping_iran()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (IRAN):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"fd1d:fc98:b73e:b48{ip_suffix}::2"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")
    


    script_content = '''#!/bin/bash


ip_address="fd1d:fc98:b73e:b481::2"


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


    with open('/etc/ping_v6.sh', 'w') as script_file:
        script_file.write(script_content)


    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()

## Native

def Native_menu():
    subprocess.run("clear", shell=True)
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93mNative IP Menu\033[0m")
    print("\033[92m \"-\"\033[93m═════════════════════\033[0m")
    display_logo2()
    print("\033[93m.-------------------------------------------------------------------------------------------------------.\033[0m")
    print("\033[93m| \033[92mIf it didn't work, please uninstall it and add extra IP manually  \033[0m")
    print("\033[93m|\033[0m  If you don't have native IPv6, please use a private IP instead.                                             \033[0m")
    print("\033[93m'-------------------------------------------------------------------------------------------------------'\033[0m")
    display_notification("\033[93mAdding extra Native IPv6 [Kharej]...\033[0m")
    print("\033[93m╭──────────────────────────────────────────────────────────╮\033[0m")

    try:
        interface = subprocess.run("ip route | awk '/default/ {print $5; exit}'", shell=True, capture_output=True, text=True).stdout.strip()
        ipv6_addresses = subprocess.run(f"ip -6 addr show dev {interface} | awk '/inet6 .* global/ {{print $2}}' | cut -d'/' -f1", shell=True, capture_output=True, text=True).stdout.strip().split('\n')

        print("\033[92mCurrent IPv6 addresses on", interface + ":\033[0m")
        for address in ipv6_addresses:
            print(address)

        confirm = input("\033[93mAre these your current IPv6 addresses? (y/n): \033[0m")
        if confirm.lower() != "y":
            display_error("\033[91mAborted. Please manually configure the correct IPv6 addresses.\033[0m")
            return

        sorted_addresses = sorted(ipv6_addresses, reverse=True)
        additional_address = ""
        for i in range(len(sorted_addresses)):
            current_last_part = sorted_addresses[i].split(':')[-1]
            modified_last_part_hex = format(int(current_last_part, 16) + 1, '04x')
            modified_address = ":".join(sorted_addresses[i].split(':')[:-1]) + ":" + modified_last_part_hex

            if modified_address not in sorted_addresses:
                additional_address = modified_address
                break

        if not additional_address:
            display_error("\033[91mNo additional address to add.\033[0m")
            return

        subprocess.run(["ip", "addr", "add", f"{additional_address}/64", "dev", interface])

        script_file = "/etc/ipv6.sh"
        with open(script_file, "a") as file:
            file.write(f"ip addr add {additional_address}/64 dev {interface}\n")

        subprocess.run(["chmod", "+x", script_file])

        subprocess.run("crontab -l | grep -v '/etc/ipv6.sh' | crontab -", shell=True)

        display_notification("\033[93mAdding cronjob for the server..\033[0m")
        subprocess.run("(crontab -l 2>/dev/null; echo \"@reboot /bin/bash /etc/ipv6.sh\") | crontab -", shell=True)

        display_checkmark("\033[92mIPv6 addresses added successfully!\033[0m")
    except ValueError as e:
        display_error("\033[91mAn error occurred while adding IPv6 addresses:", str(e), "\033[0m")
        
###menu gre		
def gre_gre6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGRE | GRE6 Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mGRE\033[0m')
    print('2. \033[93mGRE6 \033[0m')
    print('3. \033[94mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            gre_menu()
            break
        elif server_type == '2':
            gre6_menu()
            break
        elif server_type == '3':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')
			
def gre_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGRE Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mback to main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_gre_menu()
            break
        elif server_type == '2':
            iran_gre_menu()
            break
        elif server_type == '3':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')
			
def gre6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGRE6 Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mback to main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_gre6_menu()
            break
        elif server_type == '2':
            iran_gre6_menu()
            break
        elif server_type == '3':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')
			
   ##gre6         
def run_ping():
    try:
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b73e:b481::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def ping_v6_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v6.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_v6.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v6.service'])
    subprocess.run(['systemctl', 'start', 'ping_v6.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_v6.service'])
    

	
def display_kharej_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "fd1d:fc98:b73e:b481::1"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
		

def add_cron_job():
    file_path = '/etc/private.sh'

    try:
       
        subprocess.run(
            f"(crontab -l | grep -v '{file_path}') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )

        
        subprocess.run(
            f"(crontab -l ; echo '@reboot /bin/bash {file_path}') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )

        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)

##gre6 kharej

def gre6_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/gre6.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/gre6.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)
		
def ping_gre6_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip.service'])

def gre6_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/gre6.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig6 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:831a::1/64 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig6 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:83{i}a::1"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumig6' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumig6 mtu {mtu_value}'
        with open('/etc/gre6.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(command, shell=True, check=True)
    sleep(1)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    
    print("\033[93mCreated IPv6 Addresses:\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:831a::1               |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}               |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")


def create_ping_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
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

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def gre6_kharej():
    remote_ip = "fd1d:fc98:b73e:b481::2" #iran-ip
    local_ip = "fd1d:fc98:b73e:b481::1"   #kharej ip
    num_additional_ips = int(input("\033[97mEnter the number of \033[92madditional IPs\033[97m for the \033[92mGRE6\033[97m tunnel: "))
    gre6_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:831a::2" #iranip
    max_pings = 3
    interval = 47
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    create_ping_script(ip_address, max_pings, interval)
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    ping_gre6_service()

    gre6_cronjob()
   
    

   
#sit kharej
def kharej_gre6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring GRE \033[92mKharej\033[93m server\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "fd1d:fc98:b73e:b481::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip addr add fd1d:fc98:b73e:b481::1/64 dev azumi\n")
        f.write("ip -6 route add fd1d::/16 dev azumi\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)

    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    sleep(1)
    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping()
    sleep(1)
    


    script_content1 = '''#!/bin/bash


ip_address="fd1d:fc98:b73e:b481::2"

max_pings=3

interval=40

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

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()
    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    display_checkmark("\033[92mGRE6 Configuration Completed!\033[0m")
    gre6_kharej()
    sleep(1)	
    
    
 ##### IRAN gre6
def iran_ping():
    try:
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b73e:b481::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
    
	
def display_iran_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "fd1d:fc98:b73e:b481::2"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
		


def iran_gre6_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip.service'])

def gre6_iran_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/gre6.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig6 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:831a::2/64 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig6 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:83{i}a::2"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumig6' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumig6 mtu {mtu_value}'
        with open('/etc/gre6.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(command, shell=True, check=True)
    sleep(1)
    subprocess.run(f"bash {file_path}", shell=True, check=True)

    print("\033[93mCreated IPv6 Addresses:\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:831a::2               |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}               |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")



def iran_ping_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
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

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    

def gre6_iran():
    remote_ip = "fd1d:fc98:b73e:b481::1" #kharej ip
    local_ip = "fd1d:fc98:b73e:b481::2"   #iran ip
    num_additional_ips = int(input("\033[97mEnter the number of \033[92madditional IPs\033[97m for the \033[92mGRE6\033[97m tunnel: "))
    gre6_iran_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:831a::1" #kharejip
    max_pings = 3
    interval = 50
    iran_ping_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_gre6_service()

    gre6_cronjob()
   
   

   
#sit iran
def iran_gre6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring GRE \033[92mIran\033[93m server\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "fd1d:fc98:b73e:b481::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip addr add fd1d:fc98:b73e:b481::2/64 dev azumi\n")
        f.write("ip -6 route add fd1d::/16 dev azumi\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)

    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    sleep(1)
    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping()
    

    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="fd1d:fc98:b73e:b481::1"

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

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()

    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    gre6_iran()
    sleep(1)	
    display_checkmark("\033[92mGRE6 Configuration Completed!\033[0m")
	
## gre
def gre_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip.service'])
	
def gre_ping_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
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

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
	
def gre_iran():
    remote_ipv4 = input("\033[93mEnter \033[92mKharej IPv4\033[93m address [Ping Service]: \033[0m")
    
    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    sleep(1)
    

    ip_address = remote_prefix
    max_pings = 3
    interval = 30
    gre_ping_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', remote_prefix], capture_output=True, text=True).stdout.strip()
    
    print(ping_result)

    gre_service()


	
def gre_kharej():
    remote_ipv4 = input("\033[93mEnter \033[92mIran IPv4\033[93m address [Ping Service]: \033[0m")
    
    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    sleep(1)
    

    ip_address = remote_prefix
    max_pings = 3
    interval = 40
    gre_ping_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', remote_prefix], capture_output=True, text=True).stdout.strip()
    
    print(ping_result)

    gre_service()

	
## kharej gre
def server_ipv4():

    command = "curl -s https://api.ipify.org"
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print("Error retrieving server's IPv4 address.")
        return None
    ipv4 = process.stdout.strip()
    return ipv4

def kharej_gre_menu():
    clear_screen()
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGRE \033[92mKharej\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[97m  For ping service, enter \033[92mIRAN\033[97m IPV4 address")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    file_path = '/etc/gre.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────╮\033[0m")
    
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPv4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────╯\033[0m")

    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")



    num_additional_ips = int(input("Enter the number of \033[92madditional IPv6\033[93m addresses: "))
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    

    command = f"echo '/sbin/modprobe gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip tunnel add azumig mode gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip addr add {ipv6}/16 dev azumig' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    

    for i in range(2, num_additional_ips + 2):
        ip_address = f"{ipv6[:-1]}{i}/16"  
        command = f"echo 'ip addr add {ip_address} dev azumig' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumig mtu {mtu_value}'
        with open('/etc/gre.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)



    config_file_path = '/etc/gre.sh'

    subprocess.run(f"(crontab -l | grep -v -F '{file_path}') | crontab -", shell=True, check=True)


    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)

    display_checkmark("\033[92mGRE Configuration Completed!\033[0m")



    gre_kharej()
	
# iran gre

def iran_gre_menu():
    clear_screen()
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGRE \033[92mIRAN\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[97m  For ping service, enter \033[92mKharej\033[97m IPV4 address")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    file_path = '/etc/gre.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────╮\033[0m")
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPv4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────╯\033[0m")


    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")



    num_additional_ips = int(input("Enter the number of \033[92madditional IPv6\033[93m addresses: "))
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    command = f"echo '/sbin/modprobe gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip tunnel add azumig mode gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip addr add {ipv6}/16 dev azumig' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    

    for i in range(2, num_additional_ips + 2):
        ip_address = f"{ipv6[:-1]}{i}/16"  
        command = f"echo 'ip addr add {ip_address} dev azumig' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumig mtu {mtu_value}'
        with open('/etc/gre.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)

 
    config_file_path = '/etc/gre.sh'

    subprocess.run(f"(crontab -l | grep -v -F '{file_path}') | crontab -", shell=True, check=True)

  
    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)

    display_checkmark("\033[92mGRE Configuration Completed!\033[0m")
    gre_iran()
    
def clear_screen():
    os.system("clear")
    
def i6to4_menu():
    clear_screen()
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(O,O)\033[0m')
    print('\033[92m(   ) \033[93m6TO4 Menu\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════\033[0m')
    
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92m6to4 \033[0m')
    print('2. \033[93m6to4 Anycast\033[0m')
    print('3. \033[94mback to main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    server_type = input("\033[38;5;205mEnter your choice Please: \033[0m")

    if server_type == '1':
        i6to4_no()
    elif server_type == '2':
        i6to4_any()
    elif server_type == '3':
        clear_screen()
        main_menu()
    else:
        print("Invalid choice.")
        
def i6to4_no():
    clear_screen()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93m6TO4 \033[92m[Not Anycast]\033[93m Menu\033[0m")
    print("\033[92m \"-\"\033[93m════════════════════════════\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1. \033[92mKharej\033[0m")
    print("2. \033[93mIRAN\033[0m")
    print("3. \033[94mback to previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == "1":
            i6to4_kharej()
            break
        elif server_type == "2":
            i6to4_iran()
            break
        elif server_type == "3":
            clear_screen()
            i6to4_menu()
            break
        else:
            print("Invalid choice.")
			
def i6to4_kharej():
    clear_screen()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93m6TO4 \033[92mKharej\033[93m Menu\033[0m")
    print("\033[92m \"-\"\033[93m════════════════════════════\033[0m")
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[97m  For ping service, enter \033[92mIRAN\033[97m IPV4 address")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")

    if subprocess.run(['test', '-f', '/etc/6to4.sh'], capture_output=True).returncode == 0:
        subprocess.run(['rm', '/etc/6to4.sh'])
        
    display_notification("\033[93mConfiguring...\033[0m")  
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return    
    sleep(1)
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPv4 address: \033[0m")

    ipv4 = subprocess.run(["curl", "-s", "https://api.ipify.org"], capture_output=True, text=True).stdout.strip()


    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split(".")))
    
    
    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")
    

    if prefix.endswith("::1"):
        gateway = prefix[:-3] + "::2"
    else:
        gateway = prefix[:-3] + "::1"
    

    with open("/etc/6to4.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("/sbin/modprobe sit\n")
        f.write("/sbin/ip tunnel add azumi6 mode sit remote {} local {} ttl 255\n".format(remote_ip, local_ip))
        
        set_mtu = input('\033[93mDo you want to set \033[92m MTU?\033[93m (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m')
        if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
            mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
            f.write("/sbin/ip -6 link set dev azumi6 mtu {}\n".format(mtu_value))
        else:
            f.write("/sbin/ip -6 link set dev azumi6 mtu 1480\n")
        
        f.write("/sbin/ip link set dev azumi6 up\n")
        f.write("/sbin/ip -6 addr add {}/16 dev azumi6\n".format(prefix))
        f.write("/sbin/ip -6 route add 2000::/3 via {} dev azumi6 metric 1\n".format(gateway))
        f.write("ip -6 route add {} dev azumi6 metric 1\n".format(gateway))
        f.write("ip -6 route add ::/0 dev azumi6\n")

    num_ips = int(input("\033[93mHow many \033[92madditional IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    start_index = 3
    

    with open("/etc/6to4.sh", "a") as f:
        for i in range(start_index, start_index + num_ips):
            ip_addr = "2002:{:02x}{:02x}:{:02x}{:02x}::{:02x}/16".format(*map(int, ipv4.split(".")), i)
            f.write("ip -6 addr add {} dev azumi6\n".format(ip_addr))

    display_notification("\033[93mAdding cronjob!\033[0m")
      
    config_file_path = '/etc/6to4.sh'


    subprocess.run(f"(crontab -l | grep -v -F '{config_file_path}') | crontab -", shell=True, check=True)


    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)
    
    display_notification("\033[93mStarting 6to4...\033[0m")
    subprocess.run(["/bin/bash", "/etc/6to4.sh"])

    remote_ipv4 = input("\033[93mEnter \033[92mIran IPv4 address\033[93m [Ping Service]: \033[0m")


    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split(".")))

    sleep(1)

    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(["ping6", "-c", "2", remote_prefix], capture_output=True, text=True).stdout.strip()


    print(ping_result)


    script_content = '''#!/bin/bash


ip_address="''' + remote_prefix + '''"

max_pings=3

interval=40

while true
do
   
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F"time=" "{print $1}" | cut -d "." -f1)
       
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done'''


    with open("/etc/ping_v6.sh", "w") as f:
        f.write(script_content)

    subprocess.run(["chmod", "+x", "/etc/ping_v6.sh"])


    service_content = '''[Unit]
Description=Ping Service
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v6.sh
Restart=always

[Install]
WantedBy=multi-user.target'''

    with open("/etc/systemd/system/ping_v6.service", "w") as f:
        f.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "ping_v6.service"])
    subprocess.run(["systemctl", "start", "ping_v6.service"])
    sleep(1)
    subprocess.run(["systemctl", "restart", "ping_v6.service"])

    display_checkmark("\033[92m6to4 Service has been added successfully!\033[0m")

def i6to4_iran():
    clear_screen()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93m6TO4 \033[92mIRAN\033[93m Menu\033[0m")
    print("\033[92m \"-\"\033[93m════════════════════════════\033[0m")
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[97m  For ping service, enter \033[92mKharej\033[97m IPV4 address")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")

    if subprocess.run(['test', '-f', '/etc/6to4.sh'], capture_output=True).returncode == 0:
        subprocess.run(['rm', '/etc/6to4.sh'])
        
    display_notification("\033[93mConfiguring...\033[0m") 
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return    
    sleep(1)    
    print("\033[93m╭───────────────────────────────────────╮\033[0m")    

    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPv4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address: \033[0m")

    ipv4 = subprocess.run(["curl", "-s", "https://api.ipify.org"], capture_output=True, text=True).stdout.strip()


    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split(".")))
    
    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")
    

    if prefix.endswith("::1"):
        gateway = prefix[:-3] + "::2"
    else:
        gateway = prefix[:-3] + "::1"
    

    with open("/etc/6to4.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("/sbin/modprobe sit\n")
        f.write("/sbin/ip tunnel add azumi6 mode sit remote {} local {} ttl 255\n".format(remote_ip, local_ip))
        set_mtu = input('\033[93mDo you want to set \033[92m MTU?\033[93m (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m')
        if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
            mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
            f.write("/sbin/ip -6 link set dev azumi6 mtu {}\n".format(mtu_value))
        else:
            f.write("/sbin/ip -6 link set dev azumi6 mtu 1480\n")
        f.write("/sbin/ip link set dev azumi6 up\n")
        f.write("/sbin/ip -6 addr add {}/16 dev azumi6\n".format(prefix))
        f.write("/sbin/ip -6 route add 2000::/3 via {} dev azumi6 metric 1\n".format(gateway))
        f.write("ip -6 route add {} dev azumi6 metric 1\n".format(gateway))
        f.write("ip -6 route add ::/0 dev azumi6\n")

    num_ips = int(input("\033[93mHow many \033[92madditional IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    start_index = 3
    

    with open("/etc/6to4.sh", "a") as f:
        for i in range(start_index, start_index + num_ips):
            ip_addr = "2002:{:02x}{:02x}:{:02x}{:02x}::{:02x}/16".format(*map(int, ipv4.split(".")), i)
            f.write("ip -6 addr add {} dev azumi6\n".format(ip_addr))

    display_notification("\033[93mAdding cronjob!\033[0m")

    config_file_path = '/etc/6to4.sh'

    subprocess.run(f"(crontab -l | grep -v -F '{config_file_path}') | crontab -", shell=True, check=True)


    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)
    
    display_notification("\033[93mStarting 6to4...\033[0m")
    subprocess.run(["/bin/bash", "/etc/6to4.sh"])

    remote_ipv4 = input("\033[93mEnter \033[92mKharej IPv4 address\033[93m [Ping Service]: \033[0m")

    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split(".")))

    sleep(1)


    ping_result = subprocess.run(["ping6", "-c", "2", remote_prefix], capture_output=True, text=True).stdout.strip()


    print(ping_result)


    script_content = '''#!/bin/bash


ip_address="''' + remote_prefix + '''"

max_pings=3

interval=50

while true
do
  
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F"time=" "{print $1}" | cut -d "." -f1)
       
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done'''


    with open("/etc/ping_v6.sh", "w") as f:
        f.write(script_content)

    subprocess.run(["chmod", "+x", "/etc/ping_v6.sh"])


    service_content = '''[Unit]
Description=Ping Service
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v6.sh
Restart=always

[Install]
WantedBy=multi-user.target'''

    with open("/etc/systemd/system/ping_v6.service", "w") as f:
        f.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "ping_v6.service"])
    subprocess.run(["systemctl", "start", "ping_v6.service"])
    sleep(1)
    subprocess.run(["systemctl", "restart", "ping_v6.service"])

    display_checkmark("\033[92m6to4 Service has been added successfully!\033[0m")
	

def clear():
    subprocess.run(['clear'])

def i6to4_any():
    clear_screen()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93m6to4 \033[92m[Anycast]\033[93m Menu\033[0m")
    print("\033[92m \"-\"\033[93m════════════════════════════\033[0m")
    
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mback to main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    server_type = input("\033[38;5;205mEnter your choice Please: \033[0m")

    if server_type == '1':
        i6to4_any_kharej()
    elif server_type == '2':
        i6to4_any_iran()
    elif server_type == '3':
        clear()
        main_menu()
    else:
        print("Invalid choice.")
		
def i6to4_any_kharej():
    clear_screen()
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m6to4 \033[92mKharej\033[93m  Menu\033[92m[Anycast]\033[0m')  
    print('\033[92m "-"\033[93m════════════════════════════\033[0m')    
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your \033[92mKharej\033[93m IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[97m  For ping service, enter \033[92mIRAN\033[97m IPV4 address")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    
    
    if subprocess.run(['test', '-f', '/etc/6to4.sh'], capture_output=True).returncode == 0:
        subprocess.run(['rm', '/etc/6to4.sh'])
        
    display_notification("\033[93mConfiguring...\033[0m") 
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej IPv4\033[93m address: \033[0m")
           
    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))
    
    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")
    
    with open('/etc/6to4.sh', 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("/sbin/modprobe sit\n")
        f.write("/sbin/ip tunnel add azumi6 mode sit remote any local {} ttl 255\n".format(local_ip))
        set_mtu = input('\033[93mDo you want to set \033[92m MTU?\033[93m (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m')
        if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
            mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
            f.write("/sbin/ip -6 link set dev azumi6 mtu {}\n".format(mtu_value))
        else:
            f.write("/sbin/ip -6 link set dev azumi6 mtu 1480\n")
        f.write("/sbin/ip link set dev azumi6 up\n")
        f.write("/sbin/ip -6 addr add {}/16 dev azumi6\n".format(prefix))
        f.write("/sbin/ip -6 route add 2000::/3 via ::192.88.99.1 dev azumi6 metric 1\n")
    
    num_ips = input("\033[93mHow many \033[92madditional IPs\033[93m do you need? \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
    start_index = 3
    
    with open('/etc/6to4.sh', 'a') as f:
        for i in range(start_index, start_index + int(num_ips)):
            ip_addr = "2002:{:02x}{:02x}:{:02x}{:02x}::{:02x}/16".format(*map(int, ipv4.split('.')), i)
            f.write("ip -6 addr add {} dev azumi6\n".format(ip_addr))
    
    display_notification("\033[93mAdding cronjob!\033[0m")

    config_file_path = '/etc/6to4.sh'


    subprocess.run(f"(crontab -l | grep -v -F '{config_file_path}') | crontab -", shell=True, check=True)


    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)
    
    display_notification("\033[93mStarting 6to4...\033[0m")
    subprocess.run(['/bin/bash', '/etc/6to4.sh'])
    
    remote_ipv4 = input("\033[93mEnter \033[92mIRAN IPv4\033[93m address [Ping Service]: \033[0m")
    
    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    sleep(1)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', remote_prefix], capture_output=True, text=True).stdout.strip()
    
    print(ping_result)
    
    script_content = '''#!/bin/bash

ip_address="{}"

max_pings=3

interval=50

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
       
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
    with open('/etc/ping_v6.sh', 'w') as f:
        f.write(script_content)
    
    subprocess.run(['chmod', '+x', '/etc/ping_v6.sh'])
    
    with open('/etc/systemd/system/ping_v6.service', 'w') as f:
        f.write('[Unit]\n')
        f.write('Description=Ping Service\n')
        f.write('After=network.target\n')
        f.write('\n')
        f.write('[Service]\n')
        f.write('ExecStart=/bin/bash /etc/ping_v6.sh\n')
        f.write('Restart=always\n')
        f.write('\n')
        f.write('[Install]\n')
        f.write('WantedBy=multi-user.target\n')
    
    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v6.service'])
    subprocess.run(['systemctl', 'start', 'ping_v6.service'])
    sleep(1)
    subprocess.run(["systemctl", "restart", "ping_v6.service"])
    
    display_checkmark("\033[92m6to4 Service has been added successfully!\033[0m")
	
def i6to4_any_iran():
    clear_screen()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93m6to4 \033[92mIRAN\033[93m  Menu\033[92m[Anycast]\033[0m")
    print("\033[92m\"-\"\033[93m════════════════════════════\033[0m")
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your \033[92mIRAN\033[93m IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[97m  For ping service, enter \033[92mKharej\033[97m IPV4 address")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")

    if subprocess.run(['test', '-f', '/etc/6to4.sh'], capture_output=True).returncode == 0:
        subprocess.run(['rm', '/etc/6to4.sh'])
        
    display_notification("\033[93mConfiguring...\033[0m")
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return
    sleep(1)    
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIran IPv4\033[93m address: \033[0m")

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()

    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))
    
    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")

    with open('/etc/6to4.sh', 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("/sbin/modprobe sit\n")
        f.write("/sbin/ip tunnel add azumi6 mode sit remote any local {} ttl 255\n".format(local_ip))
        set_mtu = input('\033[93mDo you want to set \033[92m MTU?\033[93m (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m')
        if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
            mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
            f.write("/sbin/ip -6 link set dev azumi6 mtu {}\n".format(mtu_value))
        else:
            f.write("/sbin/ip -6 link set dev azumi6 mtu 1480\n")
        f.write("/sbin/ip link set dev azumi6 up\n")
        f.write("/sbin/ip -6 addr add {}/16 dev azumi6\n".format(prefix))
        f.write("/sbin/ip -6 route add 2000::/3 via ::192.88.99.1 dev azumi6 metric 1\n")

    num_ips = int(input("\033[93mHow many \033[92madditional IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    start_index = 3

    with open('/etc/6to4.sh', 'a') as f:
        for i in range(start_index, start_index + num_ips):
            ip_addr = "2002:{:02x}{:02x}:{:02x}{:02x}::{:02x}/16".format(*map(int, ipv4.split('.')), i)
            f.write("ip -6 addr add {} dev azumi6\n".format(ip_addr))

    display_notification("\033[93mAdding cronjob!\033[0m")

    config_file_path = '/etc/6to4.sh'


    subprocess.run(f"(crontab -l | grep -v -F '{config_file_path}') | crontab -", shell=True, check=True)


    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)

    display_notification("\033[93mStarting 6to4...\033[0m")
    subprocess.run(['/bin/bash', '/etc/6to4.sh'])

    remote_ipv4 = input("\033[93mEnter \033[92mKharej IPv4\033[93m address [Ping Service]: \033[0m")
    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))

    subprocess.run(['sleep', '1'])
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', remote_prefix], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    script_content = '''#!/bin/bash

ip_address="{}"
max_pings=3
interval=60

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
       
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix)

    with open('/etc/ping_v6.sh', 'w') as f:
        f.write(script_content)

    subprocess.run(['chmod', '+x', '/etc/ping_v6.sh'])

    with open('/etc/systemd/system/ping_v6.service', 'w') as f:
        f.write('''[Unit]
Description=Ping Service
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v6.sh
Restart=always

[Install]
WantedBy=multi-user.target
''')

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v6.service'])
    subprocess.run(['systemctl', 'start', 'ping_v6.service'])
    sleep(1)
    subprocess.run(["systemctl", "restart", "ping_v6.service"])

    display_checkmark("\033[92m6to4 Service has been added successfully!\033[0m")
    
def remove_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[91mUninstall\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mUninstall IPIP6\033[0m')
    print('2. \033[93mUninstall 6to4\033[0m')
    print('3. \033[93mUninstall 6to4 \033[96manycast\033[0m')
    print('4. \033[96mUninstall Gre\033[0m')
    print('5. \033[92mUninstall Gre6\033[0m')
    print('6. \033[93mUninstall Private IP\033[0m')
    print('7. \033[96mUninstall Native IP\033[0m')
    print('8. \033[91mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            remove_ipip6()
            break
        elif server_type == '2':
            remove_6to4()
            break
        elif server_type == '3':
            remove_6to4()
            break
        elif server_type == '4':
            remove_gre()
            break
        elif server_type == '5':
            remove_gre6()
            break
        elif server_type == '6':
            remove_private()
            break
        elif server_type == '7':
            extra_uninstall()
            break
        elif server_type == '8':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')

def remove_ipip6():
    os.system("clear")
    display_notification("\033[93mRemoving \033[92mIPIP6\033[93m Tunnel...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")

    try:
        if subprocess.call("test -f /etc/ipip.sh", shell=True) == 0:
            subprocess.run("rm /etc/ipip.sh", shell=True)
        if subprocess.call("test -f /etc/private.sh", shell=True) == 0:
            subprocess.run("rm /etc/private.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/ipip.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_v6.sh", shell=True)
        sleep(1)
        subprocess.run("sudo rm /etc/ping_ip.sh", shell=True)

        subprocess.run("systemctl disable ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v6.service > /dev/null 2>&1", shell=True)
        sleep(1)
        subprocess.run("systemctl disable ping_ip.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip.service > /dev/null 2>&1", shell=True)
        sleep(1)
        subprocess.run("systemctl daemon-reload", shell=True)

        subprocess.run("ip link set dev azumip down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumip > /dev/null", shell=True)
        sleep(1)
        subprocess.run("ip link set dev azumi down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi > /dev/null", shell=True)

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
		
def remove_6to4():
    os.system("clear")
    display_notification("\033[93mRemoving \033[92m6TO4\033[93m Tunnel...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")

    try:
        if subprocess.call("test -f /etc/6to4.sh", shell=True) == 0:
            subprocess.run("rm /etc/6to4.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot sh /etc/6to4.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_v6.sh", shell=True)
        time.sleep(1)

        subprocess.run("systemctl disable ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v6.service > /dev/null 2>&1", shell=True)
        time.sleep(1)

        subprocess.run("systemctl daemon-reload", shell=True)

        subprocess.run("ip link set dev azumi6 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi6 > /dev/null", shell=True)

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
		
def remove_gre():
    os.system("clear")
    display_notification("\033[93mRemoving \033[92mGRE\033[93m Tunnel...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")

    try:
        if subprocess.call("test -f /etc/gre.sh", shell=True) == 0:
            subprocess.run("rm /etc/gre.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot sh /etc/gre.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_ip.sh", shell=True)
        time.sleep(1)

        subprocess.run("systemctl disable ping_ip.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip.service > /dev/null 2>&1", shell=True)
        time.sleep(1)

        subprocess.run("systemctl daemon-reload", shell=True)

        subprocess.run("ip link set dev azumig down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumig > /dev/null", shell=True)


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
		
def remove_gre6():
    os.system("clear")
    display_notification("\033[93mRemoving \033[92mGRE6\033[93m Tunnel...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")

    try:
        if subprocess.call("test -f /etc/gre6.sh", shell=True) == 0:
            subprocess.run("rm /etc/gre6.sh", shell=True)
        if subprocess.call("test -f /etc/private.sh", shell=True) == 0:
            subprocess.run("rm /etc/private.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/gre6.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_v6.sh", shell=True)
        time.sleep(1)
        subprocess.run("sudo rm /etc/ping_ip.sh", shell=True)

        subprocess.run("systemctl disable ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v6.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable ping_ip.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumi down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi > /dev/null", shell=True)
        sleep(1)
        subprocess.run("ip link set dev azumig6 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumig6 > /dev/null", shell=True)

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
		
def remove_private():
    os.system("clear")
    display_notification("\033[93mRemoving private IP addresses...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    
    try:
        if subprocess.call("test -f /etc/private.sh", shell=True) == 0:
            subprocess.run("rm /etc/private.sh", shell=True)
            
        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private.sh\" | crontab -", shell=True)
        
        subprocess.run("sudo rm /etc/ping_v6.sh", shell=True)
        
        time.sleep(1)
        subprocess.run("systemctl disable ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v6.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumi down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi > /dev/null", shell=True)
        
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
    
    
def extra_uninstall():
    os.system("clear")
    display_notification("\033[93mRemoving Extra IP addresses...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")

    try:
        interface = subprocess.check_output("ip route | awk '/default/ {print $5; exit}'", shell=True).decode().strip()
        addresses = subprocess.check_output(f"ip addr show dev {interface} | awk '/inet6 .* global/ {{print $2}}'", shell=True).decode().splitlines()

        for address in addresses:
            subprocess.run(f"ip addr del {address} dev {interface}", shell=True)
            
        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/ipv6.sh\" | crontab -", shell=True)    

        sleep(1)
        subprocess.run("sudo rm /etc/ipv6.sh", shell=True)
        
        display_notification("\033[93mRemoving Extra ip, Working in the background..\033[0m")
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

        display_checkmark("\033[92mExtra IP addresses removed successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
    
main_menu()
