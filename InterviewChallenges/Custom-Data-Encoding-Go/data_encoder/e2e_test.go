package data_encoder

import (
	"testing"
)

func TestEncodeDecodeEmojis(t *testing.T) {
	data := DataInput{"😀😃😄😁 plus some UTF-8 text followed by 😆😅😂🤣", int32(871623871)}

	encoded, err := Encode(data)
	if err != nil {
		t.Fatalf(`error encoding data: %v`, err)
	}

	decoded, err := Decode(encoded)
	if err != nil {
		t.Fatalf(`error decoding data: %v`, err)
	}

	if (*decoded)[0] != data[0] {
		t.Fatalf(`emoji string did not survive encoding/decoding. %s != %s`, (*decoded)[0], data[0])
	}

	if (*decoded)[1] != data[1] {
		t.Fatalf(`int32 did not survive encoding/decoding. %d != %d`, (*decoded)[1], data[1])
	}
}
