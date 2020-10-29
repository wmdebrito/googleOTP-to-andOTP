#! /usr/bin/python3

from GAuthPayload_pb2 import GAuthPayload
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sys
import secrets
import getpass
import urllib.parse
import base64
from pprint import pprint
import json


def decode(b64Payload):
    payload = urllib.parse.unquote(b64Payload)
    payload = payload.replace('otpauth-migration://offline?data=', '')
    payload = base64.b64decode(payload)

    gAuthPayload = GAuthPayload()
    gAuthPayload.ParseFromString(payload)

    return exportToAndOTP(gAuthPayload)


def exportToAndOTP(gAuthPayload):
    andOtpValues = []
    for entry in gAuthPayload.payload:
        andOtpItem = {
            # Google supports on SHA1
            "algorithm": "SHA1" if (entry.algorithm == 1) else "ERROR",
            # only supports 6
            "digits": "6" if (entry.digits == 1) else str(entry.digits),
            "type": "TOTP" if (entry.type == 2) else "HOTP",
            "secret": base64.b32encode(entry.secret).decode("utf8").replace("=", ""),
            "label": entry.name,
            "issuer": entry.issuer,
            "thumbnail": entry.issuer
        }

        if entry.counter:
            andOtpItem["counter"] = entry.counter

        andOtpValues.append(andOtpItem)

    return andOtpValues


def encrypt(andOptData, password):
    # Encrypt the created andOTP-formatted data
    # Specs: https://github.com/andOTP/andOTP/wiki/Backup-encryption

    # Create JSON from the data
    json_bytes = json.dumps(andOptData).encode("utf-8")

    # Random 12-byte (96 bit) IV (nonce)
    nonce = secrets.token_bytes(12)

    # 256 bit key
    # PBKDF2 with HMAC-SHA1
    # Random iterations, random 12 byte salt
    # As of 2020-10-29 andOTP uses 140000-160000 iterations, so do we
    iterations = 140000 + secrets.randbelow(20001)
    salt = secrets.token_bytes(12)

    # Derive the key used to encrypt the JSON data
    kdf = PBKDF2HMAC(algorithm=hashes.SHA1(), length=32,
                     salt=salt, iterations=iterations)
    key = kdf.derive(password.encode("utf-8"))

    # Encrypt the JSON data
    # AESGCM, no padding
    a = AESGCM(key)
    encrypted = a.encrypt(nonce, json_bytes, None)

    # Format: [PBKDF2 iterations (4 bytes, Int32)] + [PBKDF2 salt (12 bytes)] + [AES IV (12 bytes)] + [Encrypted payload]
    # Iteration int32 is big endian
    iter_bytes = iterations.to_bytes(length=4, byteorder="big")
    encrypted_data = iter_bytes + salt + nonce + encrypted

    return encrypted_data


inputFile = "input.txt" if (len(sys.argv) < 2) else sys.argv[1]
with open(inputFile, "r") as inputValues:
    print("Reading file: " + inputFile)
    fullResult = []
    for line in inputValues:
        fullResult = fullResult + decode(line)
    fileExported = "exported.bin" if (len(sys.argv) < 3) else sys.argv[2]

# Get password from the user
password = getpass.getpass("Encryption password: ")
encrypted_data = encrypt(fullResult, password)

with open(fileExported, "wb") as f:
    f.write(encrypted_data)

print("Exported file (encrypted): " + fileExported)
