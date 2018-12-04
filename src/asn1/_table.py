# Class to work with structured tables. To initiate the object you must have
# list where every element is a line of table.
# Parameter "sep" exists to define table column separator. By default it's a
# tabulation, but can be changed during object initialization.
class table():
  def __init__(self, lines, sep = '\t'):
    fields = list()
    self.rowsNum = len(lines)
    self.colsNum = lines[0].count(sep)+1
    for i in range(self.colsNum):
      fields.append([])
    for line in lines:
      column = 0
      start = 0
      end = 1
      while True:
        c = line[start:end]
        if line[end] == sep:
          fields[column].append(c)
          start = end+1
          column += 1
        elif line[end] == '\n':
          fields[column].append(c)
          start = 0
          end = 0
          column = 0
          break
        end += 1
    self.fields = fields
    pass

  # Simple call of object will return variable "fields".
  def __call__(self):
    return self.fields

  # Present fields as classic table view with borders and indents.
  def show(self, sep = '|', head = True):
    table = list()
    i = 0
    for i in range(self.rowsNum):
      table.append('%s' % sep)
    for field in self.fields:
      maxLen = 0
      for cell in field:
        if len(cell) > maxLen:
          maxLen = len(cell)
      i = 0
      for cell in field:
        spaces = (maxLen-len(cell))*' '
        newCell = '%s%s%s' % (cell, spaces, sep)
        table[i] = table[i] + newCell
        i += 1
    rowLen = len(table[0])
    horizBord = '-'*rowLen
    if head == True:
      table.insert(1, horizBord)
    table.insert(0, horizBord)
    table.insert(len(table), horizBord)
    return '\n'.join(table)
