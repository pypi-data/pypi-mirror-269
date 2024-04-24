"""
globals.py - Variables needed by more than one module.

Copyright (c) 2024 Thomas Brotherton

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from decimal import Decimal
from typing import NewType
from unicodedata import normalize

PI = "\u03c0"


VariablesType = NewType("VariablesType", dict[str, Decimal])
"""Type to store varaibles and values for the parser: dict[str, Decimal]"""

# stores default variables pi and e
# including first 30 digits because default precision is 28 in Decimal
# hard coding instead of using math.pi due to float to Decimal rounding issues
DEFAULT_VARIABLES: VariablesType = VariablesType(
    {
        normalize("NFKC", PI): Decimal("3.141592653589793238462643383279"),
        "e": Decimal("2.718281828459045235360287471352"),
    }
)
