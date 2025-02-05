"""
Built using FIPS 180-4 from https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
and rfc 3174 from  https://datatracker.ietf.org/doc/html/rfc3174
Since I am using bytes in Python I changed the math from bits to bytes for ease of coding,
for example 448 bits is 56 bytes, and 512 bits is 64 bytes (bytes = bits/8)
"""


def left_rotate(num: int, bits: int) -> int:
    """
    Left shift a number, and truncate the answer to 32 bits.

    :param num: number to shift (int32)
    :param bits: number of bits to left shift (0-31)
    :return: the number left shifted and truncated to 32 bits (int32)
    """
    return ((num << bits) | (num >> (32 - bits))) & 0xFFFFFFFF


def int_to_bytes(n: int, length: int) -> bytes:
    """
    Change an integer into bytes with a set length.

    :param n: the integer to change
    :param length: the number of bits to use
    :return: a bytes version of the input number with the specified number of bits.
    """
    return bytes((n >> (8 * (length - i - 1))) & 0xff for i in range(length))


def bytes_to_int(b: bytes) -> int:
    return sum((b[i] & 0xff) << (8 * (len(b) - i - 1)) for i in range(len(b)))


def sha1(message: bytes) -> bytes:
    """
    Generate a SHA-1 hash of a message in bytes.

    :param message: the message to be hashed (bytes)
    :return: the hash as bytes. use .hex() to print
    """
    # Values from FIPS PUB 180 (NSA)
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    # Pre-processing
    input_byte_length = len(message)
    input_bit_length = input_byte_length * 8

    # Append 1
    message += b'\x80'

    # Append 0's, so the message bit length is 56 (bytes long) after mod 64
    message += b'\x00' * ((56 - (input_byte_length + 1) % 64) % 64)

    # Append the input's length in bits at the end of the message
    message += int_to_bytes(input_bit_length, 8)

    # Process the message in successive 64 byte chunks
    for chunk_start in range(0, len(message), 64):
        chunk = message[chunk_start:chunk_start + 64]
        words = [bytes_to_int(chunk[i:i + 4]) for i in range(0, 64, 4)] + [0] * 64

        for i in range(16, 80):
            words[i] = left_rotate(words[i - 3] ^ words[i - 8] ^ words[i - 14] ^ words[i - 16], 1)

        a, b, c, d, e = h0, h1, h2, h3, h4

        for i in range(80):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:  # 60 <= i <= 79
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (left_rotate(a, 5) + f + e + k + words[i]) & 0xFFFFFFFF
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    # Convert the final hash values to bytes and concatenate them
    hash_bytes = (
            int_to_bytes(h0, 4) +
            int_to_bytes(h1, 4) +
            int_to_bytes(h2, 4) +
            int_to_bytes(h3, 4) +
            int_to_bytes(h4, 4)
    )

    return hash_bytes


# Example usage
if __name__ == "__main__":
    test_message = b"hello world"
    hash_value = sha1(test_message)
    print(f"SHA-1: {hash_value.hex()}")

