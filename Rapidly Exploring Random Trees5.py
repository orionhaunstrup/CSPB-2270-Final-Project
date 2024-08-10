"""Rapidly Exploring Random Trees

This program, constructed for my class Data Structures and
Algorithms's final project, will design and impliment a
version of the data structure called a Rapidly Exploring Random
Tree.

Orion Haunstrup
CSPB 2270
Summer 2024
"""


## Finish Header Comments

## Finish Intro

## Add white rectangles on the outside to block the circles from spilling over.
                ## Perhaps more black outlines too


from math import log
import matplotlib.pyplot as pl
from random import randrange
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle
from math import atan
from math import cos



def create_colors_list():

    colors_list = ["xkcd:light grey", "xkcd:strong blue", "xkcd:sky blue",
                   "xkcd:purple", "xkcd:green", "xkcd:light green", "xkcd:brown",
                   "xkcd:red", "xkcd:teal", "xkcd:orange",
                   "xkcd:pink", "xkcd:magenta", "xkcd:yellow",
                   "xkcd:dark green", "xkcd:turquoise", "xkcd:lavender",
                   "xkcd:dark blue", "xkcd:tan", "xkcd:cyan",
                   "xkcd:melon", "xkcd:salmon", "xkcd:beige",
                   "xkcd:royal blue", "xkcd:hot pink"]
    ## A nice start

    infile = open("colors.txt", "r")
    FullData = infile.read()
    FullData = FullData.split("\n")
    infile.close()
    
    for line in FullData:
        line = line.split("\t")
        colors_list.append("xkcd:" + line[0])
    ## Then a whole bunch of random ones after

    snot_spot = colors_list.index("xkcd:snot")
    colors_list.remove("xkcd:snot")
            ##This color means fate_unknown
    colors_list.insert(snot_spot, colors_list[-1])
    colors_list = colors_list[:-1]

    neon_pink_spot = colors_list.index("xkcd:neon pink")
    colors_list.remove("xkcd:neon pink")
            ##This color means divergent
    colors_list.insert(neon_pink_spot, colors_list[-1])
    colors_list = colors_list[:-1]
    
    return colors_list



global colors_list
colors_list = create_colors_list()




def intro():
    print()
    print("Hi there! Welcome to my program on Rapidly Exploring Random Trees.")
    print()
    print("A Rapidly Exploring Random Tree is a data structure which explores")
    print("a space. It begins at a designated starting point and finds a path")
    print("through the space to a designed ending victory circle.")
    print()
    print("Let's run a demonstration!...")
    print()
    print()
    


def get_paint(first_time = False):
    print()
    if first_time is True:
        print("What color should we choose?")
        print("You can type in just about any color you can think of, and")
        print("I'll try and find those shades. You can type in simple ones")
        print("like blue or green or pink, or you can type in much more")
        print("advanced things like dust or melon or toxic.")
    choice = input("Pick any color: ")
    choice = choice.lower()
    paint = []
    for color in colors_list:
        if choice.lower() in color:
            paint.append(color)
    if len(paint) > 0:
        print("I found " + str(
            len(paint)) + " colors whose names contain the string " + choice)
        return paint
    else:
        print("Shoot! I found no colors whose names contain the string " + choice)
        print("Please try again.")
        return get_paint()


def choose_random(_list):
    return _list[randrange(len(_list))]


