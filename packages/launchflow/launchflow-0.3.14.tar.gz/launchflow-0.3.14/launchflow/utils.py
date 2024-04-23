import secrets
import string
from typing import Union

import httpx
from requests import Response


# TODO: Move "potential fix" messsages into the server.
# Server should return a json payload with a message per client type, i.e.
# {status: 409, message: "Conflict...", fix: {"cli": "Run this command..."}}
# Use details to return the fix payload:
# details = {message: "...", fix: {"cli": "Run this command..."}}
def get_failure_text(response: Union[httpx.Response, Response]) -> str:
    status_code = response.status_code
    try:
        json_response = response.json()
        return f"({status_code}): {json_response['detail']}"
    except Exception:
        if isinstance(response, Response):
            return f"({status_code}): {response.reason}"
        return f"({status_code}): {response.reason_phrase}"


def generate_random_password(
    length: int = 12, include_special_chars: bool = False
) -> str:
    """
    Generates a random password using the secrets module.
    ref: https://www.educative.io/answers/what-is-the-secretschoice-function-in-python

    **Arguments**:
    - `length` (int): The length of the password to generate.
    - `include_special_chars` (bool): Whether to include special characters in the password.

    **Returns**:
    - A random password string.
    """
    characters = string.ascii_letters + string.digits
    if include_special_chars:
        characters += string.punctuation

    password = "".join(secrets.choice(characters) for _ in range(length))
    return password
