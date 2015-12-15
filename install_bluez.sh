#! /bin/bash
abort()
{
    echo >&2 '
***************
*** ABORTED ***
***************
'
    echo "An error occurred. Exiting..." >&2
    exit 1
}

trap 'abort' 0

set -e
###############################################################################
echo "------------------------------------------------------------------------"
echo "Configuration started......"
echo "Please run this script only once, after that delete it"
cd ~
# Gatttool is a standard tool included in the BlueZ software package,
# but it is not installed on the Intel Edison board by default. 
# To install it, download BlueZ 5.36 (latest) source code and compile 
wget https://www.kernel.org/pub/linux/bluetooth/bluez-5.36.tar.gz - no-check-certificate
tar -xvf bluez-5.36.tar.gz
rm bluez-5.36.tar.gz
cd bluez-5.36
./configure --disable-systemd --disable-udev
make
make install
# To be able to launch gatttool from anywhere add it to the path
echo "export PATH=$PATH:~/bluez-5.36/attrib/" >> /etc/profile
# To run the Python script using pexpect, pexpect must be installed,
# which is easiest to do with Pip. Pip is not installed on the Intel Edison 
# board by default and is not present in the official opkg repo
echo "src/gz all http://repo.opkg.net/edison/repo/all" > /etc/opkg/base-feeds.conf
echo "src/gz edison http://repo.opkg.net/edison/repo/edison" >> /etc/opkg/base-feeds.conf
echo "src/gz core2-32 http://repo.opkg.net/edison/repo/core2-32" >> /etc/opkg/base-feeds.conf
# Update opkg list and install Pip
opkg update
opkg install python-pip
# Install setup-tools for Pip
wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py --no-check-certificate -O - | python
# Install pexpect
pip install pexpect
##############################################################################
trap : 0

echo >&2 '
************
*** DONE *** 
************
'
echo "Complete."
