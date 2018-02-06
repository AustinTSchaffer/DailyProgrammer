# How Long has the Light been On?


## Description

There is a light in a room which lights up only when someone is in the room 
(think motion detector). You are given a set of intervals in entrance and exit 
times as single integers, and expected to find how long the light has been on. 
When the times overlap, you need to find the time between the smallest and the 
biggest numbers in that interval. Input Description 

The program takes a set of two integers per line, specifying the time points 
that someone entered and exited the room, respectively. Each line is a 
visitor, each block is a room. 


## Example Input

	1 3
	2 3
	4 5


## Output Description

The program reads in this list of pairs of in/out times, and reports the 
number of hours the lights would be on. From the above input. 

	3


## Examples

### Example 1

	2 4  
	3 6  
	1 3  
	6 8

Output: `7`

### Example 2

	6 8
	5 8
	8 9
	5 7
	4 7

Output: `5`

### Example 3

	15 18
	13 16
	9 12
	3 4
	17 20
	9 11
	17 18
	4 5
	5 6
	4 5
	5 6
	13 16
	2 3
	15 17
	13 14

Output: `14`


## Credit

This challenge was found [here](https://www.reddit.com/r/dailyprogrammer/comments/7qn07r/20180115_challenge_347_easy_how_long_has_the/), 
and this README was taken from their challenge description, almost 
word-for-word. 

This challenge was suggested by the Reddit user /u/Elinaeri. 

If you have an idea for a challenge, please share it in 
/r/dailyprogrammer_ideas and there's a good chance they will use it. 
