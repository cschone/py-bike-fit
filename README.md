# py-bike-fit
Python script used to visually compare bicycle geometries defined in JSON files and plotted in matplotlib.

Bicycles are defined in JSON format according to the examples in the 'example-bikes' directory. Multiple bikes can be
compared by supplying multiple JSON files as shown below.

A Rider is defined in JSON format according to the examples 'example-bikes/rider.json'.

### Dependencies
You must install [matplotlib](http://matplotlib.org/users/installing.html) to use this script.

### Usage
    $ ./pybikefit.py -r example_bikes/rider.json -j example_bikes/cooper.json -j example_bikes/vaya_ti.json -j example_bikes/warbird.json

### Example Output
![Alt text](/example_bikes/example_bikes.png?raw=true "Example Bikes")
