# Custom Data Encoder and Decoder

## Requirements

The original requirements document for this take-home assignment can be found here: [Requirements Document (link)](./Take_Home_ClickPipes.pdf)

To summarize, the objective was to design a custom ecoding format for serializing an array of data, such that it can be deserialized/decoded unambiguously. The encoding format must support arrays containing 32-bit integers, strings of arbitrary lengths, and arrays with the same definition. The serialization format must be byte-conservative, must have low algorithmic time and space complexity, and must not use any off-the-shelf serialization/encoding libraries from Go's standard library or otherwise.

There were a few other constraints imposed by the take-home description, including:

- `DataInput` arrays cannot contain more than 1,000 elements.
- Strings cannot contain more than 1M bytes.


## Usage

To run a quick demo of the encoding and decoding software

```bash
go run .
```

Output:

    Original data: []interface {}{"foo", []interface {}{"bar", 42}}
    Encoded data: "\x00\x02\x02\x00\x01\x03\x00\x00foo\x02\x02\x00\x01\x03\x00\x00bar\x00*\x00\x00\x00"
    Decoded data: []interface {}{"foo", []interface {}{"bar", 42}}

To run the project's unit tests:

```bash
go test ./...
```


## Implementation

My custom message serialization format is defined as follows.

- The first (0th) byte of each message contains the encoding version.
- The next byte should be a `0`, signifying the start of a `DataInput` field. This `DataInput` field follows the rules of all fields.

### Fields

A **field** is defined as follows.

- A single byte is used to denote the datatype of the field (int32, vs string, vs `DataInput`, etc). This byte is known as the field's "tag".
- An optional "length" section
  - This section exists for fields which have a variable length (e.g. strings and `DataInput` instances).
  - Fields which have a fixed length (e.g. int32) do not have a length section.
  - The existence of and the number of bytes required by each length section is defined independently for each field type.
- Some number of bytes for the contents of the field.
  - In the case of the `DataInput` field, the contents of the field are either empty, or contain additional fields.

### Supported Field Types

The current list of supported fields are

- `DataInput`
  - tag: `0`
  - 2-byte length section
    - unsigned little-endian short
    - signifies the number of elements contained by the `DataInput` instance (`N`)
  - The next `N` elements on the current layer belong to the `DataInput` instance.
  - For `DataInput`s containing `DataInput`s, think of each nested `DataInput` as being on a separate layer. For counting elements towards `N`, each DataInput only considers elements which exist on its layer. In practice, this is implemented using recursion.
- `int32`
  - tag: `1`
  - no length section
  - The next 4-bytes contain the int32 using little-endian encoding.
- `string`
  - tag: `2`
  - 3-byte length section
    - unsigned little-endian int24
    - signifies the number of bytes beloging to the string (`L` for length)
  - the next `L` bytes contain the string

### The Encoding Version

The version number contained within the first byte of every message is used by the decoder as a check to make sure that it can decode the message. If the encoding format is changed in a non-backwards-compatible way, this constant will be incremented. Backwards incompatible changes include 

- Changing the max allowed lengths of either strings or `DataInput` instances, such that it requires more bytes to describe their lengths.
- Altering the endianness of encoded integers.
- Adding more header fields to the message, beyond just a single version byte.
- Adding a 257th field type, which will require all field tags to use 2 bytes instead of 1.

Adding a new field which does not conflict with any existing fields is considered a backwards-compatible change. If the decoder sees a field tag that it does not recognize, it will abort processing of the current message. This will hopefully prevent exhausing all 256 version numbers in the current scheme.

### Adding Fields

To add a new field:

- Add a new field tag in `common.go`. Field tags are unique bytes that describe a single field type.
- Add support for the new field in `encode.go`, following the existing pattern.
- Add support for the new field in `decode.go`, following the existing pattern.
- Add unit tests for the new field.
- Document the new field in this Readme.

### Time and Space Complexity

This implementation has both $O(n)$ time and $O(n)$ space complexity, where $n$ is the number of bytes required to represent the `DataInput` instance in a Go process's memory. Both the encode and decode functions scan the data only once, either to convert the `DataInput` instance directly to a byte array, or to convert a byte array back into a `DataInput` instance.


## Inspiration

I borrowed a lot of knowledge and inspiration from work that I did at Everactive related to parsing byte-array payloads containing [TLV](https://en.wikipedia.org/wiki/Type%E2%80%93length%E2%80%93value) and [TLV-BER](https://en.wikipedia.org/wiki/X.690#BER_encoding) data. Everactive's sensors transmit data encoded in a custom TLV-BER format, which is processed by their cloud ingest. This meant that new sensor capabilities required engineering time from the cloud team to process raw byte arrays.

The most common issue with this work was with due to the endianness of integers that were packed into sensor data payloads. Field encoding was documented on Confluence, and there were no automated tools for performing serialization/deserialization across our various runtimes.

My custom serialization format is also similar to how Protobuf serializes data. I believe that a custom byte array serialization format can be equivalently, if not more byte-conservative compared to Protobuf. However, in my opinion, Protobuf is better in every other possible regard (documentation, code generation, type safety, endianness concerns, available tooling, etc).
