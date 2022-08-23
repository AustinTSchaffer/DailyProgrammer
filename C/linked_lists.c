#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

struct test_struct
{
    int val;
    struct test_struct *next;
};

// Pointer to the first element of the linked list, AKA the "head" of the list
struct test_struct *ll_head = NULL;

// Pointer to the last element of the linked list, AKA the "tail" of the list
struct test_struct *ll_tail = NULL;

// This function was created after the initial `main`
// code. It encapsulates the creation of a linked list.
struct test_struct *create_list(int val)
{
    printf("[create_list] creating list with headnode as [%d]\n", val);

    // Here's the same struct creation code.
    struct test_struct *ptr = (struct test_struct *)malloc(sizeof(struct test_struct));

    // Unsure of how this may happen. Possibly null
    // in the event the system is out of memory?
    if (NULL == ptr)
    {
        printf("[create_list] Node creation failed \n");
        return NULL;
    }

    ptr->val = val;
    ptr->next = NULL;

    ll_head = ll_tail = ptr;
    return ptr;
}

// This method incorporates the previous method, and
// adds some additional functionality for adding nodes
// to the beginning or end of the current list.
struct test_struct *add_to_list(int val, bool add_to_end)
{
    if (NULL == ll_head)
    {
        printf("[add_to_list] Adding node to end of list with value [%d]\n", val);
        return (create_list(val));
    }

    // Again, `malloc` might just return nothing for some reason.
    // Usually if that's the case, it's because the system decided
    // that my program doesn't deserve any additional memory.
    struct test_struct *ptr = (struct test_struct *)malloc(sizeof(struct test_struct));
    if (NULL == ptr)
    {
        printf("[add_to_list] Node creation failed \n");
        return NULL;
    }

    ptr->val = val;
    ptr->next = NULL;

    if (add_to_end)
        printf("[add_to_list] Adding node to end of list with value [%d]\n", val);
    else
        printf("[add_to_list] Adding node to beginning of list with value [%d]\n", val);

    if (add_to_end)
    {
        // If the intent is that this node will be the new _last_
        // node, then
        ll_tail->next = ptr;
        ll_tail = ptr;
    }
    else
    {
        // Otherwise, if the intent is that this node should be the new _head_
        // node, then
        ptr->next = ll_head;
        ll_head = ptr;
    }

    return ptr;
}

// This method finds and returns the element from the
// current linked list.
//
// The `struct test_struct **prev` allows the method
// to also return the previous node that points to the
// value. This functionality is invoked using the `&`
// operator against a pointer, which results in a
// "pointer to a pointer".
//
// Example in the delete method.
struct test_struct *search_in_list(int val, struct test_struct **prev)
{
    struct test_struct *_prev = NULL;
    struct test_struct *_curr = ll_head;
    bool found = false;

    printf("[search_in_list] Searching the list for value [%d]\n", val);

    while (NULL != _curr)
    {
        if (_curr->val == val)
        {
            found = true;
            break;
        }
        else
        {
            _prev = _curr;
            _curr = _curr->next;
        }
    }

    if (true == found)
    {
        if (prev)
            *prev = _prev;
        return _curr;
    }
    else
    {
        return NULL;
    }
}

// Deletes the first occurance of `val` from the
// current linked list.
// Returns -1 if `val` is not found.
// Returns 0 if `val` is found.
int delete_from_list(int val)
{
    struct test_struct *prev = NULL;
    struct test_struct *element_to_delete = NULL;

    printf("[delete_from_list] Deleting value [%d] from list\n", val);

    element_to_delete = search_in_list(val, &prev);

    if (element_to_delete == NULL)
    {
        printf("[delete_from_list] Value [%d] not found in list\n", val);
        return -1;
    }
    else
    {
        printf("[delete_from_list] Deleting value [%d] from list\n", val);

        // Time for some pointer shuffling
        if (element_to_delete == ll_head && element_to_delete == ll_tail)
        {
            ll_head = NULL;
            ll_tail = NULL;
        }
        else if (element_to_delete == ll_head)
        {
            ll_head = element_to_delete->next;
        }
        else
        {
            prev->next = element_to_delete->next;
        }
    }

    // Don't forget to free the memory and set the
    // pointer null!
    free(element_to_delete);
    element_to_delete = NULL;

    return 0;
}

void print_list(void)
{

    printf("[print_list] list: ");

    if (NULL == ll_head)
    {
        printf("(nil)\n");
        return;
    }

    printf("[%d]", ll_head->val);
    struct test_struct *ptr = ll_head->next;

    while (ptr != NULL)
    {
        printf("->[%d]", ptr->val);
        ptr = ptr->next;
    }

    printf("\n");
    return;
}

// Unused code snippets for messing around.
void unused_code()
{
    // A node is created by allocating memory to a structure
    // the pointer ‘ptr’ now contains address of a newly created node.
    struct test_struct *ptr = (struct test_struct *)malloc(sizeof(struct test_struct));

    // Initializes the values for the node, including
    // explicitly setting next to NULL. If you don't
    // set either:
    //   - val is 0
    //   - next is NULL/(nil)
    ptr->val = 123;
    ptr->next = NULL;

    // %p is the format specifier for pointers. We need to cast it to a
    // void* in order to prevent warnings.
    printf("%d %p\n", ptr->val, (void *)ptr->next);

    // Using the new method. The left side shows
    // that we're (1) declaring a "struct" variable,
    // (2) that's of type "test_struct", and (3)
    // is being stored as a pointer named "ptr2"
    struct test_struct *ptr2 = create_list(4);
    printf("%d %p\n", ptr2->val, (void *)ptr2->next);

    // Same as above, just using more "lines of code".
    struct test_struct *ptr3;
    ptr3 = create_list(17);
    printf("%d %p\n", ptr3->val, (void *)ptr3->next);

    // struct test_struct *ptr4;
    // printf("\"Null pointer exception\" results in a segmentation fault %p\n", ptr4->next);
}

int main()
{
    for (int i = 0; i < 5; i++)
    {
        add_to_list(i, true);
    }

    print_list();

    for (int i = 4; i >= 0; i--)
    {
        delete_from_list(i);
        print_list();
    }

    add_to_list(21, false);
    delete_from_list(20);
    delete_from_list(21);
    delete_from_list(22);
    add_to_list(5, false);
    add_to_list(6, true);
    add_to_list(7, false);
    add_to_list(8, true);
    add_to_list(9, false);
    add_to_list(10, true);
    add_to_list(11, false);
    print_list();
    delete_from_list(5);
    print_list();

    return 0;
}
