r"""

This module contains solutions to all of the problems proposed in Chapter 02 of
CtCI. The problems stated in the second chapter are primarily focused on linked
lists.

This module also contains a few classes that define an implementation for a
linked list.

"""

import ctci.chapter02.linked_lists

from ctci.chapter02._q01 import (
    remove_duplicates,
    remove_duplicates2,
)

from ctci.chapter02._q02 import (
    kth_element,
    kth_to_last_element,
)

from ctci.chapter02._q03 import (
    delete_middle_node,
)

from ctci.chapter02._q05 import (
    add_big_endian,
    to_big_endian_int,
    from_big_endian_int,
    add_little_endian,
    to_little_endian_int,
    from_little_endian_int,
)

from ctci.chapter02._q08 import (
    get_loop_element,
)


__all__ = [
    'linked_lists',
    'remove_duplicates',
    'remove_duplicates2',
    'kth_element',
    'kth_to_last_element',
    'delete_middle_node',
    'add_big_endian',
    'to_big_endian_int',
    'from_big_endian_int',
    'add_little_endian',
    'to_little_endian_int',
    'from_little_endian_int',
    'get_loop_element',
]
