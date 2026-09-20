from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import jwt
from pwdlib import PasswordHash

from typing import Annotated
from datetime import datetime, timedelta, timezone


