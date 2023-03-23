#!/usr/bin/env python3

# Copyright 2018 the py-bike-fit authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import math

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

__author__ = 'cschone'
__status__ = 'dev'
__title__ = 'Py Bike Fit'
__url__ = 'https://github.com/cschone/py-bike-fit'


def init_args():
    """ Defines required arguments and generates help and usage messages and
        issues errors when users give the program invalid arguments.
    :return:    A populated namespace
    """
    parser = argparse.ArgumentParser(
        description='Used to compare bicycle geometries defined in JSON files and plotted in matplotlib.',
        epilog="cschone 2015\n%s" % __url__)

    parser.add_argument("-j", "--json",
                        help="Path to a valid json bike file. Use multiple times to compare multiple bikes",
                        action="append")

    parser.add_argument("-r", "--rider",
                        help="Path to a valid json rider file.",
                        type=str)

    return parser.parse_args()


def get_vector_coords(x1, y1, length, angle_deg):
    """ find the end point coordinates of a vector
    :param x1:      start point
    :param y1:      start point
    :param length:  vector magnitude
    :param angle_deg: vector angle (degrees)
    :return: [start_x, end_x], [start_y, end_y]
    """
    y2 = y1 + length * math.sin(math.pi - math.radians(angle_deg))
    x2 = x1 + length * math.cos(math.pi - math.radians(angle_deg))
    return [x1, x2], [y1, y2]


def get_distance_between_coords(x1, y1, x2, y2):
    """ Pythagorean theorem
    :param x1:  start_x
    :param y1:  start_y
    :param x2:  end_x
    :param y2:  end_y
    :return:    length of hypotenuse
    """
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))


class Rider(object):
    """ Rider specific dimensions.
    """

    def __init__(self,
                 saddle_height=810,
                 saddle_length=280,
                 saddle_set_back=22):
        self.saddle_height = saddle_height
        self.saddle_length = saddle_length
        self.saddle_set_back = saddle_set_back

    def print_specs(self):
        print("Rider:")
        print("\tsaddle_height:\t%s" % self.saddle_height)
        print("\tsaddle_length:\t%s" % self.saddle_length)
        print("\tsaddle_set_back:\t%s" % self.saddle_set_back)


