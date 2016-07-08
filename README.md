UniversalDictTools / DictUtils
===
A universal Python-based utility and library to download, process and build dictionary in MDict, Apple XML and multiple
formats.

---

This utility includes tools to help from grabbing data to building dictionaries.

## Simple Guide to Usage

### `grab` Module
This module implements a feature-rich downloader that supports auto-retry and break-point resuming. With the
`DictUtils.grab.grabber` module, a variety of types of downloader that handles different formats from different sources
can be easily written. A simple example to utilize this module is as below.

```python
from DictUtils.grab import HTML
# ....
with open('filename.ext', 'r') as csv:
        dl = HTML.by_csv(csv, file_prefix=sys.argv[2])
        dl.download_all(thread=3)
```

### `build` Module
This module is design as a `Provider - Generator` architecture, alike to `Server - Client` architecture. A `Provider`,
obviously, would provide dictionary data to a `Generator`. Some parameters like css file can be specified in the
constructor. A simple example to convert `Apple XML` format to `MDict Source` format is as below.

```python
from DictUtils.build.Provide.AppleDictXML import AppleDictXMLProvider
from DictUtils.build.Generate.MDict import MDictGenerator
# ....
with open('source.xml', 'r') as source:
    provider = AppleDictXMLProvider(source, handler=handler)

content = MDictGenerator(provider, css='wngyhycd.css')
with open('out.txt', 'w', newline='\r\n') as target:
   target.write(str(content)) # simply str() the generator will get the correct output
```

A `Provider` is the subclass of `Dictionary` class. You can implement your own `Provider` to fit your needs.

## Contributing
Pull-requests are always welcome.