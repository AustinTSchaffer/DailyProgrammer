package data_encoder

import (
	"fmt"
	"testing"
)

func TestDecodeNonFieldInteger(t *testing.T) {
	want := int(0b01010101_00110011_00001111_00000000)

	byteArray := []byte{0b00000000, 0b00001111, 0b00110011, 0b01010101}
	result, err := decodeInteger(byteArray, 4)

	if err != nil {
		t.Fatalf(`error decoding integer: %v`, err)
	}

	if result != want {
		t.Fatalf(`result = %d. Want %d`, result, want)
	}
}

func TestDecodeNonFieldIntegerErrorHandling(t *testing.T) {
	_, err := decodeInteger([]byte{0, 0, 0, 0}, 5)
	if err == nil {
		t.Fatalf(`expected error with decodeInteger([]byte{0, 0, 0, 0}, 5)`)
	}

	_, err = decodeInteger([]byte{0, 0, 0}, 4)
	if err == nil {
		t.Fatalf(`expected error with decodeInteger([]byte{0, 0, 0}, 4)`)
	}

	_, err = decodeInteger([]byte{}, 4)
	if err == nil {
		t.Fatalf(`expected error with decodeInteger([]byte{}, 4)`)
	}
}

func TestDecodeInt32Field(t *testing.T) {
	data := []byte{Int32Field, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0, 0, 0, 0, 0, 0}
	want := int32(-1)

	result, bytesConsumed, err := decodeField(data)
	if err != nil {
		t.Fatalf(`error decoding int32 field: %v`, err)
	}

	if bytesConsumed != 5 {
		t.Fatalf(`decodeField(%v) did not decode exactly 5 bytes. decoded: %d`, data, bytesConsumed)
	}

	result, ok := result.(int32)

	if !ok {
		t.Fatalf(`result is not assignable to an int32. Actual type: %T`, result)
	}

	if result != want {
		t.Fatalf(`result = %d. want = %d`, result, want)
	}
}

func TestDecodeStringField(t *testing.T) {
	data := []byte{StringField, 4, 0, 0, 'a', 's', 'd', 'f'}
	want := "asdf"

	result, bytesConsumed, err := decodeField(data)
	if err != nil {
		t.Fatalf(`error decoding string field: %v`, err)
	}

	if bytesConsumed != 8 {
		t.Fatalf(`decodeField(%v) did not decode exactly 8 bytes. decoded: %d`, data, bytesConsumed)
	}

	result, ok := result.(string)

	if !ok {
		t.Fatalf(`result is not assignable to a string. Actual type: %T`, result)
	}

	if result != want {
		t.Fatalf(`result = %s. want = %s`, result, want)
	}
}

func TestDecodeDataInputField(t *testing.T) {
	data := []byte{
		DataInputField, 1, 0,
		DataInputField, 3, 0,
		StringField, 4, 0, 0, 'a', 's', 'd', 'f',
		DataInputField, 1, 0,
		StringField, 4, 0, 0, 'q', 'w', 'e', 'r',
		Int32Field, 0b11111111, 0b11111111, 0b11111111, 0b01111111,
	}

	want := DataInput{
		DataInput{
			"asdf",
			DataInput{
				"qwer",
			},
			int32(0b01111111_11111111_11111111_11111111),
		},
	}

	result, bytesConsumed, err := decodeField(data)
	if err != nil {
		t.Fatalf(`error decoding DataInput field: %v`, err)
	}

	if bytesConsumed != 30 {
		t.Fatalf(`decodeField(%v) did not decode exactly 30 bytes. decoded: %d`, data, bytesConsumed)
	}

	result, ok := result.(DataInput)

	if !ok {
		t.Fatalf(`result is not assignable to a DataInput. Actual type: %T`, result)
	}

	if fmt.Sprintf(`%v`, result) != fmt.Sprintf(`%v`, want) {
		t.Fatalf(`result = %v. want = %v`, result, want)
	}
}

func TestDecode(t *testing.T) {
	data := []byte{
		DataInputField, 2, 0,
		DataInputField, 3, 0,
		StringField, 4, 0, 0, 'a', 's', 'd', 'f',
		DataInputField, 1, 0,
		StringField, 4, 0, 0, 'q', 'w', 'e', 'r',
		Int32Field, 0b11111111, 0b11111111, 0b11111111, 0b01111111,
		DataInputField, 3, 0,
		StringField, 4, 0, 0, 'z', 'x', 'c', 'v',
		DataInputField, 1, 0,
		StringField, 4, 0, 0, '1', '2', '3', '4',
		Int32Field, 0b00000000, 0b11111111, 0b11111111, 0b01111111,
	}

	want := DataInput{
		DataInput{
			"asdf",
			DataInput{
				"qwer",
			},
			int32(0b01111111_11111111_11111111_11111111),
		},
		DataInput{
			"zxcv",
			DataInput{
				"1234",
			},
			int32(0b01111111_11111111_11111111_00000000),
		},
	}

	result, bytesConsumed, err := decodeField(data)
	if err != nil {
		t.Fatalf(`error decoding DataInput field: %v`, err)
	}

	if bytesConsumed != 57 {
		t.Fatalf(`decodeField(%v) did not decode exactly 30 bytes. decoded: %d`, data, bytesConsumed)
	}

	result, ok := result.(DataInput)

	if !ok {
		t.Fatalf(`result is not assignable to a DataInput. Actual type: %T`, result)
	}

	if fmt.Sprintf(`%v`, result) != fmt.Sprintf(`%v`, want) {
		t.Fatalf(`result = %v. want = %v`, result, want)
	}
}
