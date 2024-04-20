package data_encoder

import "fmt"

// decodeInteger decodes the first "numBytes" bytes of "data" as a
// little-endian integer. Returns an error if the "numBytes" parameter
// is more than 4 and/or the number of bytes in "data".
func decodeInteger(data []byte, numBytes int) (int, error) {
	if numBytes > 4 {
		return 0, fmt.Errorf(`cannot decode %d bytes to an int. must be <= 4`, numBytes)
	}

	if numBytes > len(data) {
		return 0, fmt.Errorf(`too few bytes to parse integer. len(data) = %d. numBytes = %d`, len(data), numBytes)
	}

	result := 0
	for i := range numBytes {
		result = result << 8
		result += int(data[numBytes-i-1])
	}

	return result, nil
}

// decodeDataInput decodes the "data" parameter as a DataInput instance,
// assuming that the "data" slice pointer has been advanced past the DataInputField tag.
// Returns an instance of a DataInput and the number of bytes consumed from
// "data", or an error.
func decodeDataInput(data []byte) (*DataInput, int, error) {
	dataInputLen, err := decodeInteger(data, DataInputLengthEncBytes)
	bytesConsumed := 2

	if err != nil {
		return nil, 0, err
	}

	result := make(DataInput, dataInputLen)
	for i := range dataInputLen {
		element, elementBytesConsumed, err := decodeField(data[bytesConsumed:])
		if err != nil {
			return nil, 0, err
		}

		result[i] = element
		bytesConsumed += elementBytesConsumed
	}

	return &result, bytesConsumed, nil
}

// decodeString decodes the `data` parameter as a string, assuming that the
// "data" slice pointer has been advanced past the StringField tag. Returns the
// string and the number of bytes consumed from `data`, or an error.
func decodeString(data []byte) (string, int, error) {
	stringLen, err := decodeInteger(data, StringLengthEncBytes)
	if err != nil {
		return "", 0, err
	}

	data = data[StringLengthEncBytes:]

	if len(data) < stringLen {
		return "", 0, fmt.Errorf(`too few bytes to decode string. len(data) = %d. stringLen = %d`, len(data), stringLen)
	}

	result := string(data[:stringLen])
	bytesConsumed := StringLengthEncBytes + stringLen

	return result, bytesConsumed, nil
}

// decodeInt32 decodes the `data` parameter as an int32, assuming that the
// "data" slice pointer has been advanced past the Int32Field tag. Returns
// the int32 and the number of bytes consumed from `data`, or an error.
// The integer is assumed to be little-endian.
func decodeInt32(data []byte) (int32, int, error) {
	result, err := decodeInteger(data, 4)
	if err != nil {
		return 0, 0, err
	}

	return int32(result), 4, nil
}

// decodeField decodes the field located at the 0th index of the "data" slice.
// Currently supports Int32, string, and DataInput fields.
func decodeField(data []byte) (interface{}, int, error) {
	if len(data) == 0 {
		return nil, 0, nil
	}

	switch data[0] {

	case Int32Field:
		result, bytesConsumed, err := decodeInt32(data[1:])
		if err != nil {
			return nil, 0, fmt.Errorf(`error decoding int32 field: %v`, err)
		}

		return result, bytesConsumed + 1, nil

	case StringField:
		result, bytesConsumed, err := decodeString(data[1:])
		if err != nil {
			return nil, 0, fmt.Errorf(`error decoding string field: %v`, err)
		}

		return result, bytesConsumed + 1, nil

	case DataInputField:
		result, bytesConsumed, err := decodeDataInput(data[1:])
		if result == nil || err != nil {
			return nil, 0, fmt.Errorf(`error decoding DataInput field: %v`, err)
		}

		return *result, bytesConsumed + 1, nil

	default:
		return nil, 0, fmt.Errorf("unsupported field type: %d", data[0])
	}
}

// Decode decodes a received UTF-8 string, assuming that it is an encoded
// DataInput instance. Returns an error if that is not possible, or if the
// received string contains extra characters which were not processed.
func Decode(received string) (*DataInput, error) {
	if len(received) > MaxEncodedDataLen {
		return nil, fmt.Errorf(`received message is too long. Length: %d. Max length: %d`, len(received), MaxEncodedDataLen)
	}

	receivedBytes := []byte(received)
	if receivedBytes[0] > CurrentVersion {
		return nil, fmt.Errorf(`unable to decode message. Current version: %d. Message version: %d`, CurrentVersion, receivedBytes[0])
	}

	result, bytesConsumed, err := decodeField(receivedBytes[1:])

	if err != nil {
		return nil, fmt.Errorf(`decode error: %v`, err)
	}

	bytesConsumed += 1 // Add an offset for the version check.
	if len(receivedBytes) != bytesConsumed {
		return nil, fmt.Errorf(`discrepancy between message size and bytes consumed. len(receivedBytes) = %d. bytesConsumed = %d`, len(receivedBytes), bytesConsumed)
	}

	if dataInput, ok := result.(DataInput); ok {
		return &dataInput, nil
	}

	return nil, fmt.Errorf(`message contains invalid top-level element type: %T`, result)
}
