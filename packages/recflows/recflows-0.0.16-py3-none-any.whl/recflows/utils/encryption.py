from cryptography.fernet import Fernet
from recflows.vars import ENCRYPTION_KEY

encrypt_key = Fernet(ENCRYPTION_KEY)


def get_variable_record(record):
    record["value"] = encrypt_key.decrypt(record["value"])
    return record


def encrypt_variable_record(record):
    record["value"] = encrypt_key.encrypt(record["value"].encode())
    return record
