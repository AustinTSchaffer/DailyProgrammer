package data_encoder

import "fmt"

func Decode(received string) (*DataInput, error) {
	if len(received) > MaxEncodedDataLen {
		return nil, fmt.Errorf(`received too long. Length: %d. Max length: %d`, len(received), MaxEncodedDataLen)
	}

	receivedBytes := []byte(received)
	if receivedBytes[0] >= CurrentVersion {
		return nil, fmt.Errorf(`unable to decode message. Current version: %d. Message version: %d`, CurrentVersion, receivedBytes[0])
	}

	return &DataInput{}, nil
}
