import hmac_vanilla


def hotp(key: bytes, counter: int, digits: int = 6):
    """
    Generate an HMAC-Based One-Time Password (HOTP).

    :param key: The secret key (bytes)
    :param counter: The counter value (integer)
    :param digits: The number of digits in the OTP (default is 6)
    :return: HOTP as a string
    """

    # Generate HMAC using the key and counter
    hmac_result = hmac_vanilla.hmac(key, counter.to_bytes(8, byteorder="big"))

    # Dynamic truncation (RFC 4226, section 5.3)
    offset = hmac_result[-1] & 0x0F  # Get the last 4 bits as the offset
    truncated_hash = hmac_result[offset:offset + 4]  # Get 4 bytes starting at the offset

    # Convert the truncated hash to an integer
    hotp_value = int.from_bytes(truncated_hash, byteorder='big') & 0x7FFFFFFF  # Mask to 31 bits

    # Reduce the value to the desired number of digits
    hotp_value = hotp_value % (10 ** digits)

    # Return the HOTP as a zero-padded string
    return f"{hotp_value:0{digits}d}"


# Example usage
if __name__ == "__main__":
    key = b'12345678901234567890'  # Secret key (must be kept secure)
    counter = 0  # Counter value (incremented after each use)
    hotp = hotp(key, counter)
    print(f"HOTP: {hotp}")
