import os, secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
security = HTTPBasic()
WRITE_USER = os.getenv("WRITE_USER", "admin")
WRITE_PASS = os.getenv("WRITE_PASS", "changeme")
def require_write(credentials: HTTPBasicCredentials = Depends(security)):
    ok_user = secrets.compare_digest(credentials.username, WRITE_USER)
    ok_pass = secrets.compare_digest(credentials.password, WRITE_PASS)
    if not (ok_user and ok_pass):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password for write operation",
                            headers={"WWW-Authenticate": "Basic"})
    return True
