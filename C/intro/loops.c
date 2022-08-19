#include <stdio.h>
 
int main()
{
    int x;
    /* The loop goes while x < 10, and x increases by one every loop*/
    for (x = 0; x < 10; x++) {
        printf("%d\n", x);
    }

    x = 0;

    // hell yeah, do while
    do
    {
        printf("%d ", x);
        x++;
    } while (x < 10);
    printf("\n");
 
    return 0;
}
