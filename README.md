#Multifactor Authentication

##Time Based One Time Password

I started using an authenticator app to do my Multi-Factor logins. It worked great, but I had no idea how. So I decided to try and duplicate the functionality for myself in Python. Using a library it was 5 lines of Python.
```python
import pyotp

secret = 'SUPERSECRETPA55WORDYOUCANTGUESS5'
totp = pyotp.TOTP(secret)
otp = totp.now()
print("Current OTP:", otp)
```
However I did not really learn how it works, so I decided to write a version using Python and **no** additional libraries. I did end up adding the time library so I would not have to keep typing in the date, and time over and over again, but aside from that convienience it is all just vanilla Python.

So I started with https://datatracker.ietf.org/doc/html/rfc6238 
The TOTP algorithm has a secret value that both parties have, then it calculates a counter, that counts how many 30 second periods have occured since the Unix epoch (00:00:00 UTC on Thursday, 1 January 1970).
So once we count how many half minutes have passed since then, we just slap that on the end of the secret and calulate the HOTP value for that.
The Hotp algorith takes a secret value, concatenates a counter to it, and then uses that Value to get an HMAC (Hash-based Message Authentication Code) this value is then truncated to a set number of decimal digits. I set the default at 6 since that's what I needed.
HMAC is an algorithm ussualy used to verify file integrity. For my purpose it uses SHA-1 for hashing.
SHA-1 (Secure Hash Algorithm 1) is hashing function that has been around for a long time, and it is used as the core of TOTP.

Like peeling back layers of onion I found out that the magic at the center was SHA-1.
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
So I started in center, and did each step in it's own module. Then as each new layer was applied it just imports the previous layer. I tried to leave notes for future me, I am sure he will let me know if they are helpful.
