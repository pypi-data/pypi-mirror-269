# Multiply library
A small demo library.

### Installation
```
pip install multiply_bootleg_dev
```

### Run tests
```
python3 -m unittest -v tests/multiplication_tests.py
```

### Build Steps
```
pip3 install wheel
pip3 install twine
python3 -m build
twine check dist/*
python3 -m twine upload --repository pypi dist/*
```




### Get started
How to multiply one number by another with this lib:

```Python
from multiply_bootleg_dev import Multiplication

# Instantiate a Multiplication object
multiplication = Multiplication(2)

# Call the multiply_bootleg_dev method
result = multiplication.multiply(5)
```
