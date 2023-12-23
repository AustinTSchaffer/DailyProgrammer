# AoC 2023 Day 21 Notes

Using BFS is obviously not efficient above a certain level for part 2. For one, it's a little odd that the prompt contains no value for the sample input and 26501365 steps, so there's no way to make sure that the most efficient methodology works at the scale of the actual input search area.

Below are links to some files output by [worksheet.py](worksheet.py) for various step counts. Only the sample is contained in this repository, to prevent the input from leaking to the public.

- [./explored/sample/steps_100.txt](./explored/sample/steps_100.txt)
- [./explored/sample/steps_200.txt](./explored/sample/steps_200.txt)
- [./explored/sample/steps_300.txt](./explored/sample/steps_300.txt)
- [./explored/sample/steps_400.txt](./explored/sample/steps_400.txt)
- [./explored/sample/steps_500.txt](./explored/sample/steps_500.txt)

## Some notes

- For the repeated input blocks:
  - The input and sample input both contain a border which does not contain any rocks.
- The final search area resembles a diamond.
    - Every other node in the interior of the diamond is either a visited node (`O`) or a rock (`#`).
    - The perimiter of the diamond has the same property as the interior of the diamond.
    - Not all of the nodes that would form the border of the diamond are visited. This is due to pathing around obstacles at the very edge of the number of available steps.
- For the interior blocks:
  - Every other node is either a `O` or a `#`. In the interior, there are no empty gardens `.` that are isolated in a subgraph.
  - For each adjacent block of the input size, the pattern of visited nodes toggles between 2 different configurations.
- For the exterior blocks:
  - These are blocks of the input size that contain a segment of the perimiter of the diamond.
  - These blocks can be separated into 2 categories:
    - Corner blocks, of which there are 4.
      - These are blocks that contain a corner of the diamond's perimeter.
      - The corners of the diamond cannot fall on the border between 2 different blocks, since the starting location is in the center of the original input block.
      - These blocks are unique.
    - Edge blocks.
      - These are blocks which contain a section of the perimeter of the diamond, but do not contain a corner.
      - For each edge of the diamond, there are only 2 unique edge blocks. Refer to one of the explored sample files from earlier. Note the repeating pattern between pairs of consecutive blocks.

## Ideas for an algorithm.

- We can determine the number of blocks that the diamond will intersect, without doing any searching.
- We can determine the number of blocks which fall on the interior and the number of blocks which are exterior, containing a segment of the perimeter.
- For blocks that fall on the interior, we can determine:
  - The number of blocks which have one parity vs another.
  - How many nodes are "reachable" within each parity of an input block.
- For blocks that fall on the exterior, we can determine:
  - How many steps it took to reach each node on the edge of the block
  - How many nodes are reachable within the block given the number of steps remaining

## Better ideas for an algorithm

I bet that this problem has 262 separate closed-form solutions.
