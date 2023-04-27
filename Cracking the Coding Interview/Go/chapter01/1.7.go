package chapter01

import (
	"encoding/binary"
	"fmt"
)

// Pixel is a 4-byte struct that holds a single point of image data.
type Pixel interface {
	R() byte
	G() byte
	B() byte
	A() byte
}

// IntPixel represents the Pixel interface using a single 32-bit unsigned
// integer.
type IntPixel struct {
	Value uint32
}

// BasicPixel represents the Pixel interface using 4 individually named bytes.
type BasicPixel struct {
	R byte
	G byte
	B byte
	A byte
}

// getBytes returns the 4 bytes that represent the IntPixel using Big-Endian.
func (i IntPixel) getBytes() []byte {
	bytes := make([]byte, 4)
	binary.PutUvarint(bytes, uint64(i.Value))
	return bytes
}

// R gets the first 8 bits of i
func (i IntPixel) R() byte { return i.getBytes()[0] }

// G gets the second 8 bits of i
func (i IntPixel) G() byte { return i.getBytes()[1] }

// B gets the third 8 bits of i
func (i IntPixel) B() byte { return i.getBytes()[2] }

// A gets the last 8 bits of i
func (i IntPixel) A() byte { return i.getBytes()[3] }

/*

TransposeImage performs a matrix transpose on an image. This was accidentally
implemented while attempting to implement the ImageRotate function.

*/
func TransposeImage(image [][]Pixel) [][]Pixel {
	rows := len(image)
	columns := len(image[0])

	rotatedImage := make([][]Pixel, columns)
	for i := 0; i < columns; i++ {
		rotatedImage[i] = make([]Pixel, rows)
	}

	for i, row := range image {
		for j, pixel := range row {
			rotatedImage[j][i] = pixel
		}
	}

	return rotatedImage
}

/*

ImageRotate rotates a 2D slice of Pixels clockwise by 90 degrees. The input is
not changed and can have any dimensions.

*/
func ImageRotate(image [][]Pixel) [][]Pixel {
	rows := len(image)
	columns := len(image[0])

	rotatedImage := make([][]Pixel, columns)
	for i := 0; i < columns; i++ {
		rotatedImage[i] = make([]Pixel, rows)
	}

	for i, row := range image {
		for j, pixel := range row {
			rotatedImage[j][rows-1-i] = pixel
		}
	}

	return rotatedImage
}

/*

InPlaceImageRotate rotates a 2D image clockwise by 90 degrees, without creating
a new 2D slice of pixels. The input must be a square.

*/
func InPlaceImageRotate(image [][]Pixel) ([][]Pixel, error) {

	if image == nil || len(image) == 0 {
		return image, nil
	}

	size := len(image)

	for rownum, row := range image {
		rowlen := len(row)
		if rowlen != size {
			return image, fmt.Errorf(
				"Image must be square. Row %d expected length %d, actual %d",
				rownum, size, rowlen)
		}
	}

	inPlaceImageRotate(image)

	return image, nil
}

