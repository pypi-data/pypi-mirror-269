"""
guicalculator.py - This is the gui calculator. For an example of how to run it, 
see __main__.py.

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

import keyword
import tkinter as tk
from decimal import Decimal
from tkinter import scrolledtext, ttk
from typing import Any, Dict, Tuple

from .buttoncfg import ButtonInfo, ButtonLocation, buttons
from .globals import DEFAULT_VARIABLES, VariablesType
from .supportfuncs import evaluate_calculation, numtostr, strtodecimal

FONT = ("TkDefaultFont", "12", "bold")


class GuiCalculator(tk.Tk):
    """
    GuiCalculator - The root calculator window
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.title("Calculator")

        self.style = CalcStyle()

        # frame that contains the calculator
        self.calcfrm = CalcFrm(padding="5")
        self.calcfrm.grid(column=0, row=0, sticky="news")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # set size
        self.geometry("400x500")
        self.minsize(400, 500)


class CalcStyle(ttk.Style):
    """
    CalcStyle - The ttk.Style object for the calculator
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.theme_use("alt")

        self.configure("TLabel", font=FONT)

        self.configure("Treeview", font=FONT)
        self.configure("Treeview.Heading", font=FONT)

        self.configure("TButton", font=FONT)

        self.map(
            "number.TButton",
            foreground=[("active", "white"), ("!active", "white")],
            background=[("active", "gray45"), ("!active", "gray55")],
        )

        self.configure("orange.TButton", background="darkorange2")
        self.configure("red.TButton", background="orangered2")
        self.configure("memory.TButton", background="lightcyan3")
        self.configure("mathop.TButton", background="cornsilk3")


class CalcFrm(ttk.Frame):
    """
    CalcFrm - The main frame of the calculator root window. Everything is
    in this frame.
    """

    # data used by the calculator
    current_display_calc: str = ""  # the current caolculation to be displayed
    current_eval_calc: str = ""  # the current calculation to be evalueated
    current_input: str = ""  # the current number input

    user_variables: VariablesType = VariablesType({})  # user defined variables

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # self.buttons = bc.get_buttons(self)  # the list of calculator buttons

        # scrolled text display
        self.display = scrolledtext.ScrolledText(
            self,
            height=10,
            width=20,
            font=FONT,
        )
        # display is only enabled when we write to it
        self.display.configure(state="disabled")
        self.display.grid(row=0, column=0, sticky="news")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # frame to hold the memory display
        self.memfrm = MemDispFrm(self)
        self.memfrm.grid(column=0, row=1, sticky="news")
        self.rowconfigure(1, weight=0)

        # frame to hold the buttons
        self.btnfrm = BtnDispFrm(self)
        self.btnfrm.grid(column=0, row=2, sticky="news")
        self.rowconfigure(2, weight=1)

        self.winfo_toplevel().bind(
            "<Escape>", lambda _: self.winfo_toplevel().destroy()
        )

    def get_current_display_calc(
        self, symbol: str = "", func: Tuple[str, str] = None  # type: ignore
    ) -> str:
        """
        get_current_display_calc - Get the current displayed calculation.

        Get the current displayed calculation, including current number input
        and optional mathematical operator.

        Parameters
        ----------
        symbol : str, optional
            Optional string to be added to the end of the calculation. Normally
            will be blank or a mathematical operator, by default "".

        Returns
        -------
        str
            The current displayed calculation.
        """

        if self.current_input:
            inpt = numtostr(
                self.get_current_input(),
                commas=True,
                removeZeroes=False,
            )
            if self.current_input[-1] == ".":
                inpt += "."
        else:
            inpt = ""

        if func and inpt:
            if func[0] == "1/":
                inpt = f"({func[0]}{inpt})"
            else:
                inpt = f"{func[0]}({inpt})"

        return_value = " ".join(
            filter(None, [self.current_display_calc, inpt, symbol])
        ).strip()
        return return_value

    def get_current_eval_calc(
        self, symbol: str = "", func: Tuple[str, str] = None  # type: ignore
    ) -> str:
        """
        get_current_eval_calc - Get the current calculation to be evaluated.

        Get the current calculation to be evaluated, including current number
        input and optional mathematical operator. The primary difference from
        get_current_display_calc is that the number inputs are surrounded by
        calls to Decimal to convert int and float inputs into Decimal to avoid
        decimal to binary and back to decimal rounding errors. In other words
        0.3 - 0.2 should be 0.1, not 0.09999999999999998.

        Parameters
        ----------
        symbol : str, optional
            Optional string to be added to the end of the calculation. Normally
            will be blank or a mathematical operator, by default "".

        Returns
        -------
        str
            The calculation to be evaluated.
        """

        if self.current_input:
            i = +self.get_current_input()
            inpt = f"Decimal({str(i)!r})"
        else:
            inpt = ""

        if func and inpt:
            if func[0] == "1/":
                inpt = f"({func[1]}{inpt})"
            else:
                inpt = f"{func[1]}({inpt})"

        return_value = " ".join([self.current_eval_calc, inpt, symbol]).strip()
        return return_value

    def get_current_input(self) -> Decimal:
        """
        get_current_input - Get current number input as a Decimal.

        Returns
        -------
        Decimal
            Decimal version of the number currently being input. 0 if no
            number is currently being input.
        """

        if self.current_input:
            return Decimal(self.current_input)
        else:
            return Decimal(0)

    def update_display(self) -> None:
        """
        update_display - Update the calculator display.

        This works be erasing the last line that displays the formula being
        input and replacing it with the most recent changes as returned by
        get_current_display_calc.
        """

        self.display.configure(state="normal")
        # replace last line
        self.display.delete("end-1l", "end")
        self.display.insert("end", f"\n{self.get_current_display_calc()}")
        # move to end
        self.display.see(tk.END)
        self.display.configure(state="disabled")

    def update_current_calc(
        self, symbol: str = "", func: Tuple[str, str] = None  # type: ignore
    ) -> None:
        """
        update_current_calc - Update the current calculation being input.

        Uses get_current_display_calc and get_current_eval_calc to generate
        the most recent versions of the calculation being input (including
        the current number being input and the operator being input passed
        in by symbol) and stores them in globals.current_display_calc and
        globals.current_eval_calc. Then calls update_display.

        Notes
        -----
        As a side effect, will round the number currently being input to the
        precision in the Decimal context.

        Parameters
        ----------
        symbol : str, optional
            Optional string to be added to the end of the calculation. Normally
            will be blank or a mathematical operator, by default "".
        """

        if self.current_input:  # if we have a value, round it
            self.current_input = numtostr(self.get_current_input())

        self.current_display_calc = self.get_current_display_calc(symbol, func)
        self.current_eval_calc = self.get_current_eval_calc(symbol, func)
        self.current_input = ""

        self.update_display()

    def process_button(self, buttoncmd: str, buttontxt: str | int = "") -> None:
        """
        process_button - Process a calculator button press.

        Parameters
        ----------
        buttoncmd : str
            The command string from the ButtonInfo dictionary in
            buttoncfg.py buttons.
        buttontxt : str | int, optional
            For buttons in buttoncfg.py that don't have a command
            (number and basic math symbols) this is the button label,
            by default ""
        """

        match buttoncmd:
            case "button":
                self.button_press(buttontxt)

            case "backspace":
                self.backspace()

            case "calculate":
                self.calculate()

            case "clearAll":
                self.clear_all()

            case "clearValue":
                self.clear_value()

            case "inverseNumber":
                self.inverse_number()

            case "invertSign":
                self.invert_sign()

            case "memAdd":
                self.memory_add()

            case "memClear":
                self.memory_clear()

            case "memRecall":
                self.memory_recall()

            case "memStore":
                self.memory_store()

            case "memSubtract":
                self.memory_add(False)

            case "memSwap":
                self.memory_swap()

            case "rootNumber":
                self.root_number()

            case "squareNumber":
                self.square_number()

            case "varsPopup":
                self.vars_popup()

            case "xToTheY":
                self.button_press("**")
            case _:
                self.bell()
                print(f"Unknown command: {buttoncmd!r}")

    def button_press(self, symbol: str | int) -> None:
        """
        button_press - Handles simple button presses.

        Handles simple button presses that just add to the current formula. For
        example, a digit (passed as int, not str), ".", "+", "-", etc. Does not
        handle complex things like computing the square root of the current
        number being input.

        Notes
        -----
        As a side effect, will round the number currently being input to the
        precision in the Decimal context if symbol is not a digit or decimal
        point.

        Parameters
        ----------
        symbol : str | int
            The digit or mathematical operator being processed.
        """

        if isinstance(symbol, int):
            self.current_input += str(symbol)
            self.update_display()

        elif symbol == ".":
            if symbol in self.current_input:
                self.bell()
                return

            self.current_input = (self.current_input or "0") + symbol
            self.update_display()

        else:
            self.update_current_calc(symbol)

    def backspace(self) -> None:
        """
        backspace - Erase last character from number being input.
        """

        if self.current_input:
            self.current_input = self.current_input[:-1]
        self.update_display()

    def clear_value(self) -> None:
        """
        clear_value - Clear the current number input, or if that is empty
        then clear the current calculation.
        """

        if self.current_input:
            self.current_input = ""
        else:
            self.current_display_calc = ""
            self.current_eval_calc = ""

        self.update_display()

    def clear_all(self) -> None:
        """
        clear_all - Clear the current number being input, the current
        calculation, and the display. Does not clear the value in memory.
        """

        self.display.configure(state="normal")
        self.display.delete(1.0, "end")
        self.display.configure(state="disabled")

        self.current_display_calc = ""
        self.current_eval_calc = ""
        self.current_input = ""

        self.update_display()

    def get_current_memory(self) -> Decimal:
        """
        get_current_memory - Get the current value stored in memory as a
        Decimal.

        Returns
        -------
        Decimal
            Decimal version of the value stored in memory. 0 if no value is
            currently stored in memory.
        """

        mem = self.memfrm.memval.get().replace(",", "")
        if mem:
            return Decimal(mem)
        else:
            return Decimal(0)

    def memory_clear(self) -> None:
        """
        memory_clear - Clear the value stored in memory
        """

        self.memfrm.memval.set("")

    def memory_recall(self) -> None:
        """
        memory_recall - Replace the current number being input with the value
        stored in memory.
        """

        self.current_input = self.memfrm.memval.get().replace(",", "")
        self.update_display()

    def memory_store(self) -> None:
        """
        memory_store - Change the value stored in memory to be the same as the
        current number being input.

        Notes
        -----
        Cannot do a simple set because we round and format the display.

        As a side effect, will round the number currently being input to the
        precision in the Decimal context.
        """

        # get and reformat current value
        cur_val = +self.get_current_input()
        self.current_input = numtostr(cur_val)
        self.update_display()

        # store it
        self.memfrm.memval.set(numtostr(cur_val, commas=True))

    def memory_swap(self) -> None:
        """
        memory_swap - Swap the value stored in memory with the current number
        being input.

        Notes
        -----
        Cannot do a simple swap like (a,b) = (b,a) because we need to cal .set
        on the tk.StringVar that stores the memory value, and we round and
        format the display.

        As a side effect, will round the number currently being input to the
        precision in the Decimal context.
        """

        # get current value (formatted with commas)
        cur_num = numtostr(self.get_current_input(), commas=True)

        # store memory in current value
        self.current_input = self.memfrm.memval.get().replace(",", "")

        # store retrieved current value in memory
        self.memfrm.memval.set(cur_num)

        self.update_display()

    def memory_add(self, addto: bool = True) -> None:
        """
        memory_add - Add or subtract the current number being input to or from
        the value stored in memory.

        Notes
        -----
        If addto is passed in as false, will subtract the value being input
        from memory by multiplying the value by -1 before adding.

        As a side effect, will round the number currently being input to the
        precision in the Decimal context.

        Parameters
        ----------
        addto : bool, optional
            If true, performs addition. If false, performs subtraction.
            By default True.
        """

        # adding or subtracting
        if addto:
            sign = Decimal(1)
        else:
            sign = Decimal(-1)

        # get the current input number (and reformat it)
        cur_val = +self.get_current_input()
        self.current_input = numtostr(cur_val)
        self.update_display()

        # get current memory
        cur_mem = self.get_current_memory()

        # add (or subtract)
        mv = cur_mem + (cur_val * sign)
        self.memfrm.memval.set(numtostr(mv, commas=True))

    def invert_sign(self) -> None:
        """
        invert_sign - Convert the current number being input from positive to
        negative or negative to positive: -x.

        Notes
        -----
        As a side effect, will round the number currently being input to the
        precision in the Decimal context.
        """

        if self.current_input:
            self.current_input = numtostr(-self.get_current_input())
        self.update_display()

    def inverse_number(self) -> None:
        """
        inverse_number - Convert the current number being input to it's
        mathematical inverse: 1/x.

        Notes
        -----
        As a side effect, will round the number currently being input to the
        precision in the Decimal context.
        """
        if self.current_input:
            # inpt = self.get_current_input()
            # if inpt == Decimal(0):
            #     self.bell()
            #     return

            # self.current_input = numtostr(1 / inpt)
            self.update_current_calc(func=("1/", "1/"))
        self.update_display()

    def square_number(self) -> None:
        """
        square_number - Convert the current number being input to its
        square: x**2.

        Notes
        -----
        As a side effect, will round the number currently being input to the
        precision in the Decimal context.
        """

        if self.current_input:
            # self.current_input = numtostr(self.get_current_input() ** 2)
            self.update_current_calc("** 2")
        self.update_display()

    def root_number(self) -> None:
        """
        root_number - Convert the current number being input to its
        square root: Decimal.sqrt(x).

        Notes
        -----
        As a side effect, will round the number currently being input to the
        precision in the Decimal context.
        """

        if self.current_input:
            self.update_current_calc(func=("sqrt", "Decimal.sqrt"))
            # self.current_input = numtostr(Decimal.sqrt(self.get_current_input()))
        self.update_display()

    def vars_popup(self) -> None:
        """
        varsPopup - Display a popup window with currently defined variables.
        """

        # get x and y location for popup
        x = self.winfo_toplevel().winfo_x() + 10
        x = max(x, 10)
        y = self.winfo_toplevel().winfo_y() + 175
        y = max(y, 10)

        self.varspopup = VarsPopup(calcfrm=self)
        self.varspopup.geometry("+%d+%d" % (x, y))

    def calculate(self) -> None:
        """
        calculate - Performs the current calculation and updates the display
        with the results.
        """

        # update current calc and display
        self.update_current_calc()

        # if we have a calculation to perform
        if self.current_eval_calc:
            try:
                # run the current calculation
                val = evaluate_calculation(
                    self.current_eval_calc,
                    self.user_variables,
                )

                # clear current calc and set current input to result
                self.current_display_calc = ""
                self.current_eval_calc = ""
                self.current_input = numtostr(val)

                # show the result
                self.display.configure(state="normal")
                self.display.insert(
                    "end", f" =\n{numtostr(val, commas=True)}\n{'=' * 30}\n\n"
                )
                self.display.configure(state="disabled")

            except Exception as error:
                # should probably use a logger
                print(f"ERROR: {error}\n")

                # clear the current calculation and print the error message
                self.current_display_calc = ""
                self.current_eval_calc = ""
                self.current_input = ""

                # show user error message
                self.display.configure(state="normal")
                self.display.insert("end", f"\n= ERROR\n\n")
                self.display.configure(state="disabled")

            # update the display
            self.update_display()


class MemDispFrm(ttk.Frame):
    """
    MemDispFrm - The memory display frame.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.memlbl = ttk.Label(self, text="Memory:")
        self.memlbl.grid(row=0, column=0, sticky="e")

        self.memval = tk.StringVar()
        self.mem_txt = ttk.Label(self, textvariable=self.memval)
        self.mem_txt.grid(row=0, column=1, sticky="w")

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)


