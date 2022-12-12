mutable struct Monkey
    id::Int
    operation

    # Test Section
    modulus::Int
    ifTrue::Int
    ifFalse::Int

    # Mutable Fields
    items::Vector{Int}
    itemsInspected::Int
end

idRegex = r"Monkey (\d+):"
itemsRe = r"Starting items: ((\d+,? ?)+)"
operationRe = r"Operation: new = (.+)"
modulusRe = r"Test: divisible by (\d+)"
ifTrueRe = r"If true: throw to monkey (\d+)"
ifFalseRe = r"If false: throw to monkey (\d+)"

function loadMonkey(input::AbstractString)::Monkey
    id = parse(Int, match(idRegex, input)[1])

    items = [
        parse(Int, v) for v in
        split(match(itemsRe, input)[1], ", ")
    ]

    operation = match(operationRe, input)
    operation = eval(Meta.parse("(old) -> $(operation[1])"))

    modulus = parse(Int, match(modulusRe, input)[1])
    ifTrue = parse(Int, match(ifTrueRe, input)[1])
    ifFalse = parse(Int, match(ifFalseRe, input)[1])

    Monkey(id, operation, modulus, ifTrue, ifFalse, items, 0)
end

function loadMonkeys(filename="input.txt")
    map(
        loadMonkey,
        split(
            read(open(filename), String),
            "\n\n"
        )
    )
end

function monkeyDo!(monkeys::Vector{Monkey}; divBy3=true, modBy=0)
    for monkey in monkeys
        while length(monkey.items) > 0
            monkey.itemsInspected += 1
            old = pop!(monkey.items)

            new = monkey.operation(old)

            if divBy3
                new = div(new, 3)
            else
                new = new % modBy
            end

            if new % monkey.modulus == 0
                push!(monkeys[monkey.ifTrue + 1].items, new)
            else
                push!(monkeys[monkey.ifFalse + 1].items, new)
            end
        end
    end
end

function calcMonkeyBusiness(monkeys)
    mostActiveMonkeys = sort(monkeys, by=m -> m.itemsInspected, rev=true)
    mostActiveMonkeys[1].itemsInspected * mostActiveMonkeys[2].itemsInspected
end

part1_monkeys = loadMonkeys()
for i in 1:20
    monkeyDo!(part1_monkeys)
end

println("Part 1: ", calcMonkeyBusiness(part1_monkeys))

part2_monkeys = loadMonkeys()
gcm = prod(m->m.modulus, part2_monkeys)
for i in 1:10000
    monkeyDo!(part2_monkeys, divBy3=false, modBy=gcm)
end

println("Part 2: ", calcMonkeyBusiness(part2_monkeys))
