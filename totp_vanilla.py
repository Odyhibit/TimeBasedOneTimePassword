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
    print(f"Counter: {counter}")

    return htop_vanilla.hotp(key, counter, digits)


# Example usage
if __name__ == "__main__":
    test_key = b'12345678901234567890'  # Secret key (must be kept secure)
    totp = totp(test_key)
    print(f"TOTP: {totp}")
