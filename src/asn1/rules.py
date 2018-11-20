# Here are functions for define ASN.1 block according to its encoding rule.

def BER (data, pos = 0):
  tagBytes = bytearray()
  tagLimit = 31
  if (data[pos] & tagLimit) == tagLimit:
    tagBytes.append(data[pos])
    while True:
      pos += 1
      tagBytes.append(data[pos])
      tagExit = 128
      if (data[pos] & tagExit) == tagExit:
        continue
      else:
        break
  else:
      tagBytes.append(data[pos])
  pos += 1
  lenBytes = bytearray()
  ln_limit = 128
  if (data[pos] & ln_limit) == ln_limit:
    ln_len = (data[pos] ^ ln_limit)
    pos += 1
    while ln_len != 0:
      lenBytes.append(data[pos])
      pos += 1
      ln_len -= 1
  else:
    lenBytes.append(data[pos])
    pos += 1
  tag = tagBytes
  lenData = int(lenBytes.hex(), 16)
  lenBlock = pos + lenData
  data = (data[pos:lenBlock])
  return (tag, lenData, data, lenBlock)
