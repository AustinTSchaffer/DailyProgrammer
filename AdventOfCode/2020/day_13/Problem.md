# Day 13: Shuttle Search

Your ferry can make it safely to a nearby port, but it won't get much further. When you call to book another ship, you discover that no ships embark from that port to your vacation island. You'll need to get from the port to the nearest airport.

Fortunately, a shuttle bus service is available to bring you from the sea port to the airport! Each bus has an ID number that also indicates how often the bus leaves for the airport.

Bus schedules are defined based on a timestamp that measures the number of minutes since some fixed reference point in the past. At timestamp 0, every bus simultaneously departed from the sea port. After that, each bus travels to the airport, then various other locations, and finally returns to the sea port to repeat its journey forever.

The time this loop takes a particular bus is also its ID number: the bus with ID 5 departs from the sea port at timestamps 0, 5, 10, 15, and so on. The bus with ID 11 departs at 0, 11, 22, 33, and so on. If you are there when the bus departs, you can ride that bus to the airport!

## Part 1

Your notes (your puzzle input) consist of two lines. The first line is your estimate of the earliest timestamp you could depart on a bus. The second line lists the bus IDs that are in service according to the shuttle company; entries that show x must be out of service, so you decide to ignore them.

To save time once you arrive, your goal is to figure out the earliest bus you can take to the airport. (There will be exactly one such bus.)

For example, suppose you have the following notes:

    939
    7,13,x,x,59,x,31,19

Here, the earliest timestamp you could depart is 939, and the bus IDs in service are 7, 13, 59, 31, and 19. Near timestamp 939, these bus IDs depart at the times marked D:

    time   bus 7   bus 13  bus 59  bus 31  bus 19
    929      .       .       .       .       .
    930      .       .       .       D       .
    931      D       .       .       .       D
    932      .       .       .       .       .
    933      .       .       .       .       .
    934      .       .       .       .       .
    935      .       .       .       .       .
    936      .       D       .       .       .
    937      .       .       .       .       .
    938      D       .       .       .       .
    939      .       .       .       .       .
    940      .       .       .       .       .
    941      .       .       .       .       .
    942      .       .       .       .       .
    943      .       .       .       .       .
    944      .       .       D       .       .
    945      D       .       .       .       .
    946      .       .       .       .       .
    947      .       .       .       .       .
    948      .       .       .       .       .
    949      .       D       .       .       .

The earliest bus you could take is bus ID 59. It doesn't depart until timestamp 944, so you would need to wait 944 - 939 = 5 minutes before it departs. Multiplying the bus ID by the number of minutes you'd need to wait gives 295.

What is the ID of the earliest bus you can take to the airport multiplied by the number of minutes you'll need to wait for that bus?

## Part 1 Math

Min depart time `mdt` = 1003240

| Bus `b` | Modulo `mdt % b` | Time Until Departure `b - (mbt % b)` |
| ------- | ---------------- | ------------------------------------ |
| 19      | 2                | 17                                   |
| 41      | 11               | 30                                   |
| 37      | 22               | 15                                   |
| 787     | 602              | 185                                  |
| 13      | 4                | 9                                    |
| 23      | 3                | 20                                   |
| 29      | 14               | 15                                   |
| **571** | **564**          | **7**                                |
| 17      | 2                | 15                                   |

Minimum wait time = 7
Bus = 571
Part 1 answer: `571 * 7` = `3997`

## Part 2

The shuttle company is running a contest: one gold coin for anyone that can find the earliest timestamp such that the first bus ID departs at that time and each subsequent listed bus ID departs at that subsequent minute. (The first line in your input is no longer relevant.)

For example, suppose you have the same list of bus IDs as above:

    7,13,x,x,59,x,31,19

An x in the schedule means there are no constraints on what bus IDs must depart at that time.

This means you are looking for the earliest timestamp (called `t`) such that:

- Bus ID 7 departs at timestamp `t`.
- Bus ID 13 departs one minute after timestamp `t`.
- There are no requirements or restrictions on departures at two or three minutes after timestamp `t`.
- Bus ID 59 departs four minutes after timestamp `t`.
- There are no requirements or restrictions on departures at five minutes after timestamp `t`.
- Bus ID 31 departs six minutes after timestamp `t`.
- Bus ID 19 departs seven minutes after timestamp `t`.

The only bus departures that matter are the listed bus IDs at their specific offsets from `t`. Those bus IDs can depart at other times, and other bus IDs can depart at those times. For example, in the list above, because bus ID 19 must depart seven minutes after the timestamp at which bus ID 7 departs, bus ID 7 will always also be departing with bus ID 19 at seven minutes after timestamp `t`.