class Bicycle(object):
    """ A bicycle defined by dimensional characteristics. Generates output
        to matplotlib.
    """

    STEM_HEIGHT = 50
    HANDLEBAR_DIAMETER = 31.6

    def __init__(self,
                 name="Example",
                 frame_size="Large",
                 bb_drop=75,
                 bb_diameter=34.8,
                 chainstay_length=450,
                 color_str='r',
                 fork_length=405,
                 fork_offset=50,
                 head_tube_angle=71.5,
                 head_tube_length=205,
                 seat_tube_angle=72.5,
                 seat_tube_length=560,
                 stem_angle=0,
                 stem_length=50,
                 wheelbase=1072.6,
                 wheel_diameter=700.0,
                 rider=None
                 ):
        # public members
        self.color_str = str(color_str)
        self.frame_size = str(frame_size)
        self.name = str(name)
        # private members
        self._chainstay_length = float(chainstay_length)
        self._fork_length = float(fork_length)
        self._fork_offset = float(fork_offset)
        self._head_tube_angle = float(head_tube_angle)
        self._head_tube_length = float(head_tube_length)
        self._seat_tube_angle = float(seat_tube_angle)
        self._seat_tube_length = float(seat_tube_length)
        self._wheelbase = float(wheelbase)
        self._wheel_diameter = float(wheel_diameter)

        # BB
        self._bb = self.BottomBracket(bb_diameter, bb_drop, wheel_diameter)

        # Wheels
        x, y = self._rear_hub_coords()
        self._rear_wheel = self.Wheel([x, y],
                                      color_str=self.color_str,
                                      diameter=self._wheel_diameter)
        x, y = self._front_hub_coords()
        self._front_wheel = self.Wheel([x, y],
                                       color_str=self.color_str,
                                       diameter=self._wheel_diameter)
        # Stem
        self._stem_angle = float(stem_angle)
        self._stem_length = float(stem_length)

        # Saddle
        self._saddle = None
        if rider:
            self._saddle = self.Saddle(saddle_height=rider.saddle_height,
                                       saddle_length=rider.saddle_length,
                                       saddle_set_back=rider.saddle_set_back,
                                       bb_coords=self._bb.get_coord(),
                                       seat_tube_angle=self._seat_tube_angle,
                                       color_str=self.color_str)

    def print_specs(self):
        print("Info:")
        print("\tname:\t%s" % self.name)
        print("\tsize:\t%s" % self.frame_size)
        self._bb.print_specs()
        self._chainstay_print_specs()
        self._fork_print_specs()
        self._head_tube_print_specs()
        self._seat_tube_print_specs()
        self._stem_print_specs()
        self._top_and_down_tube_print_specs()

    def draw(self):
        self._front_wheel.draw()
        self._rear_wheel.draw()
        if self._saddle:
            self._saddle.draw()

        self._bb.draw(self.color_str)
        self._chainstay_draw()
        self._fork_draw()
        self._head_tube_draw()
        self._seat_stay_draw()
        self._seat_tube_draw()
        self._stem_draw()
        self._top_and_down_tube_draw()

    class BottomBracket(object):
        def __init__(self, diameter, drop, wheel_diameter):
            self._coord = [0, wheel_diameter / 2 - drop]
            self._diameter = diameter
            self._drop = drop

        def get_coord(self):
            return self._coord

        def get_diameter(self):
            return self._diameter

        def get_drop(self):
            return self._drop

        def draw(self, color_str):
            bb_plot = plt.Circle(self._coord,
                                 self._diameter / 2,
                                 fill=False,
                                 color=color_str)
            ax.add_artist(bb_plot)

        def print_specs(self):
            print("Bottom Bracket")
            print("\tbb diameter:\t%.2f" % self._diameter)
            print("\tbb drop:\t%.2f" % self._drop)

    class Wheel(object):
        """
        Reference:
            http://www.bikecalc.com/wheel_size_math
        """

        def __init__(self, axel_coord, diameter=700.0, color_str='b'):
            self._coord = axel_coord
            self._diameter = diameter
            self._color_str = color_str

        def draw(self):
            hub_plot = plt.Circle(self._coord, 20, fill=False, linestyle='dotted', color=self._color_str)
            ax.add_artist(hub_plot)
            wheel_plot = plt.Circle(self._coord,
                                    self._diameter / 2,
                                    fill=False,
                                    linestyle='dotted',
                                    color=self._color_str)
            ax.add_artist(wheel_plot)

        def print_specs(self):
            print("Wheel\n\t diameter:\t%.2f" % self._diameter)

    class Saddle(object):

        def __init__(self,
                     saddle_height,
                     saddle_length,
                     saddle_set_back,
                     bb_coords,
                     seat_tube_angle,
                     color_str='b'):
            self._saddle_height = saddle_height
            self._saddle_length = saddle_length
            self._saddle_set_back = saddle_set_back
            self._seat_tube_angle = seat_tube_angle
            self._bb_coords = bb_coords
            self._color_str = color_str

        def draw(self):
            # draw seat tube
            x, y = self._seat_tube_coords()
            ax.plot(x, y, self._color_str)

            # draw saddle
            seat_x = [x[1] - self._saddle_length / 2 - self._saddle_set_back,
                      x[1] + self._saddle_length / 2 - self._saddle_set_back]
            seat_y = [y[1], y[1]]
            ax.plot(seat_x, seat_y, self._color_str)

        def print_specs(self):
            print("Saddle")
            print("\tsaddle height:\t%.2f" % self._saddle_height)
            print("\tsaddle length:\t%.2f" % self._saddle_length)

        def _seat_tube_coords(self):
            return get_vector_coords(self._bb_coords[0], self._bb_coords[1],
                                     self._saddle_height, self._seat_tube_angle)

    def _chainstay_draw(self):
        rear_hub_x, rear_hub_y = self._rear_hub_coords()
        bb_x, bb_y = self._bb.get_coord()
        ax.plot([bb_x, rear_hub_x],
                [bb_y, rear_hub_y],
                self.color_str, linewidth=2)

    def _chainstay_print_specs(self):
        print("Chainstay")
        print("\tlength:\t%.2f" % self._chainstay_length)

    def _front_hub_coords(self):
        rear_x, rear_y = self._rear_hub_coords()
        return rear_x + self._wheelbase, rear_y

    def _fork_draw(self):
        # draw fork axis
        head_tube_x, head_tube_y = self._head_tube_coords()
        fork_x, fork_y = get_vector_coords(head_tube_x[0], head_tube_y[0],
                                           self._fork_length, -180 + self._head_tube_angle)
        ax.plot(fork_x, fork_y, self.color_str)

    def _fork_print_specs(self):
        print("Fork")
        print("\tlength:\t%.2f" % self._fork_length)
        print("\toffset:\t%.2f" % self._fork_offset)

    def _head_tube_draw(self):
        x, y = self._head_tube_coords()
        ax.plot(x, y, self.color_str, linewidth=2)

    def _head_tube_coords(self):
        """ Calculate head tube coordinates based on fork offset, fork length,
            wheelbase, head tube length and angle. A bit of trig required.
        :return: [start_x, end_x], [start_y, end_y]
        """
        # find point head tube axis crosses y = 0
        x_offset = self._fork_offset / math.cos(math.radians(90 - self._head_tube_angle))

        # find front hub
        rear_hub_x, rear_hub_y = self._rear_hub_coords()
        head_tube_x_origin = rear_hub_x + self._wheelbase - x_offset

        # find head tube bottom
        head_tube_bottom_x, head_tube_bottom_y = get_vector_coords(
            head_tube_x_origin,
            rear_hub_y,
            self._fork_length,
            self._head_tube_angle)

        # find head tube top
        return get_vector_coords(
            head_tube_bottom_x[1],
            head_tube_bottom_y[1],
            self._head_tube_length,
            self._head_tube_angle
        )

    def _head_tube_print_specs(self):
        print("Head Tube")
        print("\tangle:\t%.2f" % self._head_tube_angle)
        print("\tlength:\t%.2f" % self._head_tube_length)

    def _rear_hub_coords(self):
        x = - math.sqrt(math.pow(self._chainstay_length, 2) - math.pow(self._bb.get_drop(), 2))
        y = self._wheel_diameter / 2
        return x, y

    def _seat_stay_coords(self):
        seat_x, seat_y = self._seat_tube_coords()
        rear_hub_x, rear_hub_y = self._rear_hub_coords()
        return [seat_x[1], rear_hub_x], [seat_y[1], rear_hub_y]

    def _seat_stay_draw(self):
        x, y = self._seat_stay_coords()
        ax.plot(x, y, self.color_str, linewidth=2)

    def _seat_tube_coords(self):
        bb_x, bb_y = self._bb.get_coord()
        return get_vector_coords(bb_x, bb_y, self._seat_tube_length, self._seat_tube_angle)

    def _seat_tube_draw(self):
        x, y = self._seat_tube_coords()
        ax.plot(x, y, self.color_str, linewidth=2)

    def _seat_tube_print_specs(self):
        print("Seat Tube")
        print("\tangle:\t%.2f" % self._seat_tube_angle)
        print("\tlength:\t%.2f" % self._seat_tube_length)

    def _stem_draw(self):
        # draw steer tube
        x, y = self._steer_tube_coords()
        ax.plot(x, y, self.color_str)

        # draw stem
        x, y = get_vector_coords(x[1], y[1],
                                 self._stem_length + (self.HANDLEBAR_DIAMETER / 2),
                                 self._head_tube_angle - self._stem_angle + 90)
        ax.plot(x, y, self.color_str)

        # draw handlebar mount
        hb_plot = plt.Circle((x[1], y[1]),
                             self.HANDLEBAR_DIAMETER / 2,
                             fill=False,
                             color=self.color_str)
        ax.add_artist(hb_plot)

    def _steer_tube_coords(self):
        x, y = self._head_tube_coords()
        return get_vector_coords(x[1], y[1],
                                 self.STEM_HEIGHT,
                                 self._head_tube_angle)

    def _stem_print_specs(self):
        print("Stem")
        print("\tlength:\t%.2f" % self._stem_length)

    def _top_and_down_tube_coords(self):
        """ Estimates top and down tube positions based on head and seat tube
            definitions.
        :return:    [[ht_start_x, ht_end_x], [st_start_x, st_end_x]],
                    [[ht_start_y, ht_end_y], [st_start_y, st_end_y}]
        """
        head_tube_x, head_tube_y = self._head_tube_coords()
        seat_tube_x, seat_tube_y = self._seat_tube_coords()
        return [head_tube_x, seat_tube_x], [head_tube_y, seat_tube_y]

    def _top_and_down_tube_draw(self):
        x, y = self._top_and_down_tube_coords()
        ax.plot(x, y, self.color_str, linewidth=2)

    def _top_and_down_tube_print_specs(self):
        x, y = self._top_and_down_tube_coords()
        print("Top Tube:")
        print("\tlength:\t%.2f" % get_distance_between_coords(x[0][1], y[0][1], x[1][1], y[1][1]))
        print("Down Tube:")
        print("\tlength:\t%.2f" % get_distance_between_coords(x[0][0], y[0][0], x[1][0], y[1][0]))


