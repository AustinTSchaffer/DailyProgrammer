sample_dict = Dict(
    "Key" => "Value",
    "Some other key" => 2323,
)

sample_dict["Key"]

sample_dict["New Key"] = "New Value"
sample_dict["Key"] = "Override"
sample_dict

pop!(sample_dict, "Some other key")
sample_dict

# tuples, looks like python
animals = ("penguins", "cats", "dogs")

# Julia is 1 indexed...
animals[1]

# Tuples are immutable, cant do this:
# animals[1] = "otters"

# Arrays/Vectors
people = ["Tom", "Scott", "Dave", "Mike", "John"]
fibo = [1, 1, 2, 3, 5, 8, 13]

# 4-element Vector{Any}:
mix = [ people[1], fibo[2], people[3], fibo[4] ]

# Push/Pop
push!(fibo, 21)
pop!(fibo)
push!(fibo, 21, 34, 55)

array_of_arrays = [
    people,
    fibo,
    mix,
]
array_of_new_arrays = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [Nothing, 0, "."]
]

# 1D, 2D, 3D arrays of random numbers.
rand(3)
rand(4, 5)
rand(2, 2, 3)
