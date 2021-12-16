#! /bin/bash

home=$(pwd)

cd server
./scripts/build.sh

cd $home
cd ./infrastructure/db
./scripts/build.sh