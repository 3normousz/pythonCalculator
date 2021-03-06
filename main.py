import tkinter as tk

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
SEMIXTRASMALL_FONT_STYLE = ("Arial", 14)
XTRASMALL_FONT_STYLE = ("Arial", 12)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"
IOS_ORANGE = "#FEA00C"
IOS_GRAY = "#A5A5A5"


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("myCalculator")

        self.x = 0
        self.textbox = ""

        self.historyExpression = ""
        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            # 0: (4, 1),
            ".": (4, 3)
        }

        self.zerodigit = {
            0: (4, 1)
        }

        self.operations = {
            "/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"
        }

        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        self.create_history_button()
        self.create_digits_buttons()
        self.create_zerodigit_buttons()
        self.create_operators_buttons()
        self.create_special_buttons()

    def create_history_frame(self):
        if self.x == 0:
            self.historyWindow = tk.Tk()
            self.historyWindow.geometry("+%d+%d" % (self.window.winfo_rootx() + 373, self.window.winfo_rooty() - 26))
            self.historyWindow.geometry("275x467")
            self.historyWindow.resizable(0, 0)
            self.historyWindow.title("calculatorHistory")

            self.textbox = tk.Label(self.historyWindow, justify=tk.LEFT, font=XTRASMALL_FONT_STYLE)
            self.textbox.pack(anchor=tk.W)
            self.textbox.config(text=self.historyExpression)

            self.x = 1

        elif self.x == 1:
            try:
                self.historyWindow.destroy()
                self.x = 0
            except:
                self.historyWindow = tk.Tk()
                self.historyWindow.geometry("+%d+%d" % (self.window.winfo_rootx() + 368, self.window.winfo_rooty() - 31))
                self.historyWindow.geometry("275x467")
                self.historyWindow.resizable(0, 0)
                self.historyWindow.title("calculatorHistory")

                self.textbox = tk.Label(self.historyWindow, justify=tk.LEFT, font=XTRASMALL_FONT_STYLE)
                self.textbox.pack()
                self.textbox.config(text=self.historyExpression)
                pass

    def create_history_button(self):
        button = tk.Button(self.buttons_frame, text=str("History"), bg=OFF_WHITE, fg=LABEL_COLOR,
                           font=SEMIXTRASMALL_FONT_STYLE, borderwidth=0, command=lambda: self.create_history_frame())
        button.grid(row=0, column=2,columnspan=2, sticky=tk.NSEW)

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")
        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digits_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR,
                               font=DIGITS_FONT_STYLE, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def create_zerodigit_buttons(self):
        for digit, grid_value in self.zerodigit.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR,
                               font=DIGITS_FONT_STYLE, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], columnspan=2, sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operators_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=str(symbol), bg=IOS_ORANGE, fg=LABEL_COLOR,
                               font=DEFAULT_FONT_STYLE, borderwidth=0,
                               command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text=str("Clear"), bg=OFF_WHITE, fg=LABEL_COLOR,
                           font=SEMIXTRASMALL_FONT_STYLE, borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, columnspan=1, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()

        try:
            self.historyExpression += self.total_expression + " " + "=" + " " + str(eval(self.total_expression)) + "\n"
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""

        except Exception as e:
            self.current_expression = "Error"

        finally:
            self.update_history()
            self.update_label()


    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text=str("="), bg=IOS_ORANGE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=4, columnspan=1, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')

        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def update_history(self):
        try:
            self.textbox.config(text=self.historyExpression)
        except:
            pass

    def run(self):
        self.window.mainloop()



if __name__ == "__main__":
    calc = Calculator()
    calc.run()
