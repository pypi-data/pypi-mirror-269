## pynysiis

The `nysiis` package provides a Python implementation of the [New York State Identification and Intelligence System](https://en.wikipedia.org/wiki/New_York_State_Identification_and_Intelligence_System) (NYSIIS) phonetic encoding algorithm. NYSIIS encodes names based on pronunciation, which is helpful in name-matching and searching applications.

### Requirements

Python 2.7 and later.

### Setup

You can install this package by using the pip tool and installing:

```python
pip install pynysiis
## OR
easy_install pynysiis
```

Install from source with:

```python
python setup.py install --user

## or `sudo python setup.py install` to install the package for all users
```

### Usage

```python
# Basic Usage
from nysiis import NYSIIS

# Create an instance of the NYSIIS class
nysiis = NYSIIS()

# Encode a string using the NYSIIS instance
name = "Watkins"
coded_name = nysiis.encode(name)
print(coded_name) # Output: "WATCAN"


## Comparing Names
from nysiis import NYSIIS

# Create an instance of the NYSIIS class
nysiis = NYSIIS()

name1 = "John Smith"
name2 = "John Smyth"

coded_name1 = nysiis.encode(name1)
coded_name2 = nysiis.encode(name2)

if coded_name1 == coded_name2:
    print("The names are likely to be the same.")
else:
    print("The names are different.")

# Output:
# The names are likely to be the same.


## Handling different names
from nysiis import NYSIIS

# Create an instance of the NYSIIS class
nysiis = NYSIIS()

names = ["Watkins", "Robert Johnson", "Samantha Williams", "Olanrewaju Akinyele",
        "Obinwanne Obiora", "Abdussalamu Abubakar", "Virat Kohli", "Usman Shah"]

for name in names:
    coded_name = nysiis.encode(name)
    print(f"Original: {name}, NYSIIS: {coded_name}")

    # Output:
    # Original: Watkins, NYSIIS: WATCAN
    # Original: Robert Johnson, NYSIIS: RABART
    # Original: Samantha Williams, NYSIIS: SANANT
    # Original: Olanrewaju Akinyele, NYSIIS: OLANRA
    # Original: Obinwanne Obiora, NYSIIS: OBAWAN
    # Original: Abdussalamu Abubakar, NYSIIS: ABDASA
    # Original: Virat Kohli, NYSIIS: VARATC
    # Original: Usman Shah, NYSIIS: USNANS
```

### Reference

```tex
@inproceedings{Rajkovic2007,
  author    = {Petar Rajkovic and Dragan Jankovic},
  title     = {Adaptation and Application of Daitch-Mokotoff Soundex Algorithm on Serbian Names},
  booktitle = {XVII Conference on Applied Mathematics},
  editors   = {D. Herceg and H. Zarin},
  pages     = {193--204},
  year      = {2007},
  publisher = {Department of Mathematics and Informatics, Novi Sad},
  url       = {https://jmp.sh/hukNujCG}
}
```

### Additional References

+ [Commission Implementing Regulation (EU) 2016/480](https://www.legislation.gov.uk/eur/2016/480/contents)
+ [Commission Implementing Regulation (EU) 2023/2381](https://eur-lex.europa.eu/eli/reg_impl/2023/2381/oj)

### License

This project is licensed under the [MIT License](./LICENSE).

### Copyright

(c) 2024 [Finbarrs Oketunji](https://finbarrs.eu/). All Rights Reserved.