def get_color(n):
    """ Valid matplotlib colors. Could be used to automatically pick colors.
    :param n:   an integer
    :return:    a valid matploglib color string
    """
    n %= 8
    colors = [
        'b',  # blue
        'g',  # green
        'r',  # red
        'c',  # cyan
        'm',  # magenta
        'y',  # yellow
        'k',  # black
        'w',  # white
    ]
    return colors[n]


def get_rider(json_rider_file):
    """ Open JSON file and build Rider object
    :param json_rider_file:  JSON file path
    :return: Rider object
    """
    try:
        with open(json_rider_file) as rider_file:
            data = json.load(rider_file)

            try:
                return Rider(
                    saddle_height=data["rider"]["saddle_height"],
                    saddle_length=data["rider"]["saddle_length"],
                    saddle_set_back=data["rider"]["saddle_set_back"]
                )
            except KeyError as e:
                print("Error reading Rider JSON")
                print("KeyError: File does not contain %s" % e)
                raise KeyError
    except IOError as e:
        print("Error reading Rider JSON")
        print("%s" % e)
        raise e
    return Rider()


def build_bike(json_bike_file, rider=None):
    """ Open JSON file and build Bicycle object
    :param json_bike_file:  JSON file path
    :param rider: a Rider object
    :return: Bicycle object
    """
    try:
        with open(json_bike_file) as data_file:
            data = json.load(data_file)

        try:
            return Bicycle(
                name=data["bicycle"]["name"],
                frame_size=data["bicycle"]["size"],
                bb_drop=data["bicycle"]["bb_drop"],
                bb_diameter=data["bicycle"]["bb_diameter"],
                chainstay_length=data["bicycle"]["chainstay_length"],
                color_str=data["bicycle"]["color_str"],
                fork_length=data["bicycle"]["fork_length"],
                fork_offset=data["bicycle"]["fork_offset"],
                head_tube_angle=data["bicycle"]["head_tube_angle"],
                head_tube_length=data["bicycle"]["head_tube_length"],
                seat_tube_angle=data["bicycle"]["seat_tube_angle"],
                seat_tube_length=data["bicycle"]["seat_tube_length"],
                stem_angle=data["bicycle"]["stem_angle"],
                stem_length=data["bicycle"]["stem_length"],
                wheelbase=data["bicycle"]["wheelbase"],
                wheel_diameter=data["bicycle"]["wheel_diameter"],
                rider=rider
            )
        except KeyError as e:
            print("KeyError: File does not contain %s" % e)
            raise KeyError
    except IOError as e:
        print("%s" % e)

    # Return example bike
    return Bicycle()


if __name__ == "__main__":
    # execute if run as a script

    args = init_args()

    rider = None
    if args.rider:
        rider = get_rider(args.rider)
        rider.print_specs()

    bikes = []
    if args.json:
        # read JSON files
        for b in args.json:
            bikes.append(build_bike(b, rider))
    else:
        # Make an example bike
        bikes.append(Bicycle())

    # build plot
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title(__title__)
    ax.set_xlim(-1000, 1200)
    ax.set_ylim(-100, 1400)
    ax.grid(True, which='both')

    labels = []
    for bike in bikes:
        if bike is not None:
            bike.print_specs()
            bike.draw()
            labels.append(mpatches.Patch(label=bike.name + " " + bike.frame_size,
                                         color=bike.color_str))

    ax.legend(handles=labels, loc='upper left')

    plt.show(block=True)
