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

A = None
operator = None
waiting_for_second_operand = False


def clear_all():
    global A, operator, waiting_for_second_operand
    A = None
    operator = None
    waiting_for_second_operand = False
    label["text"] = "0"


def show_error():
    global A, operator, waiting_for_second_operand
    A = None
    operator = None
    waiting_for_second_operand = True
    label["text"] = "Error"


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
    global A, operator, waiting_for_second_operand

    if value == "AC":
        clear_all()
        return

    # Ekranda "Error" varsa, rəqəm basılana qədər digər əməliyyatları blokla
    if label["text"] == "Error" and value not in "0123456789.":
        return

    if value in right_symbols:
        if value == "=":
            if A is not None and operator is not None and not waiting_for_second_operand:
                try:
                    result = compute_expression(A, label["text"], operator)
                    label["text"] = remove_zero_decimal(result)
                    A = None
                    operator = None
                    waiting_for_second_operand = True
                except (ValueError, ZeroDivisionError):
                    show_error()

        elif value in "+-×÷":
            # Əgər artıq operator seçilibsə və ikinci ədəd hələ yazılmayıbsa, sadəcə operatoru dəyiş
            if operator is not None and waiting_for_second_operand:
                operator = value
                return

            if operator is not None and A is not None:
                try:
                    result = compute_expression(A, label["text"], operator)
                    formatted = remove_zero_decimal(result)
                    label["text"] = formatted
                    A = formatted
                except (ValueError, ZeroDivisionError):
                    show_error()
                    return
            else:
                A = label["text"]

            operator = value
            waiting_for_second_operand = True

    elif value in top_symbols:
        if value == "+/-":
            try:
                result = float(label["text"]) * -1
                label["text"] = remove_zero_decimal(result)
            except ValueError:
                show_error()
        elif value == "%":
            try:
                result = float(label["text"]) / 100
                label["text"] = remove_zero_decimal(result)
            except ValueError:
                show_error()

    elif value == "√":
        try:
            num = float(label["text"])
            if num < 0:
                show_error()
                return
            label["text"] = remove_zero_decimal(num ** 0.5)
            waiting_for_second_operand = True
        except ValueError:
            show_error()

    else:
        if value == ".":
            if waiting_for_second_operand or label["text"] == "Error":
                label["text"] = "0."
                waiting_for_second_operand = False
            elif "." not in label["text"]:
                label["text"] += value
        elif value in "0123456789":
            if waiting_for_second_operand or label["text"] in ("0", "Error"):
                label["text"] = value
                waiting_for_second_operand = False
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
