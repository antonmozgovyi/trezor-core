import ustruct


def write_uint32(w, n: int):
    write_bytes(w, ustruct.pack('>L', n))


def write_uint64(w, n: int):
    write_bytes(w, ustruct.pack('>Q', n))


def write_bytes(w, buf: bytearray):
    w.extend(buf)


def write_bool(w, val: True):
    if val:
        write_uint32(w, 1)
    else:
        write_uint32(w, 0)


def write_pubkey(w, pubkey: bytes):
    # first 4 bytes of an address are the type, there's only one type (0)
    write_uint32(w, 0)
    write_bytes(w, bytearray(pubkey))
