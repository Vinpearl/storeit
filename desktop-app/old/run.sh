#!/bin/sh

(sleep 1; open $1)&
node main.js -d $1
