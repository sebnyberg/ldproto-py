import struct

def write_ld(writer, protomsg):
    """
    Write a length delimited protobuf message to the provided writer
    
    Arguments:
        writer: a writer, e.g. a file opened in 'wb' mode or a BytesIO or StringIO object
        protomsg: a protobuf message
    """
    # serialize the message to a bytes array
    s = protomsg.SerializeToString()
    
    # retrieve message length as a bytes block
    len_bytes = struct.pack('>L', len(s))
    
    # write message length + serialized message
    writer.write(len_bytes + s)


def read_ld(reader, msgtype):
    """
    Read length-delimited protobuf messages from the provided reader. Returns an iterator
    that can be used to traverse the messages found in the stream.

    Example:
        with open('path/to/file.ld', 'rb') as f:
            for msg in read_ld(f, pb.User):
                print(msg)
    
    Arguments:
        reader: a reader, e.g. a file opened with 'rb' or a BytesIO or StringIO object
        msgtype: the descriptor of the protobuf message, typically the name of the message,
            e.g. pb.User
    """
    while True:
        assert reader is not None, "reader is required"
        assert msgtype is not None, "msgtype is required"
        
        msg_len_bytes = reader.read(4)
        
        # EOF 
        if len(msg_len_bytes) == 0:
            return 
        
        # retrieve length prefix
        # struct.unpack always returns a tuple, even if there is only one element
        msg_len = struct.unpack('>L', msg_len_bytes)[0]
        
        # read message as a byte string
        proto_str = reader.read(msg_len)
        
        # EOF 
        if len(proto_str) == 0:
            return 
        
        # de-serialize the bytes into a protobuf message
        msg = msgtype()
        msg.ParseFromString(proto_str)
        yield msg