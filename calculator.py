import tkinter

button_values = [
    ["AC", "+/-", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="],
]

right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["AC", "+/-", "%"]

row_count = len(button_values)
column_count = len(button_values[0])

color_light_gray = "#D4D4D2"
color_black = "#1C1C1C"
color_dark_gray = "#505050"
color_orange = "#FF9500"
color_white = "white"

window = tkinter.Tk()
window.title("Calculator")
window.resizable(False, False)

frame = tkinter.Frame(window)
label = tkinter.Label(
    frame,
    text="0",
    font=("Arial", 45),
    background=color_black,
    foreground=color_white,
    anchor="e",
    width=column_count,
)
label.grid(row=0, column=0, columnspan=column_count, sticky="we")

for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]
        button = tkinter.Button(
            frame,
            text=value,
            font=("Arial", 30),
            width=column_count - 1,
            height=1,
            command=lambda value=value: button_clicked(value),
        )

        if value in top_symbols:
            button.config(foreground=color_black, background=color_light_gray)
        elif value in right_symbols:
            button.config(foreground=color_white, background=color_orange)
        else:
            button.config(foreground=color_white, background=color_dark_gray)

        button.grid(row=row + 1, column=column)

frame.pack()

A = "0"
operator = None
B = None


def clear_all():
    global A, B, operator
    A = "0"
    B = None
    operator = None
    label["text"] = "0"


def remove_zero_decimal(num):
    if isinstance(num, float) and num.is_integer():
        num = int(num)
    return str(num)


def compute_expression(first_value, second_value, selected_operator):
    first_number = float(first_value)
    second_number = float(second_value)

    if selected_operator == "+":
        return first_number + second_number
    if selected_operator == "-":
        return first_number - second_number
    if selected_operator == "×":
        return first_number * second_number
    if selected_operator == "÷":
        if second_number == 0:
            raise ZeroDivisionError("Division by zero")
        return first_number / second_number
    return second_number


def button_clicked(value):
    global A, B, operator

    if value in right_symbols:
        if value == "=":
            if A is not None and operator is not None:
                try:
                    result = compute_expression(A, label["text"], operator)
                    label["text"] = remove_zero_decimal(result)
                    A = label["text"]
                    B = None
                    operator = None
                except ValueError:
                    label["text"] = "Error"
                    clear_all()
                except ZeroDivisionError:
                    label["text"] = "Error"
                    clear_all()

        elif value in "+-×÷":
            if operator is not None and A is not None:
                try:
                    result = compute_expression(A, label["text"], operator)
                    A = remove_zero_decimal(result)
                    label["text"] = A
                except ValueError:
                    label["text"] = "Error"
                    clear_all()
                    return
                except ZeroDivisionError:
                    label["text"] = "Error"
                    clear_all()
                    return

            A = label["text"]
            operator = value
            B = "0"
            label["text"] = "0"

    elif value in top_symbols:
        if value == "AC":
            clear_all()
        elif value == "+/-":
            try:
                result = float(label["text"]) * -1
                label["text"] = remove_zero_decimal(result)
            except ValueError:
                label["text"] = "Error"
                clear_all()
        elif value == "%":
            try:
                result = float(label["text"]) / 100
                label["text"] = remove_zero_decimal(result)
            except ValueError:
                label["text"] = "Error"
                clear_all()

    elif value == "√":
        try:
            result = float(label["text"]) ** 0.5
            label["text"] = remove_zero_decimal(result)
        except ValueError:
            label["text"] = "Error"
            clear_all()

    else:
        if value == ".":
            if "." not in label["text"]:
                label["text"] += value
        elif value in "0123456789":
            if label["text"] == "0" or label["text"] == "Error":
                label["text"] = value
            else:
                label["text"] += value


window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

window.mainloop()