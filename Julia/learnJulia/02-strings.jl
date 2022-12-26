s1 = "I am a string."
s2 = """I am also a "string". """

# Single quotes are for characters
typeof('a')

name = "Jane"
num_fingers = 10
num_toes = 10

# String interpolation
println("Hello, my name is $name.")
println("I have $num_fingers fingers and $num_toes toes, which is $(num_fingers + num_toes) total digits.")

# String concatenation
string(s1, " ", s2)
string(s1, " ", s2, 210)

s3 = s1*s2
s4 = "$s1$s2"
