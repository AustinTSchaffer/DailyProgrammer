COOKIE_HEADER="$@"
echo "$COOKIE_HEADER"

PROBABLY_MAX_NUM_LINES=10000

for day in $(seq -w 16 16); do
    day_no_leading_0=$(echo $day | sed 's/^0//')
    local_dir="day_$day/"
    mkdir -p "$local_dir"
    base_url="https://adventofcode.com/2021/day/$day_no_leading_0"

    echo "Downloading $base_url"
    curl -s "$base_url" -H "$COOKIE_HEADER" \
        | egrep -A$PROBABLY_MAX_NUM_LINES -B0 '\<article\>.+' \
        | pandoc -f html -t commonmark \
        | egrep -B$PROBABLY_MAX_NUM_LINES -A0 '(Both parts of this puzzle are complete)?' \
        | sed -e 's/Both parts of this puzzle are complete.\+//' \
        > "$local_dir/problem.md"

    echo "Downloading $base_url/input"
    curl -s "$base_url/input" -H "$COOKIE_HEADER" > "$local_dir/input.txt"

    echo "Creating project files."
    touch "$local_dir/sln.py"
    ln -s ../common.py "$local_dir"
done
