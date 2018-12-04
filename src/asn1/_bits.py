# Here is a class "bits" that contains all available functionality
# to work with data encoded in ASN.1 format.
# Class's constructor requires only variable "dataBytes" - data encoded
# in ASN.1 binary format.
# Also there is an option to pass python list with objects of
# blockPrimitive or blockComplex class as dataBlocks argument.
# Argument inputStructFile must contain input data structure definition
# (ID - data type - Name) and must be passed to recognize and decode data in
# blocks.
# Argument outputStructFile must contain list of blocks that are going to be
# converted to list of records as dictionaries.

from .decodings import *
from .rules import *
from ._strings import strings
from ._table import table
import json

class bits():
  def __init__ (
    self,
    dataBytes,
    dataBlocks = None,
    inputStructFile = None,
    outputStructFile = None,
    *args,
    **kwargs
  ):
    self.dataBytes = dataBytes
    self.dataBlocks = dataBlocks
    # Parse file defining blocks to dictionary where ID is a key
    # and data type and name are in list as value.
    if inputStructFile != None:
      tb = table(open(inputStructFile, "r").readlines())
      inputStructure = dict()
      i = 0
      for i in range(tb.rowsNum):
        ID = tb.fields[0][i]
        Type = tb.fields[1][i]
        Name = tb.fields[2][i]
        inputStructure.update({ID: [Type, Name]})
        i += 1
      self.inputStructure = inputStructure
    if outputStructFile != None:
      # Parse file defining ordered list of blocks that must be converted to
      # dictionary where key is a name of block and value is a data of block.
      with open(outputStructFile, "r") as f:
        s = f.read().splitlines()
        outputStructure = dict.fromkeys(s, '')
      self.outputStructure = outputStructure
    pass

  # Class of blocks with single value in data.
  class blockPrimitive ():
    def __init__ (self, tag, ID, length, data):
      self.tag = tag
      self.ID = ID
      self.length = length
      self.data = data
      pass

  # Class of blocks with nested structures in data.
  class blockComplex ():
    def __init__ (self, tag, ID, length, data):
      self.tag = tag
      self.ID = ID
      self.length = length
      self.data = data
      pass

  # Parse passed bytes to blocks according to one of the encoding rules
  # (BER, DER, CER).
  # Target is to analyze each byte and to separate tag, length and data
  # of one block from other bytes until bytes are not ended.
  # If block if defined it must be initiated as class - primitive or complex.
  # If block is complex its data processed by recursion function call.
  # Each class requieres tag, ID (unique absolute tag value containing all
  # parents and child tags), data length and data.
  # All found blocks are added to list on appropriate level of block read.
  # Variable "pos" is pointer on byte that is read by this moment.
  # If block is finally analized function must analyze next bytes, i.e. bytes
  # starting after pointer in value of total previous block length.
  # Function returns list of found blocks.
  def bytesParse (self,  Bytes, ID = str()):
    pos = 0
    blocks = list()
    while pos < len(Bytes):
      tag, length, data, lenBlock = BER (Bytes, pos)
      blID = ID+tag.hex()
      if (tag[0] & 32) == 32:
        blData = self.bytesParse(data, ID = blID)
        block = self.blockComplex (tag, blID, length, blData)
      else:
        block = self.blockPrimitive (tag, blID, length, data)
      blocks.append(block)
      pos = lenBlock
    return blocks

  # Parse object's "dataBytes" to blocks.
  def parse (self):
    self.dataBlocks = self.bytesParse(self.dataBytes)
    pass

  # Get asn.1 structure of blocks.
  def view(self, blocks = None, output = None):
    blocks = blocks or self.dataBlocks
    viewer = dict()
    for block in blocks:
      tag = block.tag.hex()
      if type(block).__name__ == 'blockPrimitive':
        try:
          value = block.data.decode()
        except UnicodeDecodeError:
          value = block.data.hex()
      else:
        value = self.view(block.data)

      if tag in viewer and viewer[tag] is not None:
        if isinstance(viewer[tag], list) is False:
          viewer[tag] = [viewer[tag]]
        viewer[tag].append(value)
      else:
        viewer[tag] = value
    if output is not None:
      with open(output, 'w') as output_file:
        json.dump(viewer, output_file, indent = True)
    return viewer

  # If passed blocks structure placed in inputStructure they can be recognized,
  # i.e. their names and data types can be defined using the ID.
  # If block is complex its data processed by recursion function call.
  def blocksRecognize (self, blocks):
    for block in blocks:
      block.dataType = self.inputStructure[block.ID][0]
      block.name = self.inputStructure[block.ID][1]
      if type(block).__name__ == 'blockComplex':
        self.blocksRecognize(block.data)
    pass

  # Recognized object's "dataBlocks".
  def recognize (self):
    self.blocksRecognize (self.dataBlocks)
    pass

  # Decode passed blocks data according to their data type.
  # If block is complex its data processed by recursion function call.
  def blocksDecode (self, blocks):
    for block in blocks:
      if type(block).__name__ == 'blockPrimitive':
        if block.dataType == 'INTEGER':
          block.data = INTEGER(block.data)
        elif block.dataType == 'IA5STR':
          block.data = IA5STR(block.data)
        elif block.dataType == 'OCTETSTR':
          block.data = OCTETSTR(block.data)
        elif block.dataType == 'TBCDSTR':
          block.data = TBCDSTR(block.data)
        elif block.dataType == 'BOOLEAN':
          block.data = BOOLEAN(block.data)
        elif block.dataType == 'TIMESTAMP':
          block.data = TIMESTAMP(block.data)
        elif block.dataType == 'ADDRSTR':
          block.data = ADDRSTR(block.data)
        elif block.dataType == 'BCDDIRNUM':
          block.data = BCDDIRNUM(block.data)
        elif block.dataType == 'IPV4STR':
          block.data = IPV4STR(block.data)
        else:
          block.data = block.data.hex()
      elif type(block).__name__ == 'blockComplex':
        self.blocksDecode(block.data)
    pass

  # Decode object's "dataBlocks".
  def decode (self):
    self.blocksDecode(self.dataBlocks)
    pass

  # Convert passed blocks to list of records.
  # Every record in the list is a dictionary of {field name: field value}.
  # Record structure is copied from outputStructure variable.
  # New record begins when function meets data type 'RECORD'.
  # Function returns only list of records.
  def blocksConvert (self, blocks, records = list()):
    for block in blocks:
      if block.dataType == 'RECORD':
        records.append(dict(self.outputStructure))
        records[-1]['recordTag'] = block.tag.hex()
      if type(block).__name__ == 'blockPrimitive':
        if records[-1][block.name] == '':
          records[-1][block.name] = block.data
        else:
          records[-1][block.name] = records[-1][block.name]+'::'+block.data
      elif type(block).__name__ == 'blockComplex':
        self.blocksConvert (block.data, records = records)
    return records

  # Convert object's "dataBlocks" to records. Function returns class "strings"
  # object with converted records in it.
  def convert (self):
    records = strings(self.blocksConvert(self.dataBlocks, records = list()))
    return records
