
[![Build Status](https://travis-ci.org/hachibeeDI/namedparser.svg?branch=master)](https://travis-ci.org/hachibeeDI/namedparser) [![Coverage Status](https://coveralls.io/repos/hachibeeDI/namedparser/badge.svg?branch=master&service=github)](https://coveralls.io/github/hachibeeDI/namedparser?branch=master)

# namedparser

Read name-daemon configuration files like the bind

# Installation

```bash
$ pip install https://github.com/hachibeeDI/namedparser/archive/master.zip
```

# Example

```python
from namedparser import Parser

txt = '''
options {
    directory "/var/na/named";
    check-names master ignore;
    check-names slave ignore;
    check-names response ignore;
    allow-recursion {
        any;
    };
    allow-query {
        any;
    };
    allow-query-cache {
        any;
    };
    allow-transfer { 127.0.0.1; };
    max-cache-ttl  3600000;
    min-retry-time  50;
    max-acache-size 4M;
    max-cache-size 4M;
    max-journal-size 100k;
    version "";
};
'''

result = Parser.parse_string(txt)
options = result.search('options')
check_names = options[0].search('check-names')
assert check_names[0].target == 'master'
assert check_names[1].target == 'slave'
assert check_names[2].target == 'response'

directory = options[0].search('directory')[0]
assert directory.value == '/var/na/named'
assert str(directory) == 'directory "/var/na/named";'
```

You may get more information how to acceess some nodes in `named.conf`, if you read test code in `namedparser/testsuite/test_parser.py`.


# Support

You may run on

- 2.6
- 2.7
- 3.*
