# asn1

## Short Description and How-To
Main goal of this project is to create good and fast ASN.1 decoder in Python.

Currently it is in the early life.
***

### Features now
1. Pass config file as argument.
1. Decode ASN.1 structures including files using special input/output configuration files.
1. Export decoded data as a table into the file.
1. View ASN.1 structure as Python dictionary and export it to JSON file.
1. Logging of decoding process.

### Targets now
1. More and simpler configuration.
1. More interface features.
1. Optimization.
1. Make it faster.
1. Add more encoding rules (current is only BER, planned - CER, DER).
1. Add more data types supported out of the box.
1. Implement parser and viewer as parts of the module.
1. Test on more types of ASN.1 structures.
1. Reorganize the code to follow [PEP8](https://www.python.org/dev/peps/pep-0008/) standards and add module attributes.
1. Add module to PyPI.

### Requirements
**Library developed and aimed to use only in Python 3!**

**So below if we write python somewhere and you are on Linux/MacOS we meant python3 for your case.**

No additional modules required. All you need already inside.
**In future some components will be separated but not now.**

Tested in Windows 10 Version 10.0.14393 and Python 3.7.1.

### Instructions
#### Decoder
Below the description about how to decode an ASN.1 file.

Clone repository or just load *src* folder to your local.
For example to *C:/asn1*.

Go to your local src folder and execute in terminal:
```
$ cd C:/asn1/src
$ python asn1_parser.py

Unable to start the programm.
No configuration file was found.
You need to point configuration file path as first executable parameter.
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
logPath - folder for main log.
```

Create file *C:/asn1/src/config.ini* you are asked about with sections/options required.

Create folder *C:/asn1/src/structure*.
In that folder create two files: *C:/asn1/src/structure/input.txt* and *C:/asn1/src/structure/output.txt*.

Now describe the structure of ASN.1 file in *C:/asn1/src/structure/input.txt* as in the example below:
```
a0	RECORD	_
a080	OCTETSTR	recordType
a081	INTEGER	recordId
<...>
```
* Values separated with tabulations.
* Each row stands for certain block in ASN.1 file.
* First value is a block tag in hex.
* Tag must be full. So if block with tag 80 is a part of nested structure with tag a1 in record with tag a0 then block tag must be a0a180.
* Second one is a block data type for encoder:
  * INTEGER
  * IA5STR
  * OCTETSTR
  * TBCDSTR
  * BOOLEAN
  * TIMESTAMP
  * ADDRSTR
  * BCDDIRNUM
  * IPV4STR
  * NULL
* If tag is for record then point *RECORD* instead of data type.
* Third one is a name of block.
* If block has no name or no need to export that block use *_* as a name for it.

Now list block names from *C:/asn1/src/structure/input.txt* you want to see in decoded file in *C:/asn1/src/structure/output.txt*:
```
recordTag
recordType
recordId
<...>
```
* Each block name starts from new line.
* If you want to see the tag of the record then use special name - *recordTag* as block name in the list.

Create folders *C:/asn1/src/logs* and *C:/asn1/src/logs/history* + *C:/asn1/src/logs/process*.

Create folders *C:/asn1/src/import* and *C:/asn1/src/export*.

Add files you want to decode to *C:/asn1/src/import*.
For example this is a file named *ASN1_TEST_FILE.bin*

Also create folder *C:/asn1/src/views*.

Now return to *C:/asn1/src/config.ini* and fill it:
```
[BASIC]
inputFolder = C:/asn1/src/import
outputFolder = C:/asn1/src/output
viewsFolder = C:/asn1/src/views
inputStructFile = C:/asn1/structure/input.txt
outputStructFile = C:/asn1/structure/output.txt
fileHistoryFolder = C:/asn1/logs/history
appName = asn1_test

[LOG]
logPath = C:/asn1/logs/process
```

Now execute parser file but with the path to config file in arguments:
```
$ python asn1_parser.py C:\asn1\src\config.ini
```

Your decoded data can be found in file *C:/asn1/src/export/ASN1_TEST_FILE.txt*.

Also you get two logs:
* C:/asn1/src/logs/process/asn1_test_parser_20181204130822.log with text in it:
```
[2018-12-04 13:08:22][INFO][ASN1 Parser started successfully]
[2018-12-04 13:08:22][INFO][Import folder: C:\asn1\src\import]
[2018-12-04 13:08:22][INFO][Export folder: C:\asn1\src\export]
[2018-12-04 13:08:22][INFO][File history folder: C:\asn1\src\logs\history]
[2018-12-04 13:08:22][INFO][Structure for input data definied from C:\asn1\src\structure\input.txt]
[2018-12-04 13:08:22][INFO][Structure for output data definied from C:\asn1\src\structure\output.txt]
[2018-12-04 13:08:22][INFO][Column separator: ;]
[2018-12-04 13:08:22][INFO][Start parsing.]
[2018-12-04 13:08:22][INFO][Found files in folder: 1. List of files below.]
ASN1_TEST_FILE.bin
[2018-12-04 13:08:22][INFO][Begin to process file ASN1_TEST_FILE.bin]
[2018-12-04 13:08:22][INFO][Parse bytes to blocks...]
[2018-12-04 13:08:31][INFO][Blocks found: 32234]
[2018-12-04 13:08:31][INFO][SUCCESS]
[2018-12-04 13:08:31][INFO][Recognize blocks...]
[2018-12-04 13:08:33][INFO][SUCCESS]
[2018-12-04 13:08:33][INFO][Decode data in blocks...]
[2018-12-04 13:08:37][INFO][SUCCESS]
[2018-12-04 13:08:37][INFO][Convert blocks to records...]
[2018-12-04 13:08:39][INFO][Records found: 32234]
[2018-12-04 13:08:39][INFO][SUCCESS]
[2018-12-04 13:08:40][INFO][Export records to C:\asn1\src\export\ASN1_TEST_FILE.txt...]
[2018-12-04 13:08:40][INFO][SUCCESS]
[2018-12-04 13:08:40][INFO][Write info to file history...]
[2018-12-04 13:08:41][INFO][SUCCESS]
[2018-12-04 13:08:41][INFO][Finish parsing. Execution time 18.735471487045288]
```

* C:/asn1/src/logs/history/asn1_test_20181204130822.log with data for table in it:

|END_TIMESTAMP      |FILE_NUMBER|FILE_NAME         |FILE_SIZE|COUNT_RECORDS|STATUS|
|-------------------|-----------|------------------|---------|-------------|------|
|2018-12-04 13:08:41|1          |ASN1_TEST_FILE.bin|8388482  |32234        |OK    |

#### Viewer
To get raw ASN.1 structure of file use viewer functionality.

To do that execute viewer file:
```
$ python asn1_viewer.py C:\asn1\src\config.ini
```

Your file structure can be found in file *C:/asn1/src/views/ASN1_TEST_FILE.json*.

Also you get the log:
* C:/asn1/src/logs/process/asn1_test_viewer_20181204141140.log with text in it:
```
[2018-12-04 14:11:40][INFO][ASN1 Viewer started successfully]
[2018-12-04 14:11:40][INFO][Import folder: C:\asn1\src\import]
[2018-12-04 14:11:40][INFO][Views folder: C:\asn1\src\views]
[2018-12-04 14:11:40][INFO][Start.]
[2018-12-04 14:11:40][INFO][Found files in folder: 1. List of files below.]
ASN1_TEST_FILE.dat
[2018-12-04 14:11:40][INFO][Begin to process file ASN1_TEST_FILE.dat]
[2018-12-04 14:12:03][INFO][Finish. Execution time 23.11560583114624]
```
