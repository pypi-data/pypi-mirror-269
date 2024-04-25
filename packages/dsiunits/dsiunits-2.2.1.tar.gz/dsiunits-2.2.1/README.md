[![pipeline status](https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/badges/main/pipeline.svg)](https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/-/commits/branch)
[![coverage report](https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/badges/amin/coverage.svg)](https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/-/blob/branch/coverage.xml)
# D-SI Parser

This library converts D-SI unit strings to Latex.
And is able to perform math operatins *, / and power with the D-SI units as well as checken weather teh can be converted into each other with scalar multiplication

## Instalaltion

```bash
pip install dsiUnits
```
## Usage
the Constructor `dsiUnit(str)` will parse the string and create a dsiUnit object.
The dsiUnit object has the following methods:
- `toLatex()`: returns the Latex representation of the unit
- `toUTF8()`: returns the UTF8 representation of the unit
- `isScalablyEqualTo(other)`: checks weather the unit is equal to another unit with scalar multiplication
And following magic functions 
- `__mul__(other)`: "*" multiplies the unit with another unit or a scalar
- `__truediv__(other)`:"/" divides the unit by another unit or a scalar
- `__pow__(other)`: "**" raises the unit to the power of another unit or a scalar
- `__eq__(other)`: "==" checks weather the unit is equal to another unit
- `__str__`: "str()" returns the string representation of the unit
- `__repr__`: returns the string representation of the unit

- `toBaseUnitTree()`: returns the base unit tree of the unit
- `reduceFraction()`: reduces the fraction of the unit by resolving all pers and the combinig same units by exponent addition 
- `sortTree()`: sorts the base unit tree of the unit
```python
from dsiUnits import dsiUnit

unit = dsiUnit('\metre\second\tothe{-1}')
latexStr=unit.toLatex()
print(latexStr)
```
```python
from dsiUnits import dsiUnit

mps = dsiUnit(r'\metre\second\tothe{-1}')
kmh = dsiUnit(r'\kilo\metre\per\hour')
scalfactor,baseUnit=mps.isScalablyEqualTo(kmh)
print("The unit "+str(mps)+" is equal to "+str(kmh)+"with a factor of ",scalfactor," and base unit ",str(baseUnit))
```
```python
```

For more usage Examples see the [Example Notebook](https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/-/blob/main/doc/examples.ipynb).
As well as the [pytest file](https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/-/blob/main/src/dsiUnits.py).

