from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

import hashlib
import hmac
import base64
import logging

class AuthMiddleware(BaseHTTPMiddleware):
    secret_key: str

    def __init__(self, app, secret_key: str):
        super().__init__(app)
        self.secret_key = secret_key

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        logging.info("auth_header: %s", auth_header)

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[len("Bearer "):]
            logging.info("token: %s", token)

            try:
                decoded = base64.urlsafe_b64decode(token).decode()
                telegram_id, signature = decoded.split('.')
                expected_signature = hmac.new(self.secret_key.encode(), telegram_id.encode(), hashlib.sha256).hexdigest()

                if hmac.compare_digest(signature, expected_signature):
                    request.state.telegram_id = telegram_id
                else:
                    return JSONResponse(
                        status_code=401, content={"error": "Invalid telegram_id"}
                    )
            except:
                return JSONResponse(
                    status_code=401, content={"error": "Invalid token"}
                )
        else:
            return JSONResponse(
                status_code=401, content={"error": "Authorization header missing or invalid"}
            )

        response = await call_next(request)
        return response