In this example, the earliest timestamp at which this occurs is `1068781`:

    time     bus 7   bus 13  bus 59  bus 31  bus 19
    1068773    .       .       .       .       .
    1068774    D       .       .       .       .
    1068775    .       .       .       .       .
    1068776    .       .       .       .       .
    1068777    .       .       .       .       .
    1068778    .       .       .       .       .
    1068779    .       .       .       .       .
    1068780    .       .       .       .       .
    1068781    D       .       .       .       .
    1068782    .       D       .       .       .
    1068783    .       .       .       .       .
    1068784    .       .       .       .       .
    1068785    .       .       D       .       .
    1068786    .       .       .       .       .
    1068787    .       .       .       D       .
    1068788    D       .       .       .       D
    1068789    .       .       .       .       .
    1068790    .       .       .       .       .
    1068791    .       .       .       .       .
    1068792    .       .       .       .       .
    1068793    .       .       .       .       .
    1068794    .       .       .       .       .
    1068795    D       D       .       .       .
    1068796    .       .       .       .       .
    1068797    .       .       .       .       .

In the above example, bus ID 7 departs at timestamp `1068788` (seven minutes after `t`). This is fine; the only requirement on that minute is that bus ID 19 departs then, and it does.

Here are some other examples:

- The earliest timestamp that matches the list `17,x,13,19` is `3417`.
- `67,7,59,61` first occurs at timestamp `754018`.
- `67,x,7,59,61` first occurs at timestamp `779210`.
- `67,7,x,59,61` first occurs at timestamp `1261476`.
- `1789,37,47,1889` first occurs at timestamp `1202161486`.

However, with so many bus IDs in your list, surely the actual earliest timestamp will be larger than 100000000000000!

What is the earliest timestamp such that all of the listed bus IDs depart at offsets matching their positions in the list?

## Part 2 Math

19,x,x,x,x,x,x,x,x,41,x,x,x,37,x,x,x,x,x,787,x,x,x,x,x,x,x,x,x,x,x,x,13,x,x,x,x,x,x,x,x,x,23,x,x,x,x,x,29,x,571,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,17

| Bus `b` | Position (offset) |
| ------- | ----------------- |
| 19      | 0                 |
| 41      | 9                 |
| 37      | 13                |
| 787     | 19                |
| 13      | 32                |
| 23      | 42                |
| 29      | 48                |
| 571     | 50                |
| 17      | 67                |

Find `t` such that

    (t + offset_n) % b_n = 0

    (t + 19) mod 787 = 0
    (t + 50) mod 571 = 0
    (t + 9) mod 41 = 0
    (t + 13) mod 37 = 0
    (t + 48) mod 29 = 0
    (t + 42) mod 23 = 0
    (t + 0) mod 19 = 0
    (t + 67) mod 17 = 0
    (t + 32) mod 13 = 0

`t` can be generated from any of these following linear equations.

    787d - 19 = t
    571h - 50 = t
    41b - 9 = t
    37c - 13 = t
    29g - 48 = t
    23f - 42 = t
    19a - 0 = t
    17i - 67 = t
    13e - 32 = t

## Notes from Matt Schaffer

The first thing I noticed are all the prime numbers in your equations.  All the variables are multiplied by unique primes (787, 571, 41, etc.). The second thing I noticed is that, if you combine some of the equations, you can start to see some of the prime factors of two of the variables, namely `d` and `h`.  Here’s how to see that:

Notice that, if you subtract the second and third equations below, the result factors nicely.  Specifically you get

    571h - 50 - (41b - 9) = 0

Doing the algebra gives you the following:

    571h - 50 - 41b + 9 = 571h - 41b - 41 = 571h - 41(b + 1) = 0
    (or)
    571h = 41(b+1)

This means `h` must be divisible by 41. Now subtract the second and fourth equations, and you get

    571h = 37(c + 1), which means h must be divisible by 37

If you subtract the first and last equations, you get

    787d = 13(e - 1)

So your nine equations below can be re-written to the following seven equations

    571h = 41(b+1)
    571h = 37(c+1)
    571h = 17(i-1)

    787d = 19(a+1)
    787d = 13(e-1)
    787d = 29(g-1)
    787d = 23(f-1)

These equations tell you something about the prime factorization of `d` and `h`, namely that

    d = 13*19*23*29*D
    h = 17*37*41*H

So you can write the above seven equations as follows:

    571*17*37*H = b+1
    571*17*41*H = c+1
    571*37*41*H = i-1

    787*13*23*29*D = a+1
    787*19*23*29*D = e-1
    787*13*19*23*D = g-1
    787*13*19*29*D = f-1

## Conclusion

You can check values of `t` by incrementing `d` by `13*19*23*29` in the equation `787d - 19 = t`, since `d` must be divisible by `13*19*23*29`.
