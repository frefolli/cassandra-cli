#!/bin/bash
OTHER_NODES={{node.other_node_ips}}

MY_IP=$(hostname -I)

# Initialization of Node
function update_system() {
  echo -e "[APT] Updating System"
  sudo apt update
  sudo apt upgrade
  echo -e "[APT] System has been updated"
}

# Installation of java
function install_java() {
  echo -e "[JAVA] Installing Java"
  if [ -f /usr/bin/java ]; then
    echo -e "[JAVA] Skipping - Java is already installed"
  else
    echo -e "[JAVA] Java is not installed"
    sudo apt install openjdk-17-jre-headless
    echo -e "[JAVA] Java has been installed"
  fi
}

# Setup Firewall
function setup_firewall() {
  echo -e "[UFW] Configuring Firewall"
  sudo ufw disable
  sudo ufw reset
  sudo ufw allow ssh
  for OTHER_NODE in $OTHER_NODES; do
    sudo ufw allow from $CASSANDRA1 to $MY_IP proto tcp port 7000,9042
  done
  sudo ufw enable
  sudo ufw status numbered
  echo -e "[UFW] Firewall has been configured"
}

# Download Cassandra
function download_cassandra() {
  echo -e "[TAR] Downloading Cassandra"
  if [ -f apache-cassandra-5.0-beta1-bin.tar.gz ]; then
    echo -e "[TAR] Cassandra tar.gz already downloaded"
  else
    echo -e "[TAR] Downloading Cassandra tar.gz"
    wget https://dlcdn.apache.org/cassandra/5.0-beta1/apache-cassandra-5.0-beta1-bin.tar.gz
  fi
  if [ -f apache-cassandra-5.0-beta1 ]; then
    echo -e "[TAR] Cassandra tar.gz already extracted"
  else
    echo -e "[TAR] Extracting Cassandra tar.gz"
    tar xf apache-cassandra-5.0-beta1-bin.tar.gz
  fi
  echo -e "[TAR] Cassandra has been downloaded"
}

# Install
update_system
install_java
setup_firewall
download_cassandra
