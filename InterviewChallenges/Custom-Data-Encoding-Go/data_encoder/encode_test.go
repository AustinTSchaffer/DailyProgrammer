package data_encoder

import (
	"testing"
)

func TestEncodeNonFieldInteger(t *testing.T) {
	integer := int(0b01010101_00110011_00001111_00000000)

	byteArray := make([]byte, 0)
	want := []byte{0b00000000, 0b00001111, 0b00110011, 0b01010101}
	encodeInteger(&byteArray, integer, 4)

	if len(byteArray) != 4 {
		t.Fatalf(`len(byteArray) = %d. Want %d`, len(byteArray), 4)
	}

	for i := range 4 {
		if byteArray[i] != want[i] {
			t.Fatalf(`byteArray[%d] = %d. Want %d`, i, byteArray[i], want[i])
		}
	}

	integer = int(0b11111111_00110011_00001111_00000000)
	want = []byte{0b00000000, 0b00001111, 0b00110011}
	encodeInteger(&byteArray, integer, 3)

	if len(byteArray) != 7 {
		t.Fatalf(`len(byteArray) = %d. Want %d`, len(byteArray), 7)
	}

	for i := range 3 {
		if byteArray[i+4] != want[i] {
			t.Fatalf(`byteArray[%d] = %d. Want %d`, i+4, byteArray[i+4], want[i])
		}
	}
}

func TestEncodeInt32Field(t *testing.T) {
	integer := int32(0b00110011_11110000_01010101_10101010)

	byteArray := make([]byte, 0)
	want := []byte{Int32Field, 0b10101010, 0b01010101, 0b11110000, 0b00110011}
	encodeInt32Field(&byteArray, integer)

	for i := range len(want) {
		if byteArray[i] != want[i] {
			t.Fatalf(`byteArray[%d] = %d. Want %d`, i, byteArray[i], want[i])
		}
	}
}

func TestEncodeStringField(t *testing.T) {
	data := "The lorem ipsum fox jumped over the sit dolor dog."
	stringLen := len(data)

	byteArray := make([]byte, 0)
	fieldHeaderWant := []byte{StringField, byte(stringLen), 0, 0}
	err := encodeStringField(&byteArray, data)

	if err != nil {
		t.Fatalf(`error while encoding string field: %v`, err)
	}

	if len(byteArray) != (4 + stringLen) {
		t.Fatalf(`len(byteArray) = %d. Want %d`, len(byteArray), (4 + stringLen))
	}

	for i := range len(fieldHeaderWant) {
		if byteArray[i] != fieldHeaderWant[i] {
			t.Fatalf(`byteArray[%d] = %d. Want %d`, i, byteArray[i], fieldHeaderWant[i])
		}
	}

	for i, dataByte := range []byte(data) {
		if byteArray[i+4] != dataByte {
			t.Fatalf(`byteArray[%d] = %d. Want %d`, i+4, byteArray[i+4], data[i])
		}
	}
}

func TestEncodeDataInputField(t *testing.T) {
	originalData := DataInput{
		"foo",
		DataInput{
			"bar",
			int32(42),
		},
		DataInput{},
		"baz",
	}

	originalDataNumElementsWant := 7

	want := []byte{
		DataInputField, 4, 0,
		StringField, 3, 0, 0, 'f', 'o', 'o',
		DataInputField, 2, 0,
		StringField, 3, 0, 0, 'b', 'a', 'r',
		Int32Field, 42, 0, 0, 0,
		DataInputField, 0, 0,
		StringField, 3, 0, 0, 'b', 'a', 'z',
	}

	byteArray := make([]byte, 0)
	originalDataNumElements := 0
	err := encodeDataInputField(&byteArray, &originalDataNumElements, originalData)

	if err != nil {
		t.Fatalf(`error while encoding DataInput field: %v`, err)
	}

	if originalDataNumElements != originalDataNumElementsWant {
		t.Fatalf(`originalDataNumElements = %d. Want: %d`, originalDataNumElements, originalDataNumElementsWant)
	}

	if len(byteArray) != len(want) {
		t.Fatalf(`len(byteArray) = %d. Want: %d`, len(byteArray), len(want))
	}

	for i, dataByte := range want {
		if byteArray[i] != dataByte {
			t.Fatalf(`byteArray[%d] = %d. Want %d`, i, byteArray[i], dataByte)
		}
	}
}

func TestEncodeDataInputErrorHandling(t *testing.T) {
	_, err := Encode(DataInput{int64(15)})
	if err == nil {
		t.Fatalf(`int64 is not supported`)
	}

	_, err = Encode(DataInput{[]byte{1, 2, 3}})
	if err == nil {
		t.Fatalf(`[]byte is not supported`)
	}

	di := DataInput{}
	for i := range MaxDataInputElements - 1 {
		di = append(di, int32(i))
	}
	_, err = Encode(di)
	if err != nil {
		t.Fatalf(`Encode(di) returned error: %v`, err)
	}

	di = DataInput{}
	for i := range MaxDataInputElements {
		di = append(di, int32(i))
	}
	_, err = Encode(di)
	if err == nil {
		t.Fatalf(`Encode(di) should have errored due to too many elements`)
	}
}

// TestEncode encodes an example DataInput instance to an
// encoded string.
func TestEncode(t *testing.T) {
	originalData := DataInput{"foo", DataInput{"bar", int32(42)}}

	want := "\x00\x00\x02\x00\x02\x03\x00\x00foo\x00\x02\x00\x02\x03\x00\x00bar\x01*\x00\x00\x00"
	result, err := Encode(originalData)

	if want != result || err != nil {
		t.Fatalf(`Encode(originalData) = %q, %v, want match for %#q, nil`, result, err, want)
	}
}
