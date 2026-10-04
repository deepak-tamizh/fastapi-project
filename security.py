from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in .env")

if not ALGORITHM:
    raise RuntimeError("ALGORITHM is not set in .env")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")
)


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# It takes the user_id as input and returns the JWT token as a string.

# It takes the current UTC time and adds the value of ACCESS_TOKEN_EXPIRE_MINUTES to it. The resulting time becomes
# the token’s expiration time. For example, if the current time is 10:00 and ACCESS_TOKEN_EXPIRE_MINUTES = 30,
# the token will expire at 10:30.

# It creates a payload dictionary containing the information that needs to be stored inside the JWT. The "sub" field
# identifies which user the token belongs to, using the user_id. The "type": "access" field indicates that the token
# is an access token, while "exp" specifies the time when the token will expire.

# It encodes this payload into a JWT token using the SECRET_KEY and the specified ALGORITHM, and returns it.


def create_refresh_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

