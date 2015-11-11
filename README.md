rpi-web-controller
==================

The idea is to have a simple HTTP Server to control the GPIOs of a Raspberry Pi.

The project includes a static web page with jquery to communicate with the server, all css and js files are included to support offline (no internet) operation.


##Running the server

start the server by running 

```bash
sudo python server.py
```

##Configuration
Mapping between functions and GPIO pins is in configuration.py

