package main

import (
	"data_encoder/data_encoder"
	"fmt"
	"strconv"
)

func main() {
	originalData := data_encoder.DataInput{"foo", data_encoder.DataInput{"bar", int32(42)}}

	fmt.Printf("Original data: %#v\n", originalData)

	encodedData, err := data_encoder.Encode(originalData)
	if err != nil {
		fmt.Printf("Error encoding data: %v\n", err)
		return
	}

	fmt.Printf("Encoded data: %s\n", encodedData)

	decodedData, err := data_encoder.Decode(encodedData)
	if err != nil {
		fmt.Printf("Error decoding data: %v\n", err)
		return
	}

	fmt.Printf("Decoded data: %#v\n", *decodedData)

	x := int32(100200300)

	x_0 := byte(x&255)
	x_1 := byte((x>>8)&255)
	x_2 := byte((x>>16)&255)
	x_3 := byte((x>>24)&255)

	fmt.Println("x =", x)
	fmt.Println("x =", strconv.FormatInt(int64(x), 2))

	fmt.Println("x_0 =", x_0)
	fmt.Println("x_0 =", strconv.FormatInt(int64(x_0), 2))
	fmt.Println("x_1 =", x_1)
	fmt.Println("x_1 =", strconv.FormatInt(int64(x_1), 2))
	fmt.Println("x_2 =", x_2)
	fmt.Println("x_2 =", strconv.FormatInt(int64(x_2), 2))
	fmt.Println("x_3 =", x_3)
	fmt.Println("x_3 =", strconv.FormatInt(int64(x_3), 2))
}
