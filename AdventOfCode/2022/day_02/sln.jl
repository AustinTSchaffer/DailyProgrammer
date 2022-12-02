struct Datapoint
    them::String
    me::String
end

data::Array{Datapoint} = []

open("./input.txt", "r") do f
    for line in eachline(f)
        if all(isspace, line)
            continue
        end

        move = split(line, " ")
        push!(data, Datapoint(move[1], move[2]))
    end
end

# The score for a single round is the score for the shape you selected
# (1 for Rock, 2 for Paper, and 3 for Scissors) ...
@enum Move rock paper scissors
moveScore(m::Move)::Int = m == rock ? 1 : m == paper ? 2 : 3

# ... plus the score for the outcome of the round
# (0 if you lost, 3 if the round was a draw, and 6 if you won)
@enum Outcome win loss draw
outcomeScore(o::Outcome)::Int = o == win ? 6 : o == draw ? 3 : 0
turnOutcome(round::Tuple{Move,Move})::Tuple{Outcome,Outcome} =
    (round == (rock, rock)) ? (draw, draw) :
    (round == (rock, paper)) ? (loss, win) :
    (round == (rock, scissors)) ? (win, loss) :
    (round == (paper, rock)) ? (win, loss) :
    (round == (paper, paper)) ? (draw, draw) :
    (round == (paper, scissors)) ? (loss, win) :
    (round == (scissors, rock)) ? (loss, win) :
    (round == (scissors, paper)) ? (win, loss) :
    (round == (scissors, scissors)) ? (draw, draw) :
    error("Indecipherable matchup: $(round)")

function roundScore(round::Tuple{Move,Move})::Tuple{Int,Int}
    outcome = turnOutcome(round)

    return (
        outcomeScore(outcome[1]) + moveScore(round[1]),
        outcomeScore(outcome[2]) + moveScore(round[2])
    )
end

gameScore(game::Array{Tuple{Move,Move}})::Tuple{Int,Int} = reduce(
    (a, b) -> (a[1] + b[1], a[2] + b[2]),
    map(roundScore, game)
)

# Opponent: A for Rock, B for Paper, and C for Scissors
# Response: X for Rock, Y for Paper, and Z for Scissors
function part1(data::Array{Datapoint})::Int
    convertToRound(d::Datapoint)::Tuple{Move,Move} = (
        d.them == "A" ? rock : d.them == "B" ? paper : scissors,
        d.me == "X" ? rock : d.me == "Y" ? paper : scissors
    )

    return gameScore(map(convertToRound, data))[2]
end

# "Anyway, the second column says how the round needs to end:
# X means you need to lose, Y means you need to end the round
# in a draw, and Z means you need to win. Good luck!"
function part2(data::Array{Datapoint})::Int
    getLosingMove(m::Move)::Move = m == rock ? scissors : m == paper ? rock : paper
    getWinningMove(m::Move)::Move = m == rock ? paper : m == paper ? scissors : rock

    function convertToRound(d::Datapoint)::Tuple{Move,Move}
        theirMove::Move = d.them == "A" ? rock : d.them == "B" ? paper : scissors
        myOutcome::Outcome = d.me == "X" ? loss : d.me == "Y" ? draw : win
        myMove = myOutcome == draw ? theirMove : myOutcome == win ? getWinningMove(theirMove) : getLosingMove(theirMove)
        return (theirMove, myMove)
    end

    return gameScore(map(convertToRound, data))[2]
end

print("Part 1: ")
println(part1(data))
print("Part 2: ")
println(part2(data))
