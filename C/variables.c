#include <stdio.h>
 
int main()
{
    int this_is_a_number;
 
    printf("Please enter a number: ");

    // scanf reads formatted input from stdin
    // Reads the input and converts text to an integer.
    // If the input doesn't start with a number, it sets this_is_a_number to 0
    // If the input starts with a number, it takes numbers up until the first number
    // The & indicates that the function takes a reference
    // It's pretty easy to overwhelm this function with numbers that are too large
    scanf("%d", &this_is_a_number);

    printf("You entered %d", this_is_a_number);
    getchar();
    return 0;
}
