# Humble Bundle Downloader

This script leverages the Humble Bundle API to download all the books in a
bundle once they are bought. This script was inspired by way too much clicking
on the Humble Bundle website to download all my books.

### Installation

Simply clone the repository and the install the dependencies with:
```
pip install -r requirements.txt
```

### Usage
```
Usage:       hb_download.py KEY [PATH]
             hb_download.py --key KEY [--path PATH]
```

The optional `PATH` variable is the folder where all the books will be
deposited once they have been downloaded. Books will only download if they pass
the checksum.
