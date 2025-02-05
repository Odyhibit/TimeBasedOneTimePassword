import base64

import htop_vanilla
import time


def totp(key: str, time_step: int = 30, digits: int = 6) -> str:
    """
    Generate a Time-Based One-Time Password (TOTP).

    :param key: The secret key (base32 encoded bytes)
    :param time_step: The time step in seconds (default is 30)
    :param digits: The number of digits in the OTP (default is 6)
    :return: TOTP as a string
    """
    current_time = int(time.time())
    counter = current_time // time_step

    return htop_vanilla.hotp(base32_decode(key), counter, digits)


def base32_decode(encoded: str) -> bytes:
    base32_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    encoded = encoded.rstrip('=')  # Remove padding
    binary_str = "".join(f"{base32_alphabet.index(char):05b}" for char in encoded if char in base32_alphabet)

    return bytes(int(binary_str[i : i + 8], 2) for i in range(0, len(binary_str), 8))


# Example usage
if __name__ == "__main__":
    test_key = 'NCHXDMEQ6L7IJXGN'  # Secret key (must be kept secure)
    totp = totp(test_key)
    print(f"TOTP: {totp}")
