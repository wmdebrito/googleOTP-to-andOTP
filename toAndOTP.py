#! /usr/bin/python3

from GAuthPayload_pb2 import GAuthPayload
import sys
import urllib.parse
import base64
from pprint import pprint
import json

def decode(b64Payload):
    payload = urllib.parse.unquote(b64Payload)
    payload = payload.replace('otpauth-migration://offline?data=','')
    payload = base64.b64decode(payload)

    gAuthPayload = GAuthPayload()
    gAuthPayload.ParseFromString(payload)

    return exportToAndOTP(gAuthPayload)

def exportToAndOTP(gAuthPayload):
    andOtpValues = []
    for entry in gAuthPayload.payload:
        andOtpItem = {
               "algorithm": "SHA1" if (entry.algorithm == 1) else "ERROR", #Google supports on SHA1
               "digits": "6" if (entry.digits == 1)  else str(entry.digits), #only supports 6
               "type": "TOTP" if (entry.type == 2)  else "HOTP",
               "secret": base64.b32encode(entry.secret).decode("utf8").replace("=",""),
               "label": entry.name,
               "issuer": entry.issuer,
               "thumbnail": entry.issuer
            }

        if entry.counter:
            andOtpItem["counter"] = entry.counter

        andOtpValues.append(andOtpItem)

    return andOtpValues

inputFile = "input.txt" if (len(sys.argv) < 2) else sys.argv[1]
with open(inputFile, "r") as inputValues:
    print("Reading file:"+ inputFile)
    fullResult = []
    for line in inputValues:
         fullResult = fullResult + decode(line)
    fileExported = "exported.json" if (len(sys.argv) < 3) else sys.argv[2]
    json.dump(fullResult, open(fileExported, "w"))
    print("Exported file:"+ fileExported)
