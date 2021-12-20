COOKIE_HEADER="$@"
echo "$COOKIE_HEADER"

PROBABLY_MAX_NUM_LINES=10000

for day in $(seq -w 1 25); do
    day_no_leading_0=$(echo $day | sed 's/^0//')
    mkdir -p day_$day/
    echo "Downloading https://adventofcode.com/2021/day/$day_no_leading_0"
    curl -s "https://adventofcode.com/2021/day/$day_no_leading_0" -H "$COOKIE_HEADER" \
        | egrep -A$PROBABLY_MAX_NUM_LINES -B0 '\<article\>.+' \
        | pandoc -f html -t commonmark \
        | egrep -B$PROBABLY_MAX_NUM_LINES -A0 'Both parts of this puzzle are complete' \
        | sed -e 's/Both parts of this puzzle are complete.\+//' \
        > "day_$day/problem.md"
done
