# py-bike-fit
Python script used to visually compare bicycle geometries defined in JSON files and plotted in matplotlib.

Bicycle are defined in JSON format according the examples in the 'example-bikes' directory. Multiple bikes can be
compared by supplying multiple JSON files as shown below.

### Dependencies
You must install [matplotlib](http://matplotlib.org/users/installing.html) to use this script.

### Usage
    $ ./pybikefit.py -j example_bikes/cooper.json -j example_bikes/vaya_ti.json -j example_bikes/warbird.json

### Example Output
![Alt text](/example_bikes/example_bikes.png?raw=true "Example Bikes")
