Today's daily challenge is described by these 5 rows from `levelpack_d1.txt`

    5,50,1,5;11,16,17,18;10,15,20,21,22,23,24,19,14,13,8;6,7,12;1,0,5;9,4,3,2
    8,50,2,6;49,50,51,52,53,54;38,39,31,23,15,7,6,5,4;21,20,19,27,35,43,42,41;18,26,34,33,32,40,48,56,57,58,59,60,61,62,63,55,47,46,45,37;44,36,28,29,30,22,14,13,12,11,10,9,17;3,2,1,0,8,16,24,25
    8,50,3,5;54,46,38,30,22,14,13,12,11,10,9;40,48,56,57,58,59,51,43,35,36;28,27,26,34,42,50,49;32,24,16,8,0,1,2,3,4,5,6,7,15,23,31,39,47,55,63,62,61,60,52,44;41,33,25,17,18,19,20,21,29,37,45,53
    7,50,4,5;16,17,18,25,26,27;47,48,41,34,33,32,31,38;20,13,6,5,4,3,2,1,0,7,14,21;19,12,11,10,9,8,15,22,29,28,35,42,43,44,45,46,39,40;24,23,30,37,36
    5,50,5,3;15,10,11,12;20,21,16,17,18,13,8,7,6,5,0;22,23,24,19,14,9,4,3,2,1

All of these levels are square. These 5 levels re described by the sizes `5x5`, `8x8`, `8x8`, `7x7`, and `5x5`. Let's take the first encoded level as an example

    5,50,1,5;11,16,17,18;10,15,20,21,22,23,24,19,14,13,8;6,7,12;1,0,5;9,4,3,2

- This corresponds with level 1 of 5 for daily challenge Dec 26, 2022.
- The string is delimited by `;`, then by `,`
- The first grouping `5,50,1,5` describes the level's metadata
    - `5` is the size, `5x5`. For rectangular levels, this identifier is specified `width:height`. For completeness, this level's size could be specified as `5:5`. All of the other level information is identical between square and rectangle levels.
    - `50` is the daily challenge collection ID. This `50` somehow refers to Dec 26, 2022. This ID is constant for all 5 of these levels.
    - `1` refers to the ID within the collection. This ID increments starting at 1 for each level in a collection.
    - The 2nd `5` refers to the number of flows (colors) within the level. This level has 5.
- Each following grouping describes one of the flows within the level.
    - Each grouping actually describes the full path of each flow within the level.
    - The elements in these groupings identify cells within the grid. The cells in the grid are identified starting with 0 in the bottom left corner, and increment row-wise.
    - The first and last elements refer to the source and sink of the flow. Each element in between describes the path from the first to the last element.
    - Grouping `11,16,17,18` as an example. Start at cell `11` (using 1-indexing, row 3 from bottom, column 2 from left). Move up one cell to cell `16`. Move right to cell `17`. Move right to cell `18`.

This is all we should need to reproduce rectangular levels.
