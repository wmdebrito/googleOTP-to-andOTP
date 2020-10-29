# googleOTP-to-andOTP
Export googleOTP app to anOTP

## This is a basic python3 script used to export a json file from a QR code generated from Google Authenticator App
### Pre-requirements
* Protoc must be installed (https://developers.google.com/protocol-buffers/docs/pythontutorial#compiling-your-protocol-buffers)
* Python 3

## Protobuf/protoc parser
### Below and example of parsing base64 to protobuf format, used to reverse engineering (input.txt with 1 base64 entry URLdecoded)
```
$ base64 -D input.txt |protoc --decode_raw
1 {
  1: "JR\221\246I\222d\231&I$\223d\2212I\010"
  2: "Test"
  4: 1
  5: 1
  6: 1
  7: 0
}
1 {
  1: "\322/]\304\202V\313\035\252*\006^\233h\364\273`u-\005\204k\371\212Pg\247\376\366\025~\223\315\303\250"
  2: "Amazon:765595469557"
  4: 1
  5: 1
  6: 2
}
2: 1
3: 1
4: 0
5: 1468242669
```

### How to
1. `git clone https://github.com/wmdebrito/googleOTP-to-andOTP.git`
2. Setup a virtualenv:

   1. `python3 -m virtualenv venv`
   2. `source venv/bin/activate`
   3. Install requirements: `pip install -r requirements.txt`
3. Go to export account on Google App Authenticator
4. Scan the QRCode, for example using: https://qrcodescan.in/ (Tip: it is hard to get it right when you have too many entries. The QRCodes the app generates are hard to read with a webcam. You can export it in smaller batches 5-8 entries at a time or use another phone that has focus adjustment)
5. Copy the scanned string `(otpauth-migration://offline?data=CiEKEUpSkaZJ...)` to a file (`input.txt` for example)
   - if you have too many accounts, more than 1 QRCode will be generated, put the string scanned in each line of the file.
6. Save the `input.txt` file
7. Run `rm GAuthPayload_pb2.py && protoc --python_out=. GAuthPayload.proto`
8. Run the script `python3 toAndOTP.py <input file> <output file>.bin`
   - Example: `$ python3 toAndOTP.py ~/input.txt ~/exported.bin`

   The script will prompt for a password that is used to encrypt the exported data.
   The given password will be used in andOTP to decrypt the exported data.

8. Now transfer the exported file to your phone and restore backup (encrypted).

   **IMPORTANT**: Make a BACKUP of your andOTP accounts before importing the exported file
