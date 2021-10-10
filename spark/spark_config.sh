#! /bin/bash

# restore backup of bashrc
cp ~/.bashrc.bak ~/.bashrc

# changes to bashrc

echo "alias python=python3" >> ~/.bashrc

echo "export PATH=$PATH:/app/spark/bin" >> ~/.bashrc
echo "export PYSPARK_PYTHON=/usr/bin/python3" >> ~/.bashrc
echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> ~/.bashrc

source ~/.bashrc