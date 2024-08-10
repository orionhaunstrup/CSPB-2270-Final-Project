Rapidly Exploring Random Trees

    For my project I constructe a fully-working prototype of a data structure called a Rapidly Exploring Random Tree. I found it whilst perusing the Professor’s recommended “List of Data Structures” on Wikipedia. It sounded both fascinating and fun. I really wanted to try building and implementing one.

    The way it works is the following: You supply a 2 dimensional “playing field” for it to operate in, perhaps a large rectangle or circular area. You place two locations in at random, a start and an end. You a little victory circle around the ending point with some defined radius. You can then place obstacles in as well; perhaps obstructing circles and rectangles. The goal is to have the program find a way to explore outwards from the starting point and eventually find a route to the ending victory circle.

    This is where a Rapidly Exploring Random Tree comes in. It is built out of nodes and connecting lines. It begins by placing a root node at the starting location. You supply a random location in the playing field and travel from the starting node in that direction as far as some set maximum distance d. Place another node there and a connecting line between it and the root. Now supply it with another random location in the playing field, and have it check across all nodes in the tree to see which is the closest. Travel from that closest node in this new direction a maximum distance d and lay down a new exploratory node. Repeat this algorithm until the tree has entered the ending victory circle. Upon finding the ending circle, the tree can identify a route from finish to start by taking that final node in the victory circle and tracing back up its parent nodes until it finds the root.

    My program is written in Python 3. To run my program, download the main file "Rapidly Exploring Random Trees5.py" and make sure to have the accompanying file "colors.txt" in the same folder when you're running it. The only other thing you might need to do to get the program up and running is download the MatPlotLib package. The program itself, when run, contains a little introduction, and each step is explained clearly.

    I had so much fun writing this code! I tried to not only make the program fun and colorful, but I tried to give the user plenty of freedom to be artsy as well. The user has full creative freedom to choose all the colors and to control the program in many ways. This makes playing with it fun and dynamic.

    Instead of just letting the user choose from a preset list of colors (blue, green, red, etc...), I used a massive text document of all the xkcd colors, and let the user select a desired word or string. The program then sifts through all the colors in the entire list and selects those than contain the desired string. This means the user can collect all the colors containing the word "blue" (ex: xkcd:sky blue, xkcd:dusk blue), or if the user prefers they can type in a more strange or exotic string like "egg" or "dust" and get those colors. Lastly, if the user wants to select a more random list of colors, they can type in a very general string like "p" that will bring up many colors of every random shade and hue. Definitely try that out!
    
    Once I got the Rapidly Exploring Random Tree up and running, I was quite impressed with how speedy it is! Interestingly, the more obstacles present and the seemingly harder it is to find a path, the better the Exploring Tree is at finding a route! It gets a little lost in wide open spaces and is actually a lot faster with restricted movement.

    To watch a demo of my program, go to this YouTube link: https://www.youtube.com/watch?v=hQw_YWCx2_s

    I hope you have fun playing with the program. I sure did!
