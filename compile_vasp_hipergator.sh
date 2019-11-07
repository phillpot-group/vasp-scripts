#!/bin/bash

# first and only command line arg should be path to vasp tarball
src=$1
dst="$(pwd)"

# untar the tarball into a new directory
mkdir "$dst/vasp"
tar -xf $src -C "$dst/vasp"

# move into the created directory
cd "$dst/vasp/"
cd "$(ls | grep vasp)"

# clean the package
make veryclean

# this is the compile chain as of November 7, 2019
module load ufrc
module load intel/2016.0.109
module load impi/5.1.1

# get the makefile.include from GitHub
wget https://raw.githubusercontent.com/phillpot-group/vasp-scripts/master/resources/makefile.include

# compile
make all

# add VASP_BIN environment variable to .bashrc
echo "VASP_BIN=$(pwd)/bin/vasp_std" >> ~/.bashrc
# update the session
source ~/.bashrc
