# pyhstr

Work in progress, but it's pretty usable already.

### Installation

```bash
git clone https://github.com/adder46/pyhstr.git
cd pyhstr
python3 -m pip install -e .
```

### Usage

You should make an alias:

```bash
alias py='python3 -ic "from pyhstr import hh"'
```

![screenshot](pyhstr.gif)

### FIXME 

- make it work for ipython (how do I set sys.displayhook on IPython?)
- handle non-existant config files
- remove duplicates from "history"
- handle pages (1/0)