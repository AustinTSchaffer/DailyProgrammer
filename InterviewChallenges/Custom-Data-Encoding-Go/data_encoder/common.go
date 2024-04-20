package data_encoder

type DataInput = []interface{}

const (
	CurrentVersion byte = 0

	DataInputMaxStringLen = 1_000_000
	StringLengthEncBytes  = 3 // Max length supported: ~16M

	DataInputMaxElemments = 1_000
	DataInputLengthBytes  = 2 // Max length supported: 65535

	// Pessimistic maxumum buffer size, assuming a DataInput containing
	// DataInputMaxElemments strings of length DataInputMaxStringLen.
	MaxBufferSize = 1 + (DataInputMaxElemments * (1 + StringLengthEncBytes + DataInputMaxStringLen))

	// Decoding constraint.
	MaxEncodedDataLen = MaxBufferSize

	// Field Tags
	Int32Field     byte = 0
	StringField    byte = 1
	DataInputField byte = 2
)
