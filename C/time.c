#include <stdio.h>
#include <time.h>

void wait(int sec)
{
    clock_t end_wait;
    end_wait = clock() + (sec * CLOCKS_PER_SEC);

    while (clock() < end_wait) {}
}

int main()
{
    time_t sec = time(NULL);
    printf("Number of hours since January 1, 1970 is %ld\n", sec / 3600);

    time_t sometime = time(NULL);
    printf("%s\n", ctime(&sometime));

    struct tm str_time;

    // So I've learned that the arrow operator is syntactic sugar
    // for whatever this is.
    str_time.tm_year = 2012 - 1900;
    str_time.tm_mon = 6;
    str_time.tm_mday = 12;
    str_time.tm_hour = 2;
    str_time.tm_min = 32;
    str_time.tm_sec = 55;
    str_time.tm_isdst = 0;

    time_t time_of_day = mktime(&str_time);
    printf("%s\n", ctime(&time_of_day));

    // Diffing the time

    // Check it out, one line, many variables declared.
    time_t start, end;

    start = time(NULL);

    // 6 second wait
    wait(6);

    end = time(NULL);

    printf("The loop took %f seconds.\n", difftime(end, start));

    return 0;
}
