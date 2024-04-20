package data_encoder

import (
	"fmt"
)

// encodeInteger encodes an integer using litte-endian format. numBytes
// determines the number of bytes that will be written to encodedData.
// Returns a slice pointing to the next available index of encodedData.
func encodeInteger(encodedData *([]byte), integer int, numBytes int) {
	offset := 0
	for range numBytes {
		*encodedData = append(*encodedData, byte((integer>>offset)&255))
		offset += 8
	}
}

// encodeStringField encodes a string into the encodedData byte array.
// The first byte will contain the "StringField" tag. The next 3 bytes
// will contain the length of the string, using litte-endian encoding.
// The next N bytes will contain the string's bytes, where N is the length
// of the string. Returns a slice pointing to the next available index of
// encodedData.
func encodeStringField(encodedData *([]byte), data string) error {
	*encodedData = append(*encodedData, StringField)

	stringLen := len(data)
	if stringLen > DataInputMaxStringLen {
		// TODO: Error formatting
		return fmt.Errorf("input string too long. Length %d. Max Length %d", stringLen, DataInputMaxStringLen)
	}

	// encode the length of the string as a 3-byte integer (max value: ~16M)
	encodeInteger(encodedData, stringLen, 3)

	// copy the string's bytes into the encoded array.
	*encodedData = append(*encodedData, data...)

	return nil
}

// encodeInt32Field encodes an int32 into the encodedData byte array.
// The first byte will contain the "Int32Field" tag. The next 4 bytes
// will contain the int32, using litte-endian encoding. Returns a slice
// pointing to the next available index of encodedData.
func encodeInt32Field(encodedData *([]byte), data int32) {
	*encodedData = append(*encodedData, Int32Field)
	encodeInteger(encodedData, int(data), 4)
}

// encodeDataInputField encodes a DataInput slice into the encodedData byte
// array. The first byte will contain the "DataInputField" tag. The next 2
// bytes will contain the length of the DataInput field. Returns a slice
// pointing to the next available index of encodedData.
func encodeDataInputField(encodedData *([]byte), dataInputNumElements *int, data DataInput) error {
	if dataInputNumElements == nil {
		val := 1
		dataInputNumElements = &val
	}

	if *dataInputNumElements == 0 {
		*dataInputNumElements = 1
	}

	*encodedData = append(*encodedData, DataInputField)

	dataInputLen := len(data)
	if dataInputLen > DataInputMaxElemments {
		return fmt.Errorf("too many elements in data input. Data input length: %d. Max length allowed: %d", dataInputLen, DataInputMaxElemments)
	}

	// encode the length of the DataInput slice
	encodeInteger(encodedData, dataInputLen, DataInputLengthBytes)

	for _, element := range data {
		(*dataInputNumElements) += 1
		if (*dataInputNumElements) > DataInputMaxElemments {
			return fmt.Errorf("too many elements in data input. Max length allowed %d", DataInputMaxElemments)
		}

		switch v := element.(type) {
		case int32:
			encodeInt32Field(encodedData, element.(int32))
		case string:
			err := encodeStringField(encodedData, element.(string))
			if err != nil {
				return err
			}
		case DataInput:
			err := encodeDataInputField(encodedData, dataInputNumElements, element.(DataInput))
			if err != nil {
				return err
			}
		default:
			// TODO: Proper formatting for this.
			return fmt.Errorf("unsupported type: %v", v)
		}
	}

	return nil
}

func Encode(toSend DataInput) (string, error) {
	encodedData := make([]byte, 1)

	encodedData[0] = CurrentVersion

	err := encodeDataInputField(&encodedData, nil, toSend)
	if err != nil {
		return "", err
	}

	return string(encodedData[:]), nil
}
