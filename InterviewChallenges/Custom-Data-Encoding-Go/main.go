package main

import (
	"data_encoder/data_encoder"
	"fmt"
)

func main() {
	originalData := data_encoder.DataInput{"foo", data_encoder.DataInput{"bar", int32(42)}}

	fmt.Printf("Original data: %#v\n", originalData)

	encodedData, err := data_encoder.Encode(originalData)
	if err != nil {
		fmt.Printf("Error encoding data: %v\n", err)
		return
	}

	fmt.Printf("Encoded data: %q\n", encodedData)

	decodedData, err := data_encoder.Decode(encodedData)
	if err != nil {
		fmt.Printf("Error decoding data: %v\n", err)
		return
	}

	fmt.Printf("Decoded data: %#v\n", *decodedData)
}
