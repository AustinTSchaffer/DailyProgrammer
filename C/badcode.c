#include <stdio.h>
#include <stdlib.h>

struct somestruct
{
    int a;
    float b;
    int c;
};

int main() {
    struct somestruct *x = malloc(sizeof(struct somestruct));
    x->a = 12;
    x->b = 13.2;

    printf("Freeing a struct leads to essentially random numbers.\n");
    printf("a->%d b->%f c->%d\n", x->a, x->b, x->c);
    free(x);
    printf("a->%d b->%f c->%d\n", x->a, x->b, x->c);

    return 0;
}