def distance(a,b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5
    


class PlayingField:

    def __init__(self, circ_or_rec, color):
        self.circ_or_rec = circ_or_rec
        self.color = color


class Node:
    
    def __init__(self, location, previous, color, line_color,
                 highlighted = False):
        self.location = location
        self.previous = previous
        self.color = color
        self.line_color = color
        self.highlighted = highlighted
        

class ExploringTree:

    def __init__(self, root, paint, node_spacing, obstacles, circ_or_rec):

        self.root = root
        self.paint = paint
        self.node_spacing = node_spacing
        self.nodes_list = [root]
        self.lines_list = []
        self.obstacles = obstacles
        self.circ_or_rec = circ_or_rec
        

    def find_closest_node(self, beacon):

        closest_distance = False
        closest_node = False
        
        for test_node in self.nodes_list:
            _dist = distance(test_node.location, beacon)
            if closest_distance == False:
                closest_distance = _dist
                closest_node = test_node
            else:
                if _dist < closest_distance:
                    closest_distance = _dist
                    closest_node = test_node

        return closest_node
    

    def get_the_towards_node(self, closest_node, beacon):
        if distance((closest_node.location[0], closest_node.location[1]), beacon) < self.node_spacing:
            return Node(beacon, closest_node, choose_random(self.paint), choose_random(self.paint))
        
        # Checking to make sure it's not straight vertical, so we don't divide by 0
        if beacon[0] == closest_node.location[0]:
            beacon[0] += 0.00001
        # Getting the correct line
            # y = m(x-x1) + y1
        m = (beacon[1] - closest_node.location[1]) / (beacon[0] - closest_node.location[0])
        x_1 = beacon[0]
        y_1 = beacon[1]
        angle = atan(m)
        x_dist_to_move = self.node_spacing * cos(angle)
        
        if beacon[0] > closest_node.location[0]:
            direction = 1
        else:
            direction = -1

        new_location = (closest_node.location[0] + direction * x_dist_to_move,
                        closest_node.location[1] + direction * x_dist_to_move * m)

        return Node(new_location, closest_node, choose_random(self.paint), choose_random(self.paint))


    def is_this_point_in_an_obstacle(self, point):
        
        for obstacle in self.obstacles:
            if obstacle[0] == "c":
                if distance(point, obstacle[1]) < obstacle[2]:
                    return True
            if obstacle[0] == "r":
                if obstacle[1][0] < point[0] < obstacle[2][0]:
                    if obstacle[1][1] < point[1] < obstacle[2][1]:
                        return True
        return False

    def does_this_line_cross_an_obstacle(self, point1, point2):
        x_dist = point2[0] - point1[0]
        y_dist = point2[1] - point1[1]

        line_list = []

        for i in range(101):
            new_point_x = point1[0] + i * x_dist/100
            new_point_y = point1[1] + i * y_dist/100
            line_list.append((new_point_x, new_point_y))

        for pt in line_list:
            if self.is_this_point_in_an_obstacle(pt) is True:
                return True
        return False
        

    def next(self):

        valid = False
        while valid is False:
            if self.circ_or_rec == "r":
                beacon = [randrange(201), randrange(151)]
            if self.circ_or_rec == "c":
                inner_valid = False
                while inner_valid == False:
                    beacon = [randrange(-100, 100), randrange(-100, 100)]
                    if distance(beacon, (0,0)) < 99:
                        inner_valid = True
            #print("beacon = " + str(beacon))
            closest_node = self.find_closest_node(beacon)
            #print("closest_node = " + str(closest_node.location))
            towards_node = self.get_the_towards_node(closest_node, beacon)
            #print("towards_node = " + str(towards_node.location))

            if self.does_this_line_cross_an_obstacle(
                closest_node.location, towards_node.location) is False:
                valid = True
        
        self.nodes_list.append(towards_node)

        


class Simulation:

    def __init__(self):

        self.playing_field = False
        self.obstacles = []
        self.start_end_n_victory_circle = False
        self.explorer = False
        
        self.get_playing_field(True)
        self.get_some_obstacles()

        self.get_start_and_end()

        root = Node(self.start_end_n_victory_circle[0], False, self.start_end_n_victory_circle[3], False)
        paint = self.get_explorer_paint()
        node_spacing = 20
        self.explorer = ExploringTree(root, paint, node_spacing,
                                      self.obstacles, self.playing_field.circ_or_rec)

        while True:
            self.explorer.next()
            self.display()
            latest_node = self.explorer.nodes_list[-1]
            end_location = self.start_end_n_victory_circle[1]
            victory_circle_radius = self.start_end_n_victory_circle[2]
            if distance(latest_node.location, end_location) < victory_circle_radius:
                print()
                print("We did it!! Yey!")
                print("We did it!! Yey!")
                print("We did it!! Yey!")
                print("We did it!! Yey!")
                print("We did it!! Yey!")
                print("We did it!! Yey!")
                print("We did it!! Yey!")
                self.display()
                break

        self.highlight_the_path(
            latest_node, self.start_end_n_victory_circle[3])
        self.display()
        

    def display(self, paint_demo = False):

        if self.playing_field.circ_or_rec == "r":

            plt.gca().add_patch(Rectangle((0,0),200,150,
                        edgecolor='black',
                        facecolor=self.playing_field.color,
                        lw=4))

            plt.xlim(0, 200)
            plt.ylim(0, 150)
            
        if self.playing_field.circ_or_rec == "c":

            plt.gca().add_patch(Rectangle((-134,-100),268,200,
                        edgecolor='black',
                        facecolor='black',
                        lw=0))

            plt.gca().add_patch(Circle((0, 0), 100,
                        edgecolor='black',
                        facecolor=self.playing_field.color,
                        lw=1))

            plt.xlim(-134, 134)
            plt.ylim(-100, 100)

        x_list = []
        y_list = []
        c_list = []

        if self.start_end_n_victory_circle != False:
            start = (self.start_end_n_victory_circle[0][0],
                     self.start_end_n_victory_circle[0][1])
            end = (self.start_end_n_victory_circle[1][0],
                   self.start_end_n_victory_circle[1][1])
            victory_circle_radius = self.start_end_n_victory_circle[2]
            color = self.start_end_n_victory_circle[3]
            x_list.append(start[0])
            y_list.append(start[1])
            c_list.append(color)

            plt.gca().add_patch(Circle(end, victory_circle_radius,
                        edgecolor='black',
                        facecolor=color,
                        lw=1))

            plt.gca().add_patch(Circle(start, 5,
                        edgecolor='black',
                        facecolor=color,
                        lw=1))

        if self.obstacles != []:
            for obstacle in self.obstacles:
                if obstacle[0] == "c":
                    plt.gca().add_patch(Circle(obstacle[1], obstacle[2],
                        edgecolor='black',
                        facecolor=obstacle[3],
                        lw=1))
                if obstacle[0] == "r":
                    plt.gca().add_patch(Rectangle(obstacle[1],
                            obstacle[2][0]-obstacle[1][0],
                            obstacle[2][1]-obstacle[1][1],
                            edgecolor='black',
                            facecolor=obstacle[3],
                            lw=1))

        if self.explorer != False:
            highlighted_line = []
            for node in self.explorer.nodes_list:
                x_list.append(node.location[0])
                y_list.append(node.location[1])
                c_list.append(node.color)

                if node.previous == False:
                    None
                else:
                    line_x_1 = (node.previous.location[0], node.location[0])
                    line_y_1 = (node.previous.location[1], node.location[1])
                    if node.highlighted is False:
                        plt.plot(line_x_1, line_y_1, label='Line',
                                 linewidth=2, color=node.line_color)  # Adding a line
                    else:
                        highlighted_line.append((line_x_1, line_y_1, node.line_color))
            for i in highlighted_line:
                plt.plot(i[0], i[1], label='Line',
                         linewidth=4, color=i[2])  # Adding a line
            

        plt.scatter(x_list, y_list, c=c_list, s=10)

        if paint_demo != False:
            for i in range(10):
                color = choose_random(paint_demo)
                if self.playing_field.circ_or_rec == "r":
                    plt.gca().add_patch(Rectangle((1+i*19.8,1),19.8,20,
                                edgecolor='black',
                                facecolor=color,
                                lw=1))
                if self.playing_field.circ_or_rec == "c":
                    plt.gca().add_patch(Rectangle((-133+i*26.6,-99),26.6,26.6,
                                edgecolor='black',
                                facecolor=color,
                                lw=1))

        plt.xticks([])
        plt.yticks([])
        
        plt.show()


    def get_playing_field(self, first_time = False):
        print()
        print("Let's define a playing field.")
        print("Do you want a rectangular playing field or a circular one?")
        circ_or_rec = input('Type "r" for rectangular or "c" for circular: ')
        if circ_or_rec not in ["r", "c"]:
            raise Exception('You did not type in "r" or "c".')
        
        if first_time is True:
            paint = get_paint(True)
        else:
            paint = get_paint()
            #paint is a list of similar hues from the colors_list
        print("Choosing a random one of those colors...")
        color = choose_random(paint)

        self.playing_field = PlayingField(circ_or_rec, color)
        
        print()
        print("Here is what the playing field currently looks like:")
        self.display()
        print()
        print("Do you like this playing field as it is?")
        choice = input('Enter "y" to accept or "n" to get a different playing field: ')
        if choice == "n":
            self.get_playing_field()


    def get_some_obstacles(self):
        print()
        print("Let's add some obstacles.")
        print("First we need to choose a color.")

        paint = get_paint()

        print()
        print("Let's add in a few obstacles")
        while True:
            for i in range(3):
                self.obstacles.append(self.make_obstacle(paint))
            self.display()
            choice = input("Should we add some more?: ")
            if choice != "y":
                break


    def make_obstacle(self, paint):
        if self.playing_field.circ_or_rec == "r":
            if randrange(2) == 0:
                circ_or_rec = "c"
                valid = False
                while valid is False:
                    valid = True
                    center = (randrange(201), randrange(151))
                    radius = randrange(10,26)
                    if (center[0] - radius < 1):
                        valid = False
                    if (center[0] + radius > 199):
                        valid = False
                    if (center[1] - radius < 1):
                        valid = False
                    if (center[1] + radius > 149):
                        valid = False
                color = choose_random(paint)
                return (circ_or_rec, center, radius, color)
            else:
                circ_or_rec = "r"
                width = randrange(10,26)
                height = randrange(10,26)
                center = (randrange(201), randrange(151))
                x1 = center[0]-width/2
                x2 = center[0]+width/2
                y1 = center[1]-height/2
                y2 = center[1]+height/2
                if x1 < 1:
                    x1 = 1
                if x2 > 199:
                    x2 = 199
                if y1 < 1:
                    y1 = 1
                if y2 > 145:
                    y2 = 145
                color = choose_random(paint)
                return (circ_or_rec, (x1, y1), (x2, y2), color)

        if self.playing_field.circ_or_rec == "c":
            if randrange(2) == 0:
                circ_or_rec = "c"
                valid = False
                while valid is False:
                    valid = True
                    center = (randrange(-100, 100), randrange(-100, 100))
                    radius = randrange(10,26)
                    if distance(center, (0,0)) > 100:
                        valid = False
                color = choose_random(paint)
                return (circ_or_rec, center, radius, color)
            else:
                circ_or_rec = "r"
                width = randrange(10,26)
                height = randrange(10,26)
                valid = False
                while valid is False:
                    valid = True
                    center = (randrange(-100,100), randrange(-100,100))
                    x1 = center[0]-width/2
                    x2 = center[0]+width/2
                    y1 = center[1]-height/2
                    y2 = center[1]+height/2
                    if distance(center, (0,0)) > 100:
                        valid = False
                color = choose_random(paint)
                return (circ_or_rec, (x1, y1), (x2, y2), color)
        

    def is_it_in_an_obstacle(self, point):
        for obstacle in self.obstacles:
            if obstacle[0] == "c":
                if distance(point, obstacle[1]) < obstacle[2]:
                    return True
            if obstacle[1] == "r":
                if obstacle[1][0] < point[0] < obstacle[2][0]:
                    if obstacle[1][1] < point[1] < obstacle[2][1]:
                        return True
        return False
        

    def get_start_and_end(self):
        if self.playing_field.circ_or_rec == "r":
            print()
            print("Getting the start point and the end victory circle...")
            print("First we need to choose a color.")

            paint = get_paint()
            
            print()
            valid = False
            while valid is False:
                start = (randrange(201), randrange(151))
                if self.is_it_in_an_obstacle(start) is False:
                    valid = True
            valid = False
            while valid is False:
                end = (randrange(201), randrange(151))
                if self.is_it_in_an_obstacle(end) is False:
                    valid = True
            victory_circle_radius = 10
            color = choose_random(paint)

            self.start_end_n_victory_circle = (start, end, victory_circle_radius, color)

            print()
            print("Here is what the starting point and ending victory circle look like:")
            self.display()
            print()
            print("Do you like these?")
            choice = input('Enter "y" to accept or "n" to redo: ')
            if choice == "n":
                self.get_start_and_end()

        if self.playing_field.circ_or_rec == "c":
            print()
            print("Getting the start point and the end victory circle...")
            print("First we need to choose a color.")

            paint = get_paint()
            
            print()
            valid = False
            while valid is False:
                start = (randrange(-100,100), randrange(-100,100))
                if distance(start, (0,0)) < 99:
                    if self.is_it_in_an_obstacle(start) is False:
                        valid = True
            valid = False
            while valid is False:
                end = (randrange(-100,100), randrange(-100,100))
                if distance(end, (0,0)) < 99:
                    if self.is_it_in_an_obstacle(end) is False:
                        valid = True
            victory_circle_radius = 10
            color = choose_random(paint)

            self.start_end_n_victory_circle = (start, end, victory_circle_radius, color)

            print()
            print("Here is what the starting point and ending victory circle look like:")
            self.display()
            print()
            print("Do you like these?")
            choice = input('Enter "y" to accept or "n" to redo: ')
            if choice == "n":
                self.get_start_and_end()


    def get_explorer_paint(self):
        print()
        print("We're just about to start building the exploring tree.")
        print("First we need to choose a color.")

        paint = get_paint()
        print()
        print("Let's do a little demo of what those colors will look like:")

        self.display(paint)
        
        print()
        print("Do you like this color?")
        choice = input('Enter "y" to accept or "n" to redo: ')
        if choice == "n":
            self.get_explorer_paint()
        else:
            return paint


    def highlight_the_path(self, latest_node, _color):
        print()
        print("Now let's highlight the path from start to end...")
        cursor = latest_node
        while cursor != False:
            cursor.color = _color
            cursor.line_color = _color
            cursor.highlighted = True
            cursor = cursor.previous
        

            
        
            


def main():

    intro()

    A = Simulation()


main()
