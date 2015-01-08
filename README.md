py-scale
========

Read Mettler toledo weighting scale in Python

## Scripts

#### Modules
- scale.py     => Mettler toledo parser
- simulator.py => pseudo serial for Mettler toledo simulation

#### Executable
- sender.py    => publish scale value via mqtt

#### Test scripts
- test.py      => test serial communication

## Test
    mosquitto -c /etc/mosquitto/mosquitto.conf -d # start broker
    python sender.py

## Installation
    sudo pip install -r requirements.txt

## Miscs
- [Setup Environment on BBB](https://gist.github.com/taka-wang/29433180cc8affcde3b2)
- [Install mosquitto 1.4 on raspberry pi](https://gist.github.com/taka-wang/1c47cde3e4c9c2d83156)

## MIT License