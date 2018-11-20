# Here are functions for convert data from ASN.1 bytes to strings.

def INTEGER (encoded):
  encoded = encoded.hex()
  decoded = int(encoded, 16)
  return str(decoded)

def IA5STR (encoded):
  decoded = encoded.decode('ascii')
  return str(decoded)

def OCTETSTR (encoded):
  decoded = encoded.hex().upper()
  return str(decoded)

def TBCDSTR (encoded):
  encoded = encoded.hex()
  first = 0
  last = 1
  decoded = str()
  while last < len(encoded):
    decoded = decoded+encoded[last:last+1]
    decoded = decoded+encoded[first:last]
    first += 2
    last += 2
  decoded = decoded.replace('f', '')
  return str(decoded)

def BOOLEAN (encoded):
  if encoded == b'\xff':
    decoded = 1
  elif encoded == b'\x00':
    decoded = 0
  return str(decoded)

def TIMESTAMP (encoded):
  YY = bytes([encoded[0]]).hex()
  MM = bytes([encoded[1]]).hex()
  DD = bytes([encoded[2]]).hex()
  hh = bytes([encoded[3]]).hex()
  mm = bytes([encoded[4]]).hex()
  ss = bytes([encoded[5]]).hex()
  S = bytes([encoded[6]]).decode("ascii")
  h = bytes([encoded[7]]).hex()
  m = bytes([encoded[8]]).hex()
  decoded = "20"+YY+"-"+MM+"-"+DD+" "+hh+":"+mm+":"+ss+S+h+m
  return str(decoded)

def ADDRSTR (encoded):
  byte1 = int.from_bytes(encoded[0:1], byteorder='little')
  TonNpi = byte1 & 127
  numDigits = TBCDSTR(encoded[1:])
  decoded = str(TonNpi)+"."+numDigits
  return str(decoded)

def BCDDIRNUM (encoded):
  byte1 = int.from_bytes(encoded[0:1], byteorder='little')
  if (byte1 & 128) == 128:
    TonNpi = byte1 & 127
    PresentScreen = 0
    numDigits = TBCDSTR(encoded[1:])
    decoded = str(TonNpi)+"."+str(PresentScreen)+"."+numDigits
  else:
    byte2 = int.from_bytes(encoded[1:2], byteorder='little')
    TonNpi = byte1 & 127
    PresentScreen = byte2 & 127
    numDigits = TBCDSTR(encoded[2:])
    decoded = str(TonNpi)+"."+str(PresentScreen)+"."+numDigits
  return decoded

def IPV4STR (encoded):
  b1 = str(encoded[0])
  b2 = str(encoded[1])
  b3 = str(encoded[2])
  b4 = str(encoded[3])
  decoded = b1+'.'+b2+'.'+b3+'.'+b4
  return decoded

def NULL (encoded):
  return str()
