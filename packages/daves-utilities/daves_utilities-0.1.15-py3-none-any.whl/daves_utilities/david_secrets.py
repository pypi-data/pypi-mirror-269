import os

from cryptography.fernet import Fernet
from typeguard import typechecked

from daves_utilities.credentials import credentials

@typechecked
def get_david_secret() -> str:
    key = os.getenv("DAVID_SECRET")
    if key is None:
        raise ValueError("Environment variable DAVID_SECRET is not set")
    return key

@typechecked
def create_fernet_key() -> Fernet:
    key = get_david_secret()
    return Fernet(key)

@typechecked
def generate_key() -> bytes:
    return Fernet.generate_key()

@typechecked
def encrypt_message(message: str) -> bytes:
    fernet = create_fernet_key()
    return fernet.encrypt(message.encode())

@typechecked
def decrypt_message(enc_message: bytes) -> str:
    fernet = create_fernet_key()
    return fernet.decrypt(enc_message).decode()

@typechecked
def get_credentials(credential_name: str) -> dict[str, str]:
    crd = credentials[credential_name]
    return {"usr": crd["usr"], "pwd": decrypt_message(crd["pwd"])}


if __name__ == "__main__":
    message = "<pwd>"
    print(f"{message=}")

    enc_message = encrypt_message(message)
    print(f"{enc_message=}")

    dec_message = decrypt_message(enc_message)
    print(f"{dec_message=}")
