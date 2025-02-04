import htop_vanilla
import time


def totp(key, time_step=30, digits=6):
    """
    Generate a Time-Based One-Time Password (TOTP).

    :param key: The secret key (bytes)
    :param time_step: The time step in seconds (default is 30)
    :param digits: The number of digits in the OTP (default is 6)
    :return: TOTP as a string
    """
    # Get the current Unix time
    print(f"Current Time: {time.time()}")
    current_time = int(time.time())
    print(f"Epoch: {current_time}")

    # Calculate the counter value (number of time steps since the epoch)
    counter = current_time // time_step
    print(f"Counter: {counter}")

    # Generate HOTP using the counter
    return htop_vanilla.hotp(key, counter, digits)


# Example usage
if __name__ == "__main__":
    test_key = b'12345678901234567890'  # Secret key (must be kept secure)
    totp = totp(test_key)
    print(f"TOTP: {totp}")
