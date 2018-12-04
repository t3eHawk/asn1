from time import strftime, localtime
from traceback import extract_tb
from sys import exc_info, exit
from os import makedirs
from os.path import exists

class log():
  def __init__(
    self,
    appName,
    logPath = 'logs',
    logExt = 'log',
    logName = '{appName}_{logDate}',
    logDate = '%Y%m%d%H%M%S',
    console = False,
    greetings = True,
    control = True,
    *args,
    **kwargs
  ):
    self.appName = appName
    self.console = console
    self.control = control

    if console == False:
      logDate = strftime(logDate, localtime())
      logPath = logPath.format(**vars(), **kwargs)
      if not exists(logPath):
        makedirs(logPath)
      logName = logName.format(**vars(), **kwargs)
      self.logFile = '%s/%s.%s' % (logPath, logName, logExt)
    elif greetings == True:
      header = ' %s ' % appName
      side = int((80-len(header))/2)*'#'
      print ('%s %s %s' %(side, header, side))

    # All other default variables.
    self.timeFormat = '%Y-%m-%d %H:%M:%S'
    self.record = '[{currentTimestamp}][{recType}][{message}]\n'
    self.messageOK = 'SUCCESS'
    self.errMessage = 'Failed with {errName} - {errValue} - during execution {errLineNo} in {errFilename}'
    self.errLevels = {0: 'WARNING', 1: 'ERROR', 2: 'CRITICAL'}
    pass

  # Log text stored in "message" attribute.
  def write(
    self,
    message,
    recType = 'INFO',
    record = None,
    *args,
    **kwargs
  ):
    if not record:
      record = self.record
    currentTimestamp = strftime(self.timeFormat, localtime())
    record = record.format(**vars(), **kwargs)
    if self.console == False:
      with open(self.logFile, "a+") as f:
        f.write(record)
    else:
      print(record, end='')
    pass

  # Log positive message in format stored in default variable "okFormat".
  def ok(self, messageOK = None, *args, **kwargs):
    if not messageOK:
      messageOK = self.messageOK
    message = self.messageOK.format(**vars(), **kwargs)
    self.write(message, **kwargs)
    pass

  # Log debug message.
  def debug(self, *args, **kwargs):
    self.write(recType = 'DEBUG', *args, **kwargs)
    pass

  # Parse error and log it in format stored in default variable "errFormat".
  # Control program execution in case of critical error.
  def error(
    self,
    errMessage = None,
    errLevel = 1,
    errLevels = None,
    *args,
    **kwargs
  ):
    if not errLevels:
      errLevels = self.errLevels
    recType = errLevels.get(errLevel)
    if not errMessage:
      errMessage = self.errMessage
      if exc_info() != (None, None, None):
        errType, errValue, errTb = exc_info()
        tb = str(extract_tb(errTb))
        errName = errType.__name__
        errFilename = tb[tb.find('file'):tb.find('line')-2:]
        errLineNo = tb[tb.find('line'):tb.find(' in '):]
        errMessage = errMessage.format(**vars(), **kwargs)
      else:
        errMessage = 'No errors to report'
    self.write(errMessage, recType=recType, *args, **kwargs)
    # Critical error must lead to execution break when control mode enabled.
    if self.control == True:
      if errLevel == 2:
        exit('Critical error caused exit from execution.')
    pass

  # Shorthand for error(errLevel = 0)
  def warning(self, *args, **kwargs):
    self.error (errLevel = 0, *args, **kwargs)
    pass

  # Shorthand for error(errLevel = 2)
  def critical(self, *args, **kwargs):
    self.error (errLevel = 2, *args, **kwargs)
    pass
