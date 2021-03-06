# googleOTP-to-andOTP
Export googleOTP app to anOTP

## This is a basic python3 script used to export a json file from a QR code generated from Google Authenticator App
### Pre-requirements
* Protoc must be installed (https://developers.google.com/protocol-buffers/docs/pythontutorial#compiling-your-protocol-buffers)
* Python3

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
2. Go to export account on Google App Authenticator
3. Scan the QRCode, for example using: https://qrcodescan.in/ (Tip, it is hard get it right when you have too many entries. The QRCodes the app generates are hard the read with Webcam. You can export it is smaller batches 5-8 entries at time or Use another phone that have focus adjustment)
4. copy the scanned string `(otpauth-migration://offline?data=CiEKEUpSkaZJ...)` to a file (`input.txt` for example)
   - if you have too many accounts, more than 1 QRCode will be generated, put the string scanned in each line of the file.
5. save the `input.txt` file
6. run `rm GAuthPayload_pb2.py && protoc --python_out=. GAuthPayload.proto`
7. run the script `python3 toAndOTP.py <input file> <output file>.json`
   - example `$ python3 toAndOTP.py ~/input.txt ~/exported.json`
   
Also https://github.com/jay-aye-see-kay suggested the steps below in case the above fails:
 - set up a virtual env
 
`python 3 -m venv venv`

`source venv/bin/activate`

 - install python protobuf package (you need an OS install of protobuf too, as mentioned in the pre-requirements)
 
`pip install protobuf`

`python toAndOTP.py <input file> <output file>.json`

8. now transfer the exported file to your phone and restore backup (plain text).**IMPORTANT** Make a BACKUP of your andOTP accounts before importing the exported file
