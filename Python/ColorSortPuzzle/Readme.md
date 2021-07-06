# Color Sort Puzzle Automation

Mern and I have been obsessed with this game on our phones, so I decided to write a solver for it.

The program uses an installation of Android Debug Bridge (`adb`) to pull a screenshot from my phone. The program then runs
some image processing on the screenshot to determine the locations of all of the vials and colored balls. Once the program
has that information, it runs a depth first search to determine the fewest number of moves required to solve the level.
Then the program is able to use `adb` to automate the clicks required to solve the level, using my phone.

The image processing step of this process is probably trash, but I had a lot of fun making this.

No guarentees that it works on your particular phone. The image processing was designed around my old Samsung S8+, though
it was designed to handle levels with any number of vials with any number of balls.

Enjoy!

![](./images/Color%20Sort%20Puzzle%20Solver%20Example.gif)
