import sha_1_vanilla


def hmac(key: bytes, message: bytes) -> bytes:
    """
    HMAC implementation using SHA-1 from the sha_1_vanilla.py file.

    :param key: The secret key (bytes).
    :param message: The message to authenticate (bytes).
    :return: HMAC as a bytes.
    """

    block_size = 64

    # If the key is longer than the block size, hash it
    if len(key) > block_size:
        key = sha_1_vanilla.sha1(key)

    # If the key is shorter than the block size, pad it with zeros
    if len(key) < block_size:
        key += b'\x00' * (block_size - len(key))

    # Create the inner and outer padded keys
    o_key_pad = bytes([x ^ 0x5c for x in key])  # Outer padded key
    i_key_pad = bytes([x ^ 0x36 for x in key])  # Inner padded key

    # Inner hash: hash(i_key_pad + message)
    inner_hash = sha_1_vanilla.sha1(i_key_pad + message)

    # Outer hash: hash(o_key_pad + inner_hash)
    outer_hash = sha_1_vanilla.sha1(o_key_pad + inner_hash)

    return outer_hash


# Example usage
if __name__ == "__main__":
    test_key = b"secret_key"
    test_message = b"Hello, World!"
    hmac_result = hmac(test_key, test_message)
    print("HMAC:", hmac_result.hex())