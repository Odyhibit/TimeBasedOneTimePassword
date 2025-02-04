import pyotp

secret = 'SUPERSECRETPA55WORDYOUCANTGUESS5'
totp = pyotp.TOTP(secret)
otp = totp.now()
print("Current OTP:", otp)
