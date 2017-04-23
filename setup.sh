#!/bin/bash

# Check ran by root, if not, elevate to root
if [[ $EUID -ne 0 ]]; then
    sudo su -s "$0"
    exit
fi

BLACKLIST=/etc/modprobe.d/raspi-blacklist.conf
CONFIG=/boot/config.txt

apt-get update
apt-get upgrade -y

# Install required tools
apt-get install -y i2c-tools python-smbus python-pip git
pip install flask

# Enable I2C interface
echo "[INFO] Enabling I2C interface..."
#set_config_var dtparam=i2c_arm on $CONFIG &&
echo "dtparam=i2c_arm=on" >> $CONFIG
if ! [ -e $BLACKLIST ]; then
  touch $BLACKLIST
fi
sed $BLACKLIST -i -e "s/^\(blacklist[[:space:]]*i2c[-_]bcm2708\)/#\1/"
sed /etc/modules -i -e "s/^#[[:space:]]*\(i2c[-_]dev\)/\1/"
if ! grep -q "^i2c[-_]dev" /etc/modules; then
  printf "i2c-dev\n" >> /etc/modules
fi
dtparam i2c_arm=on
modprobe i2c-dev

# Rename to MagicWatt
echo "[INFO] Changing hostname to MagicWatt..."
CURRENT_HOSTNAME=`cat /etc/hostname | tr -d " \t\n\r"`
echo "MagicWatt" > /etc/hostname
sed -i "s/127.0.1.1.*$CURRENT_HOSTNAME/127.0.1.1\tMagicWatt/g" /etc/hosts

# Change GPU Memory split
echo "[INFO] Changing GPU memory split..."
echo "gpu_mem=16" >> $CONFIG

# Add boot job for app
head -n -1 /etc/rc.local > /etc/rc.local.tmp
mv /etc/rc.local.tmp /etc/rc.local
echo "# Start MagicWatt on boot" >> /etc/rc.local
echo "su -c /home/pi/magicwatt-api/app.py magicwatt &" >> /etc/rc.local
echo "exit 0" >> /etc/rc.local

reboot
