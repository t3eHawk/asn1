from os import listdir
from os.path import abspath, splitext
from sys import argv, exit
from configparser import ConfigParser
from time import time, localtime, strftime
import asn1

# Initiate configuration file from executable parameters.
# If parameter was missed exit from execution and give warning.
try:
  appConfig = ConfigParser()
  appConfig.optionxform = str
  appConfig.read(argv[1])
except IndexError:
  exit (
"""Unable to start the programm.
No configuration file was found.
You need to point configuration  file path as first executable parameter.
For correct execution configuration file must include next few sections with options:

[BASIC]
inputFolder - folder with encoded ASN.1 files.
outputFolder - folder for decoded ASN.1 files.
viewsFolder - folder for views of encoded ASN.1 files.
inputStructFile - file where structure of input file definied.
outputStructFile - file where structure of output file fields definied.
fileHistoryFolder - folder for file history log.
appName - name of current stream.

[LOG]
logPath - folder for main log."""
  )

launchTimestamp = strftime('%Y%m%d%H%M%S', localtime())

appName = appConfig['BASIC'].get('appName', 'asn1')
appName = '%s_parser' % appName

# Initiate main log.
l = asn1.log (
  appName,
  logDate = launchTimestamp,
  **appConfig['LOG']
)
l.write('ASN1 Parser started successfully')

# Initiate basic variables.
inputFolder = abspath(appConfig['BASIC']['inputFolder'])
l.write('Import folder: %s' % inputFolder)
outputFolder = abspath(appConfig['BASIC']['outputFolder'])
l.write('Export folder: %s' % outputFolder)
fileHistoryFolder = abspath(appConfig['BASIC']['fileHistoryFolder'])
l.write('File history folder: %s' % fileHistoryFolder)
inputStructFile = abspath(appConfig['BASIC']['inputStructFile'])
l.write('Structure for input data definied from %s' % inputStructFile)
outputStructFile = abspath(appConfig['BASIC']['outputStructFile'])
l.write('Structure for output data definied from %s' % outputStructFile)
sep = appConfig['BASIC'].get('separator', ';')
l.write('Column separator: %s' % sep)

# Format of row in output file.
outputRow = '{fileName}{sep}{recNo}{sep}{values}\n'

# Initiate log with file history.
fh = asn1.log (
  appName,
  logDate = launchTimestamp,
  logName = '{appName}_{logDate}',
  logPath = fileHistoryFolder
)
# Format of row in log with file history.
fh.record = '{currentTimestamp}{sep}{fileNo}{sep}{fileName}{sep}{fileSize}{sep}{recQuantity}{sep}{status}\n'

fileInfoForm = {
  'fileNo': None,
  'fileName': None,
  'fileSize': None,
  'recQuantity': None,
  'status': None
}

def main ():
  startTime = time()
  l.write('Start parsing.')

  fileList = listdir (inputFolder)
  l.write('Found files in folder: %s. List of files below.' % str(len(fileList)))
  l.write('\n'.join(fileList), record = '{message}\n')

  fileNo = 1
  for fileName in fileList:
    l.write('Begin to process file %s' % fileName)
    # Copy dict from pattern to use for file on this current iteration.
    fileInfo = fileInfoForm.copy()
    fileInfo['fileNo'] = fileNo
    fileInfo['fileName'] = fileName

    # Full path for input file on this iteration.
    inputPath = abspath('%s/%s' % (inputFolder, fileName))
    # Full path for output file on this iteration.
    # Name of output equal to name of input but with txt extension.
    outputPath = abspath('%s/%s.txt' % (outputFolder, splitext(fileName)[0]))

    # Initiate default status variable that would not be changed during
    # processing if all stages finished without issues.
    status = 'OK'

    # Open input file in binary mode and make all necessary actions with data.
    with open(inputPath, "rb") as f:
      b = asn1.bits (
        f.read(),
        inputStructFile = inputStructFile,
        outputStructFile = outputStructFile
      )
      fileInfo['fileSize'] = len(b.dataBytes)

      try:
        l.write('Parse bytes to blocks...')
        b.parse()
      except BaseException:
        l.error()
        status = 'FAIL'
      else:
        blockQuantity = len(b.dataBlocks)
        l.write('Blocks found: %s' % blockQuantity)
        l.ok()

      try:
        l.write('Recognize blocks...')
        b.recognize()
      except BaseException:
        l.error()
        status = 'FAIL'
      else:
        l.ok()

      try:
        l.write('Decode data in blocks...')
        b.decode()
      except BaseException:
        l.error()
        status = 'FAIL'
      else:
        l.ok()

      try:
        l.write('Convert blocks to records...')
        r = b.convert()
      except BaseException:
        l.error()
        status = 'FAIL'
      else:
        fileInfo['recQuantity'] = len(r.dataRecords)
        l.write('Records found: %s' % fileInfo['recQuantity'])
        l.ok()

      try:
        l.write('Export records to %s...' % outputPath)
        r.export(
          outputPath,
          rowForm = outputRow,
          sep = sep,
          fileName = fileName
        )
      except BaseException:
        l.error()
        status = 'FAIL'
      else:
        l.ok()

      try:
        l.write('Write info to file history...')
        fileInfo['status'] = status
        fh.write(None, sep = sep,  **fileInfo)
      except BaseException:
        l.error()
      else:
        l.ok()

    fileNo += 1
    pass

  endTime = time()
  l.write('Finish parsing. Execution time %s' % str(endTime-startTime))

if __name__ == "__main__":
  main()
