println("I'm excited to learn Julia!")

my_variable = 42

print(my_variable)
print(" ")
println(typeof(my_variable))

🐱 = "Emoji variable name"

println(🐱)

# Comments use the # symbol

sum = 3 + 8
diff = 10 - 3
product = 20 * 2
quotient = 100 / 10
power = 10 ^ 3
mod = 101 % 7

# Type conversion
days = 365
days_float = float(days)
# Alternatives
# days_float = convert(Float64, days)
# days_float = convert(Float32, days)


@assert days == 365
@assert days_float == 365.0
