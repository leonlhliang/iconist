#!/bin/bash
TYPE=$1
OS=$(lsb_release -d | sed -n 's/[^U]*//p')

if [ -z $TYPE ]; then
    echo "USAGE: install.sh < web | node | mq | proc >"
    exit 1
elif [ "$OS" != "Ubuntu 12.04.3 LTS" ]; then
    echo "ERROR: Not a valid Ubuntu machine."
    exit 1
else
    echo "INFO: Installing $TYPE on $OS ..."
    :
fi


declare -a ospkgs=("vim" "curl" "sendmail" "python-dev")
declare -a pypkgs=("pip" "virtualenv" "boto")


if [ "$TYPE" == "web" ]; then
    ospkgs+=("apache2" "libapache2-mod-wsgi" "libapache2-mod-macro")
    pypkgs+=("web.py")

elif [ "$TYPE" == "node" ]; then
    ospkgs+=("python-software-properties python g++ make")

elif [ "$TYPE" == "mq" ]; then
    key="rabbitmq-signing-key-public.asc"
    wget http://www.rabbitmq.com/$key
    gpg --import $key
    apt-key add $key
    add-apt-repository "deb http://www.rabbitmq.com/debian/ testing main"
    rm $key

    ospkgs+=("rabbitmq-server")

elif [ "$TYPE" == "proc" ]; then
    add-apt-repository "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) universe"

    ospkgs+=(
    "libjpeg-dev" "libfreetype6-dev" "zlib1g-dev" "imagemagick" "zbar-tools"
     "libmysqlclient-dev" "python-mysqldb"
    )
    pypkgs+=(
    "web.py" "nose" "pika" "MySQL-python" "requests"
    "python-daemon" "setproctitle"
    "PIL" "reportlab" "PyPDF2"
    )

else
    echo "ERROR: Role can only be web, node, mq, or proc."
    exit 1

fi


apt-get update

for package in "${ospkgs[@]}"; do
    apt-get install --assume-yes $package
done

apt-get --assume-yes autoremove


if [ "$TYPE" == "web" ]; then
    service apache2 stop
    a2enmod rewrite expires macro

elif [ "$TYPE" == "node" ]; then
    add-apt-repository ppa:chris-lea/node.js
    apt-get update
    apt-get install nodejs

    for module in pm2; do
        npm install -g $module
    done

elif [ "$TYPE" == "mq" ]; then
    :

elif [ "$TYPE" == "proc" ]; then
    for library in libjpeg.so libfreetype.so libz.so; do
        ln -s /usr/lib/x86_64-linux-gnu/$library /usr/lib
    done

else
    echo "FATAL: This block should never be reached."
    exit 1

fi


curl --remote-name http://python-distribute.org/distribute_setup.py
python distribute_setup.py
rm -f distribute*
easy_install pip

for package in "${pypkgs[@]}"; do
    pip install --upgrade $package
done


echo "Done on $(date). Should reboot before use!"
exit 0