class BtnDispFrm(ttk.Frame):
    """
    BtnDispFrm - The calculator button display frame.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # each row with a different number of buttons is a different frame
        # this dict keeps track of all the frames
        self.button_frames: Dict[int, ttk.Frame] = {}

        # this frame contains only frames, so has only one column
        self.columnconfigure(0, weight=1)

        # the keys in buttons are tuples of frame, row, column
        # sorting them ensures we process in the correct order
        for btn_loc, btn_info in sorted(buttons.items()):
            self.add_button(btn_loc, btn_info)

    def add_button(self, btn_loc: ButtonLocation, btn_info: ButtonInfo) -> None:
        """
        add_button - add a button to BtnDispFrm

        Parameters
        ----------
        button_loc : ButtonLocation
            Button location information
        button_info : ButtonInfo
            Button creation information
        """

        """
        at the paranoid level should proably validate that
        everything in button_loc and button_info is what it
        should be and not an injection attack
        """

        # if we have a new frame to add
        if btn_loc.btn_frame not in self.button_frames:

            self.button_frames[btn_loc.btn_frame] = ttk.Frame(self)

            self.button_frames[btn_loc.btn_frame].grid(
                column=0,
                row=btn_loc.btn_frame,
                sticky="news",
            )

        # create the button
        cf: CalcFrm = self.master  # type: ignore
        if "command" in btn_info:
            cmd = lambda x=btn_info["command"]: cf.process_button(x)
        else:
            cmd = lambda x=btn_info["label"]: cf.process_button("button", x)

        btnopts: dict = {"text": btn_info["label"], "command": cmd}
        if "style" in btn_info:
            btnopts["style"] = btn_info["style"]

        cur_btn = ttk.Button(self.button_frames[btn_loc.btn_frame], **btnopts)

        # add the button to the frame
        gridopts: dict = {
            "row": btn_loc.btn_row,
            "column": btn_loc.btn_column,
            "sticky": "news",
        }

        if "rowspan" in btn_info:
            gridopts["rowspan"] = btn_info["rowspan"]

        if "columnspan" in btn_info:
            gridopts["columnspan"] = btn_info["columnspan"]

        cur_btn.grid(**gridopts)

        # if this button is binding any events ...

        if "events" in btn_info:
            for be in btn_info["events"]:
                topwin = self.winfo_toplevel()
                topwin.bind(be, lambda _, c=cur_btn: c.invoke())  # type: ignore

        # configure the weigts for the buttons
        self.button_frames[btn_loc.btn_frame].rowconfigure(
            btn_loc.btn_row,
            weight=1,
        )
        self.button_frames[btn_loc.btn_frame].columnconfigure(
            btn_loc.btn_column,
            weight=1,
        )
        # the weight of the subframe should be proportional to the
        # number of rows in the subframe
        self.rowconfigure(
            btn_loc.btn_frame,
            weight=btn_loc.btn_row + 1,
        )


class VarsPopup(tk.Toplevel):
    """
    VarsPopup - The popup window to display variables.
    """

    def __init__(self, *args, calcfrm: CalcFrm, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.focus_set()
        self.wm_title("Variables")

        self.treefrm = VarsPopupTreeFrm(self, calcfrm=calcfrm)
        self.treefrm.grid(row=0, column=0, sticky="news")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        vars_tree = self.treefrm.vars_tree
        if vars_tree.get_children():
            vars_tree.focus(vars_tree.get_children()[0])
            vars_tree.selection_set(vars_tree.get_children()[0])


class VarsPopupTreeFrm(ttk.Frame):
    """
    VarsPopupTreeFrm - The frame with the variables displayed.
    """

    def __init__(self, *args, calcfrm: CalcFrm, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.calcfrm = calcfrm

        self.focus_set()

        # scrollbar and treeview
        self.scrollbar = ttk.Scrollbar(self, orient="vertical")
        self.vars_tree = ttk.Treeview(
            self,
            yscrollcommand=self.scrollbar.set,
            columns=("value"),
            height=7,
            selectmode="browse",
        )
        self.scrollbar.configure(command=self.vars_tree.yview)
        self.vars_tree.focus_set()

        self.vars_tree.grid(row=0, column=0, sticky="news")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        # our columns in the tree view
        self.vars_tree.heading("#0", text="Variable")
        self.vars_tree.column("#0", width=150, anchor="w")

        self.vars_tree.heading("value", text="Value")
        self.vars_tree.column("value", width=325, anchor="w")

        # this loop iterates over the default variables and adds
        # them to the treeview
        self.add_variable_section("default", DEFAULT_VARIABLES)

        # this loop iterates over the user variables and adds
        # them to the treeview
        self.add_variable_section("user variables", self.calcfrm.user_variables)

        # add buttons to select or edit user variables
        self.buttonfrm = VarsPopupTreeFrmButtons(self, vptf=self)
        self.buttonfrm.grid(row=1, column=0, sticky="news")
        self.rowconfigure(1, weight=0)

        # double click to select
        self.vars_tree.bind(
            "<Double-Button-1>", lambda _: self.buttonfrm.select_button.invoke()
        )

    def add_variable_section(
        self, section_name: str, section_vars: VariablesType
    ) -> None:
        """
        add_variable_section - Add a variable dictionary to the tree frame

        Parameters
        ----------
        section_name : str
            Section Name
        section_vars : VariablesType : dict[str, Decimal]
            Variables
        """

        section_id = self.vars_tree.insert(
            "",
            "end",
            text=section_name,
            values=([""]),
        )
        for v_key, v_value in section_vars.items():
            self.vars_tree.insert(
                section_id,
                "end",
                text=v_key,
                values=([numtostr(v_value, commas=True)]),
            )
        self.vars_tree.item(section_id, open=True)


class VarsPopupTreeFrmButtons(ttk.Frame):
    """
    VarsPopupTreeFrmButtons - The frame with the buttons in the variables
    popup window.

    """

    def __init__(self, *args, vptf: VarsPopupTreeFrm, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.vptf = vptf

        self.edit_button = ttk.Button(
            self,
            text="Edit User Variables",
            command=self.user_vars_edit,
        )
        self.edit_button.grid(row=0, column=0, columnspan=2)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)

        self.cancel_button = ttk.Button(
            self,
            text="Cancel",
            command=self.winfo_toplevel().destroy,
        )
        self.cancel_button.grid(row=1, column=0)
        self.rowconfigure(1, weight=0)

        self.select_button = ttk.Button(
            self,
            text="Select",
            command=self.user_vars_select,
        )
        self.select_button.grid(row=1, column=1)
        self.columnconfigure(1, weight=1)

        top_win = self.winfo_toplevel()
        top_win.bind("<Return>", lambda _: self.select_button.invoke())
        top_win.bind("<Escape>", lambda _: self.winfo_toplevel().destroy())

    def user_vars_select(self) -> None:
        """
        user_vars_select - Return selected variable to the calculator.
        """

        vars_tree = self.vptf.vars_tree

        # if we have one of the variables selected
        # not on "default" or "user variables"
        if (
            vars_tree.selection()
            and vars_tree.selection()[0] not in vars_tree.get_children()
        ):
            self.vptf.calcfrm.button_press(
                vars_tree.item(vars_tree.selection()[0])["text"]
            )

        self.winfo_toplevel().destroy()

    def user_vars_edit(self) -> None:
        """
        user_vars_edit - Popup window to edit the user variables.
        """
        editvars_win = UserVarsEditPopup(calcfrm=self.vptf.calcfrm)

        x = self.winfo_toplevel().winfo_x()
        y = self.winfo_toplevel().winfo_y()
        editvars_win.geometry("+%d+%d" % (x + 10, y + 10))


class UserVarsEditPopup(tk.Toplevel):
    """
    UserVarsEditPopup - Popup window to edit the user variables.
    """

    def __init__(self, *args, calcfrm: CalcFrm, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.focus_set()
        self.wm_title("Edit User Variables")

        self.focus_set()
        self.treefrm = UserVarsEditFrm(self, calcfrm=calcfrm)
        self.treefrm.grid(row=0, column=0, sticky="news")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)


class UserVarsEditFrm(tk.Frame):
    """
    UserVarsEditFrm - The frame with the user variables edit widgets
    """

    def __init__(self, *args, calcfrm: CalcFrm, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.calcfrm = calcfrm

        # column headers
        self.var_lbl = ttk.Label(self, text="User Variable", width=16)
        self.val_lbl = ttk.Label(self, text="Value", width=32)

        lastrow: int = 0
        self.var_lbl.grid(row=lastrow, column=0, sticky="we")
        self.val_lbl.grid(row=lastrow, column=1, sticky="we")

        self.rowconfigure(lastrow, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # validate functions for name/value
        self.validate_var_name = (self.register(self.validate_varname), "%P")
        self.validate_value = (self.register(self.validate_decimal), "%P")

        """
        variable name/value entry widgets

        This dictionary stores all the Text entry boxes for editing 
        user variables.
        
        The tuple[int, int] index is the row and column of the entry widget

        The frame row 0 is the header, so the first variable is row 1.

        Column 0 is variable name.
        Column 1 is variable value.

        So the first variable name is the entry widget at uservars[1,0] 
        not at uservars[0,0].
        """
        self.uservars: dict[Tuple[int, int], ttk.Entry] = {}

        for k, v in calcfrm.user_variables.items():
            lastrow += 1
            self.addrow(lastrow, k, numtostr(v, commas=True))

        # if we had no rows, add a blank one
        if not self.uservars:
            lastrow += 1
            self.addrow(lastrow)

        self.uservars[(1, 0)].focus_set()

        # put these at row 1000 to allow for inserting more rows
        # add row button
        self.addbtn = ttk.Button(
            self,
            text="Add Row",
            command=self.user_vars_edit_addrow,
        )
        self.addbtn.grid(row=1000, column=0)
        self.rowconfigure(1000, weight=0)

        # add delete row nutton
        self.delbtn = ttk.Button(
            self,
            text="Delete Row",
            command=self.user_vars_edit_delrow,
            takefocus=False,
        )
        self.delbtn.grid(row=1000, column=1)

        # add current_calculation button
        self.curcalcbtn = ttk.Button(
            self,
            text="Add current result as new variable",
            command=self.add_current,
        )
        self.curcalcbtn.grid(row=1001, column=0, columnspan=2)
        self.rowconfigure(1001, weight=0)

        topwin = self.winfo_toplevel()
        # cancel button
        self.cancelbtn = ttk.Button(self, text="Cancel", command=topwin.destroy)
        self.cancelbtn.grid(row=1002, column=0)
        self.rowconfigure(1002, weight=0)

        topwin.bind("<Escape>", lambda _: self.cancelbtn.invoke())

        # ok button
        self.okbtn = ttk.Button(
            self,
            text="Ok",
            command=self.user_vars_edit_ok,
        )
        self.okbtn.grid(row=1002, column=1)

        topwin.bind("<Return>", lambda _: self.okbtn.invoke())

        # error message display
        self.errmsg = tk.StringVar(self)
        self.errmsg_lbl = ttk.Label(self, anchor="w", textvariable=self.errmsg)
        self.errmsg_lbl.grid(row=1003, column=0, columnspan=2, sticky="news")
        self.rowconfigure(1003, weight=0)

    def user_vars_edit_delrow(self) -> None:
        """Delete the current row"""

        # find the current row
        cur_widget = self.winfo_toplevel().focus_get()
        if cur_widget in list(self.uservars.values()):
            widget_num = list(self.uservars.values()).index(cur_widget)  # type: ignore
            row = list(self.uservars.keys())[widget_num][0]

            # found it, now destroy entry widgets and remove from dictionary
            self.uservars[(row, 0)].destroy()
            self.uservars[(row, 1)].destroy()
            self.uservars.pop((row, 0), None)
            self.uservars.pop((row, 1), None)

            # if we still have entry widgets, set focus to one of them
            if self.uservars:
                remaining_vars = list(self.uservars.keys())
                if widget_num >= len(remaining_vars):
                    widget_num = -1
                self.uservars[remaining_vars[widget_num]].focus_set()

    def add_current(self) -> None:
        """Add the current calculation result as a variable"""

        currcalc = self.calcfrm.get_current_display_calc()
        if currcalc:
            # get the result
            self.calcfrm.calculate()
            result = self.calcfrm.get_current_input()

            # add result to a new row
            row = self.user_vars_edit_addrow()

            self.uservars[(row, 0)].delete(0, tk.END)
            self.uservars[(row, 0)].insert(0, "x")

            self.uservars[(row, 1)].delete(0, tk.END)
            self.uservars[(row, 1)].insert(0, numtostr(result, commas=True))

    def addrow(self, rownum: int, var: str = "", val: str = "") -> None:
        """
        addrow - Add a row for a new variable

        Parameters
        ----------
        rownum : int
            Row number
        var : str, optional
            Variable name, by default ""
        val : str, optional
            Variable value, by default ""
        """

        self.addtextbox(rownum, 0, var)
        self.addtextbox(rownum, 1, val)

    def addtextbox(self, rownum: int, colnum: int, text: str = "") -> None:
        """
        addtextbox - Add a text entry box for variable name or variable value

        Parameters
        ----------
        rownum : int
            Text box row number
        colnum : int
            Text box column number, 0 for variable name, 1 for variable value
        text : str, optional
            Initial text to put in box, by default ""
        """

        entopts: dict[str, Any]  # entry widget validation options
        if colnum == 0:
            entopts = {
                "validate": "key",
                "validatecommand": self.validate_var_name,
            }
        elif colnum == 1:
            entopts = {
                "validate": "key",
                "validatecommand": self.validate_value,
            }
        else:
            entopts = {}

        tbox = ttk.Entry(self, width=(16 * (colnum + 1)), font=FONT, **entopts)
        tbox.insert(tk.INSERT, text)
        tbox.grid(row=rownum, column=colnum, sticky="news")
        self.uservars[(rownum, colnum)] = tbox
        self.rowconfigure(rownum, weight=1)

        if colnum == 1:
            tbox.bind("<KeyRelease>", self.format_number)

    def format_number(self, event: tk.Event) -> None:
        """
        formatnumber - Format the number input

        Parameters
        ----------
        event : tk.Event
            The event triggering this call
        """

        v = event.widget.get()
        if v:
            # if we have an entry, get it and format it
            v_decimal = strtodecimal(v)
            v_str = numtostr(v_decimal, commas=True, removeZeroes=False)
            if v[-1] == ".":
                v_str += "."
            event.widget.delete(0, tk.END)
            event.widget.insert(0, v_str)

    def validate_varname(self, newnam: str) -> bool:
        """
        validate_varname - Validate that the variable being entered
        is a valid variable name

        Only validates that the new name is a valid identifier. Does
        not check for keywords or duplicate names because input may
        not be completed.

        Parameters
        ----------
        newnam : str
            New variable name

        Returns
        -------
        bool
            True if the name is a valid identifier, False if not.
        """

        if newnam and not newnam.isidentifier():
            self.bell()
            return False

        return True

    def validate_decimal(self, newval: str) -> bool:
        """
        validate_decimal - Validate that the number being entered is a
        valid Decimal.

        Parameters
        ----------
        newval : str
            The number being entered

        Returns
        -------
        bool
            True if the number is a valid Decimal, False if not.
        """

        if newval:
            try:
                _ = strtodecimal(newval)
            except:
                self.bell()
                return False

        return True

    def user_vars_edit_addrow(self) -> int:
        """
        user_vars_edit_addrow - Add a row for a new user variable. Returns row number added
        """

        if self.uservars.keys():
            nextrow = max(r for (r, _) in self.uservars.keys()) + 1
        else:
            nextrow = 1

        self.addrow(nextrow)
        self.uservars[(nextrow, 0)].focus_set()

        return nextrow

    def user_vars_edit_ok(self) -> None:
        """
        user_vars_edit_ok - Update the user variables from entered data
        """

        newuservars: VariablesType = VariablesType({})

        if self.uservars:
            k = self.uservars.keys()
            rows = set(list(zip(*k))[0])
        else:
            rows = set()

        for i in rows:
            # user variable name
            nam = self.uservars[(i, 0)].get().strip()

            # common parts of these error messages
            # extracted for consistency in messaging
            errmsg = f"ERROR:"
            varnam = f"variable name {nam!r}"

            # if we don't have a valid identifier, print an error
            if not nam.isidentifier():
                self.set_errmsg(f"{errmsg} invalid {varnam}")
                self.uservars[(i, 0)].focus_set()
                return

            # if we have a keyword, print an error
            if keyword.iskeyword(nam):
                self.set_errmsg(f"{errmsg} {varnam} is a reserved word")
                self.uservars[(i, 0)].focus_set()
                return

            # if we  have a duplicate variable name, print an error
            if nam in newuservars.keys() or nam in DEFAULT_VARIABLES.keys():
                self.set_errmsg(f"{errmsg} duplicate {varnam}")
                self.uservars[(i, 0)].focus_set()
                return

            # new user variable value
            val = self.uservars[(i, 1)].get().strip()

            # if we don't have a value, print an error
            if not val:
                self.set_errmsg(f"{errmsg} value not set")
                self.uservars[(i, 1)].focus_set()
                return

            # if we don't have a valid Decimal value, print an error
            try:
                val_decimal = +strtodecimal(val)
            except:
                self.set_errmsg(f"{errmsg} invalid numeric value {val!r}")
                self.uservars[(i, 1)].focus_set()
                return

            newuservars[nam] = val_decimal

        # save the new variables
        self.calcfrm.user_variables = newuservars

        # close this window
        self.winfo_toplevel().destroy()

        # rebuild the varspopup
        self.calcfrm.varspopup.destroy()
        self.calcfrm.vars_popup()

    def set_errmsg(self, error_msg: str) -> None:
        """
        set_errmsg - Set the error message and ring a bell

        Parameters
        ----------
        error_msg : str
            Error message to display
        """
        self.bell()
        self.errmsg.set(error_msg)
