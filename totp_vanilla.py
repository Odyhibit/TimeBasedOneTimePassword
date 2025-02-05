import base64

import htop_vanilla
import time


def totp(key: bytes, time_step: int = 30, digits: int = 6) -> str:
    """
    Generate a Time-Based One-Time Password (TOTP).

    :param key: The secret key (bytes)
    :param time_step: The time step in seconds (default is 30)
    :param digits: The number of digits in the OTP (default is 6)
    :return: TOTP as a string
    """
    current_time = int(time.time())
    counter = current_time // time_step
    print(f"Counter: {counter} epoch: {current_time}")

    return htop_vanilla.hotp(key, counter, digits)


def base32_decode(encoded: str) -> bytes:
    base32_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    encoded = encoded.rstrip('=')  # Remove padding
    binary_str = "".join(f"{base32_alphabet.index(char):05b}" for char in encoded if char in base32_alphabet)

    return bytes(int(binary_str[i : i + 8], 2) for i in range(0, len(binary_str), 8))


# Example usage
if __name__ == "__main__":
    base32_key = 'NCHXDMEQ6L7IJXGN'  # Secret key (must be kept secure)
    test_key = base32_decode(base32_key)
    totp = totp(test_key)
    print(f"TOTP: {totp}")
