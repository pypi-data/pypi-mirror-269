# SimpleWikiParser
An Simplified Wiki Data Parser

## Installation
```bash
pip install git+https://github.com/Biswajit2902/SimpleWikiParser.git
```

## Usage:
```python
from wikiparser.core import WikiMediaDumpParser

# initialise Parser for a language (say Hindi)
wiki_dump_parser = WikiMediaDumpParser(language="Hindi")

# parse
wiki_dump_parser.parse()

# export
wiki_dump_parser.export_hf_dataset("/path/to/data.jsonl", "dataset_name")
```
