# Length-Delimited Proto

When protobuf messages are either across the wire, or put in intermediary storage, it is helpful to be able to read and write individual messages in a streaming format.

This package exposes two methods:

* `write_ld(writer, protomsg)` - writes one instance of a protobuf message to the stream
* `read_ld(reader, msgtype) -> protomsg` - returns an iterable that yields messages from the stream one by one.

This package uses a big-endian unsigned 32-bit integer as the length-prefix.

## Example

Assuming there is a protobuf message with the type name "User"

```python
from ldproto import read_ld, write_ld
import myproto as pb

# .ld is for length-delimited
with open('out.user.ld', 'wb') as f:
    for user in users:
        write_ld(f, user)

pb_users = []
with open('out.user.ld', 'rb') as f:
    for pb_user in read_ld(f, pb.User):
        pb_users.append(user)
```

To write to / from a bytestream in-memory, use BytesIO in-place of the files in the example.
