"""
supportfuncs.py - Support functions needed by guicalculator. These functions do 
not depend on the calculator interface or data, other than data passed in to and
back from the function.

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

import ast
import keyword
import operator
from decimal import Decimal
from typing import Callable, Type
from unicodedata import normalize

from .globals import DEFAULT_VARIABLES, VariablesType

# map of ast operators to functions used by parser
OPERATOR_MAP: dict[Type[ast.AST], Callable] = {
    ast.Div: operator.truediv,
    ast.Mult: operator.mul,
    ast.Sub: operator.sub,
    ast.Add: operator.add,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Pow: operator.pow,
}


def numtostr(
    val: int | float | Decimal,
    commas: bool = False,
    removeZeroes: bool = True,
) -> str:
    """
    numtostr - Convert number to string.

    Converts an int or float or Decimal to a string representation. Can
    add thousand separators and/or remove trailing zeroes after a decimal
    point.

    Notes
    -----
    As a side effect, will round the number currently being input to the
    precision in the Decimal context if removeZeroes is True.

    Parameters
    ----------
    val : int | float | Decimal
        Number to be converted
    commas : bool, optional
        True means add thosands separators (commas). By default False.
    removeZeroes : bool, optional
        True means remove trailing zeroes after the decimal point.
        By default True.

    Returns
    -------
    str
        The string representation of the number
    """
    v: int | float | Decimal
    if commas:
        c = ","
    else:
        c = ""

    if isinstance(val, Decimal):
        if val == val.to_integral_value() and removeZeroes:
            v = val.to_integral_value()
        else:
            if removeZeroes:
                v = (
                    val.quantize(Decimal(1))
                    if val == val.to_integral()
                    else val.normalize()
                )
            else:
                v = val
        fmt = "{0:" + c + "f}"
    elif val == int(val) and removeZeroes:
        v = int(val)
        fmt = "{0:" + c + "d}"
    else:
        v = val
        fmt = "{0:" + c + ".28g}"

    return fmt.format(v)


def strtodecimal(val: str) -> Decimal:
    """
    strtodecimal  - convert string value to Decimal.

    Parameters
    ----------
    val : str
        Value to be converted

    Returns
    -------
    Decimal
        Converted value
    """
    if val:
        return Decimal(val.replace(",", ""))
    else:
        return Decimal(0)


def evaluate_calculation(
    current_calculation: str, user_variables: VariablesType
) -> Decimal:
    """
    evaluate_calculation - Evaluate the provided calculation, returning the
    result as Decimal.

    Parameters
    ----------
    current_calculation : str
        The calculation
    user_variables : VariablesType : dict[str, Decimal]
        Dictionary of user defined variables

    Returns
    -------
    Decimal
        The result of the calculation

    Raises
    ------
    TypeError
        Used for custom errors, message indicates what the specific error was.

    """

    # validate that nothing improper is in user_variables
    # we should be able to trust DEFAULT_VARIABLES
    for nam, val in user_variables.items():
        if (
            not nam
            or type(nam) != str
            or not nam.isidentifier()
            or keyword.iskeyword(nam)
        ):
            raise TypeError("Invalid variable name {nam!r}")
        if nam in DEFAULT_VARIABLES.keys():
            raise TypeError("Attempt to overwrite default variable {nam!r}")
        if not val or type(val) != Decimal:
            raise TypeError("Invalid value for variable {nam!r}: {val!r}")

    # validate we actually have a str in current_calculation
    if not current_calculation or type(current_calculation) != str:
        raise TypeError("Invalid calculation")

    root_node = ast.parse(current_calculation, mode="eval")

    # internal function, nested so it can't be called directly
    # unnesting would require moving above validation inside the function
    def _eval(node: ast.AST) -> Decimal:
        """_eval - Internal recursive function to evaluate the ast nodes"""

        # used in multiple error messages
        node_fmtd = ast.dump(node, indent=2)

        match node:
            case ast.Expression():
                return _eval(node.body)

            # replaced with Decimal numbers, left in just in case
            case ast.Constant():
                if isinstance(node.value, (int, float)):
                    return +Decimal(node.value)
                else:
                    raise TypeError(f"Unknown constant: ast.{node_fmtd}")

            case ast.BinOp():
                left, right, op = node.left, node.right, node.op
                method = OPERATOR_MAP[type(op)]
                return method(_eval(left), _eval(right))

            case ast.UnaryOp():
                operand, uop = node.operand, node.op
                method = OPERATOR_MAP[type(uop)]
                return method(_eval(operand))

            case ast.Name():
                if normalize("NFKC", node.id) in DEFAULT_VARIABLES:
                    return +DEFAULT_VARIABLES[normalize("NFKC", node.id)]

                elif normalize("NFKC", node.id) in user_variables:
                    return +user_variables[normalize("NFKC", node.id)]

                else:
                    node_escpd = node.id.encode("unicode_escape")
                    raise TypeError(f"Unknown variable: {node_escpd!r}")

            case ast.Call():
                pkg, func = _get_caller(node, node_fmtd)

                # if I ever allow more function calls, will have to make another dict
                if (pkg, func) in (("decimal", "Decimal"), ("", "Decimal")):
                    parm = _get_str_parameter(node)
                    return +Decimal(parm)
                elif (pkg, func) == ("Decimal", "sqrt"):

                    return Decimal.sqrt(_eval(node.args[0]))
                else:
                    raise TypeError(
                        f"Unknown function call: {pkg}.{func}: \nast.{node_fmtd}"
                    )

            case _:
                raise TypeError(f"Unknown ast node: \nast.{node_fmtd}")

    def _get_str_parameter(node):
        """_get_str_parameter - Internal function to return a single str parameter"""

        if len(node.args) == 1 and isinstance(node.args[0], ast.Constant):
            parm = node.args[0].value
        else:
            raise TypeError("Decimal function accepts exactly one argument")
        if type(parm) == str:
            return parm
        else:
            raise TypeError("Decimal function should only have str parameter")

    def _get_caller(node, node_fmtd):
        """_get_caller - Internal function to get calling module/function name"""

        if isinstance(node.func, ast.Attribute):  # package.procedure
            if isinstance(node.func.value, ast.Name):
                pkg = node.func.value.id
                func = node.func.attr
            else:  # ??? not sure if this can happen
                errmsg = f"Unknown type of ast.Call: \nast.{node_fmtd}"
                raise TypeError(errmsg)

        elif isinstance(node.func, ast.Name):  # procedure
            pkg = ""
            func = node.func.id

        else:  # ??? not sure if this can happen
            errmsg = f"Unknown type of ast.Call: \nast.{node_fmtd}"
            raise TypeError(errmsg)
        return pkg, func

    val = _eval(root_node)
    return val
