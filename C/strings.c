#include <string.h>
#include <stdio.h>

/*

Most important C functions for strings.

strlen()    Get length of a string.
strcpy()    Copy one string to another.
strcat()    Link together (concatenate) two strings.
strcmp()    Compare two strings.
strchr()    Find character in string.
strstr()    Find string in string.
strlwr()    Convert string to lowercase.
strupr()    Convert string to uppercase.

*/

int main()
{
    // strings in C are a pointer to a character.
    char *t = "XXX";
    printf("Length of <%s> is %d.\n", t, strlen(t));

    // strings can also be represented by character arrays.
    char s1[100],
        s2[100];

    // strcpy can be used to 
    strcpy(s1, "xxxxxx 1");
    strcpy(s2, "zzzzzz 2");

    puts("Original strings: ");
    puts("");
    puts(s1);
    puts(s2);
    puts("");

    strcpy(s2, s1);

    puts("New strings: ");
    puts("");
    puts(s1);
    puts(s2);

    return 0;
}
