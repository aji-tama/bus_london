# bus_london
![Screenshot](bus_london.png?raw=true "Screenshot")

## **Overview**
This project is an info panel for displaying local informations around Colindale, London. It is modified according to its [previous version for Hong Kong](https://github.com/aji-tama/bus). The panel is updated every 15s by **matplotlib** and uploaded to specific Dropbox directory (external **rclone** setting would be required).  It is designed to be run in a Raspberry Pi 2B.

## **Features**
- Local time
- Hong Kong time
- Hourly weather info from MET Northolt station
- SkyColor tile showing color of the sky, which changes with local elevation of the Sun accordingly
- Bus ETA info (suspended) 

## **Update**
20211024 - wind chill and heat index are added. It will be shown when conditions meet.


