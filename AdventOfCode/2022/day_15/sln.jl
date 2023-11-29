struct Sensor
    Loc::CartesianIndex
    NearestBeacon::CartesianIndex
    DistanceToNearest::Int
end

sensorBeaconRegex = r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"

function loadInput(filename::String)::Tuple{Vector{Sensor}, Set{CartesianIndex}}
    sensors = Sensor[]
    beacons = Set{CartesianIndex}()

    open(filename, "r") do f
        for line in readlines(f)
            sbMatch = match(sensorBeaconRegex, line)
            ints = [parse(Int, m) for m in sbMatch]
            beacon = CartesianIndex((ints[3], ints[4]))
            loc = CartesianIndex((ints[1], ints[2]))
            sensor = Sensor(loc, beacon, manhattan(loc, beacon))
            push!(sensors, sensor)
            push!(beacons, beacon)
        end
    end

    return (sensors, beacons)
end

manhattan(a::CartesianIndex, b::CartesianIndex)::Int = sum(map(abs, (b - a).I))

canScan(sensor::Sensor, loc::CartesianIndex)::Bool = manhattan(sensor.Loc, loc) <= sensor.DistanceToNearest

sensors, beacons = loadInput("./input.txt")
sample_sensors, sample_beacons = loadInput("./sample_input.txt")

function part1(sensors::Vector{Sensor}, beacons::Set{CartesianIndex}, y::Int)::Int
    function scannableXRange(sensor::Sensor, y::Int)::Union{Nothing, Tuple{Int, Int}}
        distToY = abs(sensor.Loc[2] - y)
        if distToY > sensor.DistanceToNearest
            return nothing
        end

        return (
            sensor.Loc[1] - (sensor.DistanceToNearest - distToY),
            sensor.Loc[1] + (sensor.DistanceToNearest - distToY),
        )
    end

    scannableXRanges = map(sensor -> scannableXRange(sensor, y), sensors)

    leftMostX = minimum(xrange -> xrange[1], filter(xrange -> xrange !== nothing, scannableXRanges))
    rightMostX = maximum(xrange -> xrange[2], filter(xrange -> xrange !== nothing, scannableXRanges))

    println("left: ", leftMostX, " right: ", rightMostX)

    scannableLocationsNoBeacons = 0
    for x in leftMostX:rightMostX
        location = CartesianIndex(x, y)
        if any(sensor -> canScan(sensor, location), sensors) && (location ∉ beacons)
            scannableLocationsNoBeacons += 1
        end
    end

    return scannableLocationsNoBeacons
end

println("Part 1: (Sample): ", part1(sample_sensors, sample_beacons, 10))
println("Part 1: ", part1(sensors, beacons, 2000000))

function part2(sensors::Vector{Sensor}, maxX::Int, maxY::Int, minX=0, minY=0)::CartesianIndex
    function perimeter(sensor::Sensor)
        left = sensor.Loc - CartesianIndex(sensor.DistanceToNearest + 1, 0)
        up = sensor.Loc + CartesianIndex(0, sensor.DistanceToNearest + 1)
        right = sensor.Loc + CartesianIndex(sensor.DistanceToNearest + 1, 0)
        down = sensor.Loc - CartesianIndex(0, sensor.DistanceToNearest + 1)

        return Iterators.flatten((
            (CartesianIndex(idx) for idx in zip(left[1]:up[1], left[2]:up[2])),
            (CartesianIndex(idx) for idx in zip(up[1]:right[1], up[2]:-1:right[2])),
            (CartesianIndex(idx) for idx in zip(right[1]:-1:down[1], right[2]:-1:down[2])),
            (CartesianIndex(idx) for idx in zip(down[1]:-1:left[1], down[2]:left[2])),
        ))
    end

    # Generate all indexes that are outside the border of each sensor
    for sensor in sensors
        perim = perimeter(sensor)
        for idx in perim
            # Check that the index is >= lower and <= upper
            if (minX <= idx[1] <= maxX) && (minY <= idx[2] <= maxY)
                # Check that the index is not contained within any sensor ranges
                if !any(s -> canScan(s, idx), sensors)
                    return idx
                end
            end
        end
    end

    # Way too slow.
    # for idx in CartesianIndex(minX, minY):CartesianIndex(maxX, maxY)
    #     if !any(sensor -> canScan(sensor, idx), sensors)
    #         return idx
    #     end
    # end
end

println("Part 2: (Sample): ", part2(sample_sensors, 20, 20))
println("Part 2: ", part2(sensors, 4000000, 4000000))
