#!/bin/bash
apt update -y
apt install wget -y
wget -O /etc/logo.sh https://github.com/Azumi67/UDP2RAW_FEC/raw/main/logo2.sh
chmod +x /etc/logo2.sh
if [ -f "chisel.py" ]; then
    rm chisel.py
fi
wget https://github.com/Azumi67/Chisel_multipleServers/releases/download/ubuntu24/chisel.py
python3 chisel.py
