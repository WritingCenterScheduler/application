#!/bin/bash

sudo echo "Starting Mongo"
sudo mongod --auth 2>/dev/null >/dev/null &