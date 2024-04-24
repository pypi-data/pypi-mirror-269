import os

from cryptography.fernet import Fernet

from daves_utilities.credentials import credentials

key: str = os.getenv("DAVID_SECRET")
fernet = Fernet(key)


def generate_key() -> bytes:
    return Fernet.generate_key()


def encrypt_message(message: str) -> bytes:
    return fernet.encrypt(message.encode())


def decrypt_message(enc_message: str) -> bytes:
    return fernet.decrypt(enc_message).decode()


def get_credentials(credential_name: str) -> dict[str, str]:
    crd = credentials[credential_name]
    return {"usr": crd["usr"], "pwd": decrypt_message(crd["pwd"])}


if __name__ == "__main__":
    message = "J28i93Grx!KQ7t4$AD*C"
    print(f"{message=}")

    enc_message = encrypt_message(message)
    print(f"{enc_message=}")

    dec_message = decrypt_message(enc_message)
    print(f"{dec_message=}")