/*

inPlaceImageRotate rotates a square image clockwise by 90 degrees, recursively.

The algorithm works by rotating 4 points at a time, starting with the corners of
the image. One cycle consists of rotating all of the points in one "shell" of
the image, where a "shell" is all of the points on the perimeter of the image
that surround the points that have not yet been rotated.

	|  1  2  3  4 |
	|  5  6  7  8 |
	|  9 10 11 12 |
	| 13 14 15 16 |

In cycle 0, the shell consists of the points `[1, 2, 3, 4, 5, 8, 9, 12, 13, 14, 15, 16]`.
Points, `[1, 4, 13, 16]` are rotated first, followed by `[2, 8, 9, 15]`, then `[3, 5, 12, 14]`.
Notice how the collection of points that are rotated at one time is always 4 in
length. The number of collections that are rotated is also 1 less than the side
length of the current shell.

	| 13  9  5  1 |
	| 14  _  _  2 |
	| 15  _  _  3 |
	| 16 12  8  4 |

Repeating this process for cycle 1, points `[6, 7, 10, 11]` are rotated, finishing
the rotation for the whole image.

	|  _  _  _  _ |
	|  _ 10  6  _ |
	|  _ 11  7  _ |
	|  _  _  _  _ |

If the cycle only contains 1 point, the center element of a square with an odd
side length, then you can finish early.

The number of cycles (shells) in an image is equal to half the size of the
image, rounding up for images with odd side lengths. This detail in unimportant
since the algorithm is recursive.

*/
func inPlaceImageRotate(imageSlice [][]Pixel) {

	imageSize := len(imageSlice)
	maxIndex := imageSize - 1

	for groupNumber := 0; groupNumber < maxIndex; groupNumber++ {
		tmp := imageSlice[0][0+groupNumber]
		imageSlice[0][0+groupNumber] = imageSlice[maxIndex-groupNumber][0]
		imageSlice[maxIndex-groupNumber][0] = imageSlice[maxIndex][maxIndex-groupNumber]
		imageSlice[maxIndex][maxIndex-groupNumber] = imageSlice[0+groupNumber][maxIndex]
		imageSlice[0+groupNumber][maxIndex] = tmp
	}

	if imageSize <= 2 {
		return
	}

	newImageSliceSize := imageSize - 2
	newImageSlice := make([][]Pixel, newImageSliceSize)

	for i := 0; i < newImageSliceSize; i++ {
		newImageSlice[i] = imageSlice[i+1][1 : 1+newImageSliceSize]
	}

	inPlaceImageRotate(newImageSlice)
}

/*

main1dot7 runs an example usage of the functions and types that exist in this
file.

*/
func main1dot7() {
	// Wow this is awful. Definitely should be using openCV for image creation and manipulation.

	image1 := [][]Pixel{
		{IntPixel{Value: 1}, IntPixel{Value: 2}, IntPixel{Value: 3}, IntPixel{Value: 4}},
		{IntPixel{Value: 5}, IntPixel{Value: 6}, IntPixel{Value: 7}, IntPixel{Value: 8}},
		{IntPixel{Value: 9}, IntPixel{Value: 10}, IntPixel{Value: 11}, IntPixel{Value: 12}},
		{IntPixel{Value: 13}, IntPixel{Value: 14}, IntPixel{Value: 15}, IntPixel{Value: 16}},
	}

	fmt.Println("Original:", image1)
	newImage1 := ImageRotate(image1)
	fmt.Println("New Matrix Rotate:", newImage1)
	InPlaceImageRotate(image1)
	fmt.Println("In Place Rotate:", image1)

	image2 := [][]Pixel{
		{IntPixel{Value: 1}, IntPixel{Value: 2}, IntPixel{Value: 3}, IntPixel{Value: 4}, IntPixel{Value: 5}},
		{IntPixel{Value: 6}, IntPixel{Value: 7}, IntPixel{Value: 8}, IntPixel{Value: 9}, IntPixel{Value: 10}},
		{IntPixel{Value: 11}, IntPixel{Value: 12}, IntPixel{Value: 13}, IntPixel{Value: 14}, IntPixel{Value: 15}},
		{IntPixel{Value: 16}, IntPixel{Value: 17}, IntPixel{Value: 18}, IntPixel{Value: 19}, IntPixel{Value: 20}},
		{IntPixel{Value: 21}, IntPixel{Value: 22}, IntPixel{Value: 23}, IntPixel{Value: 24}, IntPixel{Value: 25}},
	}

	fmt.Println("Original:", image2)
	newImage2 := ImageRotate(image2)
	fmt.Println("New Matrix Rotate:", newImage2)
	InPlaceImageRotate(image2)
	fmt.Println("In Place Rotate:", image2)

	image3 := [][]Pixel{
		{IntPixel{Value: 1}, IntPixel{Value: 2}, IntPixel{Value: 3}},
		{IntPixel{Value: 4}, IntPixel{Value: 5}, IntPixel{Value: 6}},
	}

	fmt.Println("Original:", image3)
	newImage3 := ImageRotate(image3)
	fmt.Println("New Matrix Rotate:", newImage3)
}
