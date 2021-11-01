# bus_london
![Screenshot](bus_london.png?raw=true "Screenshot")

## **Overview**
This project is an info panel for displaying local informations around Colindale, London. It is modified according to its [previous version for Hong Kong](https://github.com/aji-tama/bus). The panel is updated every 20s by **matplotlib** and uploaded to specific Dropbox directory (external **rclone** setting would be required).  It is expected to be run in Raspberry Pi OS, change some specific paths if running in other platforms.

Data provided by Transport for London

Contains public sector information licensed under the Open Government Licence

## **Features**
- Local time
- Hong Kong time
- Hourly weather info from MET Northolt station, font color changes according to temperture
- SkyColor tile showing color of the sky, which changes with local elevation of the Sun accordingly
- Bus and tube ETA info

## **Update**
20211024 - wind chill and heat index are added. It will be shown when conditions meet.

20211028 - transportation info added. Update frequency reduced to avoid reaching MET daily call limit.

20211101 - fix server cache problem, see [StopPoint Arrivals is out of date if I use my app key](https://techforum.tfl.gov.uk/t/stoppoint-arrivals-is-out-of-date-if-i-use-my-app-key)


