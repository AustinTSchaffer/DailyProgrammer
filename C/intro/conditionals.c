#include <stdio.h>
#include <stdbool.h>

#define BOOL char
#define TRUE 0
#define FALSE 1

int main()
{
    // "true" and "false" require the stdbool preprocessor
    if (true) {
        printf("hi!\n");
    } else {
        printf("not hi\n");
    }

    // Most people use this format for booleans:
    if (TRUE) {
        printf("boolean but defined\n");
    }

    if (1 > 0) {
        printf("1 is still more than 0\n"); // semicolons are NOT optional
    }

    int age;
    printf("Please enter your age (in years): ");
    scanf("%d", &age);
    if (age < 100) {
        printf ("You are less than 100 years old!\n");
    }
    else if (age == 100) {
        printf("You are exactly 100 years old\n");
    }
    else {
        printf("You are not exactly 100 years old, but also not less than 100 years old? What would you call that...\n");
    }

    return 0;
}
