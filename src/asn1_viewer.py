from os import listdir
from os.path import abspath, splitext, basename
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

appName = appConfig['BASIC'].get('appName', 'asn1_parser')
appName = '%s_viewer' % appName

# Initiate main log.
l = asn1.log (
  appName,
  logDate = launchTimestamp,
  **appConfig['LOG']
)
l.write('ASN1 Viewer started successfully')

# Initiate basic variables.
inputFolder = abspath(appConfig['BASIC']['inputFolder'])
l.write('Import folder: %s' % inputFolder)
viewsFolder = abspath(appConfig['BASIC']['viewsFolder'])
l.write('Views folder: %s' % viewsFolder)

def main():
  startTime = time()
  l.write('Start.')
  fileList = listdir (inputFolder)
  l.write('Found files in folder: %s. List of files below.' % str(len(fileList)))
  l.write('\n'.join(fileList), record = '{message}\n')

  for input in fileList:
    l.write('Begin to process file %s' % input)
    inputPath = abspath('%s/%s' % (inputFolder, input))
    outputPath = abspath('%s/%s.json' % (viewsFolder, splitext(input)[0]))
    with open(inputPath, 'rb') as input_file:
      bits = asn1.bits(input_file.read())
    bits.parse()
    bits.view(output = outputPath)

  endTime = time()
  l.write('Finish. Execution time %s' % str(endTime-startTime))
  pass

if __name__ == "__main__":
  main()
