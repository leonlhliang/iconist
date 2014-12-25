#!/bin/bash
# This script requires the latest Xcode and Xcode-CLI-Tools pre-installed

OS=$(uname)
HOME=$(pwd)


if [ $OS != "Darwin" ]; then
    echo "ERROR: Not an OSX machine."
    exit 1
fi


echo "Machine: $(sw_vers -productName) $(sw_vers -productVersion) detected."
echo "Begin installing development stack on $(date) ..."


sudo -u ${SUDO_USER} ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
export PATH=/usr/local/bin:$PATH

sudo -u ${SUDO_USER} brew install git
git config --global url."https://".insteadOf git://


sudo -u ${SUDO_USER} brew update
sudo -u ${SUDO_USER} brew upgrade


declare -a stack
stack=(
"python --framework" "node"
"sqlite" "mysql" "rabbitmq"
"openssl" "vim" "wget" "curl"
"freetype" "imagemagick" "zbar"
)

for package in "${stack[@]}"; do
    sudo -u ${SUDO_USER} brew install $package
done

sudo -u ${SUDO_USER} brew link --force sqlite
export PATH=/usr/local/share/python:$PATH


for package in grunt-cli bower karma nodemon pm2; do
    npm install -g $package
done


curl -O http://valgrind.org/downloads/valgrind-3.8.1.tar.bz2
tar -xjvf valgrind-3.8.1.tar.bz2
cd valgrind-3.8.1
./configure
make
make install
make clean
cd ..
rm -rf valgrind-3.8.1*


curl -O http://modwsgi.googlecode.com/files/mod_wsgi-3.4.tar.gz
tar xvfz mod_wsgi-3.4.tar.gz
cd mod_wsgi-3.4
./configure --with-python=/usr/local/bin/python
make
make install
make clean
cd ..
rm -rf mod_wsgi*
echo "LoadModule wsgi_module /usr/libexec/apache2/mod_wsgi.so" > /etc/apache2/users/wsgi.conf

wget http://people.apache.org/~fabien/mod_macro/mod_macro-1.1.11.tar.gz
tar xzvf mod_macro-1.1.11.tar.gz
apxs -cia mod_macro-1.1.11/mod_macro.c
rm -rf mod_macro*


apachectl reload
apachectl restart


curl --remote-name http://python-distribute.org/distribute_setup.py
python distribute_setup.py
rm -f distribute*
easy_install pip


declare -a pystack
pystack=(
"pip" "virtualenv" "nose" "python-daemon" "setproctitle"
"PIL" "reportlab" "PyPDF2"
"MySQL-python" "pika" "web.py" "requests"
"boto" "awscli"
)

for package in "${pystack[@]}"; do
    pip install --upgrade $package
done


echo "Done on $(date). Reboot and enjoy this bare machine!"
exit 0
