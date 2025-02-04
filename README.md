# Multifactor Authentication

## Time Based One Time Password

I started using an authenticator app to do my Multi-Factor logins. It worked great, but I had no idea how. So I decided to try and duplicate the functionality for myself in Python. Using a library it was 5 lines of Python.
```python
import pyotp

secret = 'SUPERSECRETPA55WORDYOUCANTGUESS5'
totp = pyotp.TOTP(secret)
otp = totp.now()
print("Current OTP:", otp)
```
While this approach was effective, it didn't provide me with a deep understanding of the underlying mechanics. So, I challenged myself to implement TOTP without relying on external libraries. The only exception was the time module, which I used to avoid manually entering the current date and time repeatedly. Beyond that, the implementation is pure, vanilla Python.


To begin, I referred to the RFC 6238 specification, which outlines the TOTP algorithm. Here's a high-level overview of how it works:

1. Secret Key: Both the server and the client share a secret key.

2. Time-Based Counter: The algorithm calculates the number of 30-second intervals (or "time steps") that have elapsed since the Unix epoch (00:00:00 UTC on January 1, 1970).

3. HOTP Calculation: The TOTP value is derived by applying the HMAC-Based One-Time Password (HOTP) algorithm to the combination of the secret key and the time-based counter.

4. Truncation: The resulting HMAC value is truncated to a fixed number of digits (typically 6).

The HOTP algorithm itself relies on HMAC (Hash-based Message Authentication Code), which is commonly used for verifying data integrity. In this case, HMAC uses SHA-1 (Secure Hash Algorithm 1) as its underlying hashing function. SHA-1, despite its age, remains the core of TOTP's functionality.


To better understand the process, I visualized the layers of the TOTP algorithm as follows:
```
┌──────────────────┐
│    TOTP          │
│┌────────────────┐│
││   HOTP         ││
││┌──────────────┐││
│││  HMAC        │││
│││┌────────────┐│││
││││ SHA-1      ││││
│││└────────────┘│││
││└──────────────┘││
│└────────────────┘│
└──────────────────┘
```
I started by implementing the innermost layer (SHA-1) and worked my way outward, adding each subsequent layer as a separate module. This modular approach allowed me to build and test each component independently. I tried to leave notes for future me, I am sure he will let me know if they are helpful.
