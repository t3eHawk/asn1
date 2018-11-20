# Here is a class "strings" that contains all available functionality to work
# with decoded ASN.1 data.
# Class's constructor requires only variable "dataRecords" - list of
# dictionaries with records in them.

class strings():
  def __init__ (self, dataRecords):
    self.dataRecords = dataRecords
    pass

  # Export of passed "dataRecords" to "filePath".
  # Variable "sep" is a field separator in export file.
  # Variable "rowForm" is a format of row in export file where values is a
  # necessary variable with record's fields.
  def recordsExport (
    self,
    dataRecords,
    filePath,
    sep = ';',
    rowForm = '{recNo};{values}\n',
    *args,
    **kwargs
  ):
    with open(filePath, 'w+') as f:
      recNo = 1
      for record in dataRecords:
        values = sep.join(record.values())
        row = rowForm.format(**vars(), **kwargs)
        f.write(row)
        recNo += 1
    pass

  # Export object's dataRecords to file.
  def export (self, *args, **kwargs):
    self.recordsExport(self.dataRecords, *args, **kwargs)
    pass
