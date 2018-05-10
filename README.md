# scrapy-gdpr
A scrapy module to find things that might be of interest when auditing a site for GDPR.

## Functionality
Currently will output data about:

* Forms (which may be collecting personal data)
* iFrames (which may be linking out to site which collects personal data)

## Usage
This is a python3 module for scrapy. If you're on a Mac, the steps to run it are roughly as follows:

1. Install python3. Best done via homebrew (https://brew.sh/):
```
$ brew install python3
```

2. Install virtualenv
```
$ pip3 install virtualenv
```

3. Create a virtualenv and install scrapy
```
$ virtualenv -p python3 scrapy-gdpr
```

4. Install scrapy in your virtualenv
```
cd scrapy-gdpr
source bin/activate
pip install scrapy
git checkout https://github.com/gkluoe/scrapy-gdpr.git
```

5. Run it (<url_file> should be the path to a file containing a list of URLs to use as start points, one per line):
```
scrapy runspider gdpr.py -a urlfile=<url_file> -t csv -o outfile.csv
```

You can output in formats other than csv - see the scrapy documentation for more detail.
