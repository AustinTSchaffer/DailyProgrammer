"""
The syntax for a while is

    while *condition*
        *loop body*
    end
"""

n = 1
while n <= 10
    n += n
    println(n)
end

# My only friends are numbers 😢
friends = [1, 2, 3, 4, 5, 6]

i = 1 # This language better have an iterator/higher-order functions STG
while i <= length(friends)
    friend = friends[i]
    println("Hi $friend, it's nice to see that you're still hanging around these parts.")
    i += 1
end 

# Praise
for friend in friends
    println(friend)
end

# Julia has "ranges"
example_range = 1:100 # UnitRange{Int64}
another_range = 'a':'z' # StepRange{Char, Int64}

for letter in 'a':'z'
    print(letter)
end
println()

# Julia also has unicode overloading
for letter = 'a':'z'
    print(letter)
end
println()

# That's a Unicode U+2208 "Element of" symbol
for letter ∈ 'a':'z'
    print(letter)
end
println()

# Make a 5x5 addition table
m, n = 5, 5
table = zeros(m, n)
println(typeof(table)) # Matrix{Float64}, NOT a 2D array
for i in 1:m
    for j in 1:n
        table[i, j] = i + j
    end
end
table

# Same thing but condensed
table = zeros(m, n)
for i in 1:m, j in 1:n
    table[i, j] = i+j
end
table

# More exploration of condensing loops.
combinations_2 = []
for f1 in friends, f2 in friends
    if f1 != f2
        push!(combinations_2, (f1, f2))
    end
end

combinations_3 = []
#for f1 in friends, f2 = friends, f3 ∈ friends
for f1 = friends, f2 = friends, f3 = friends
    if f1 != f2 && f2 != f3 && f1 != f3
        push!(combinations_3, (f1, f2, f3))
    end
end
combinations_3

# COMPREHENSIONS!!!
table = [i+j for i in 1:m, j in 1:n]

for n in 1:10
    powtable = [i^j for i = 1:n, j in 1:n]
    display(powtable)
end
