from random import random
import tkinter as tk
from tkinter import Frame, Label, Button
from functools import partial

dig = True
flags = 0
first_click = True
game_board = []

def create_map(rows, columns, bombs, safety):
    list = []
    temp_row = []
    global flags            
    flags = bombs
    for i in range(0, rows):
        for i in range(0, columns):
            temp_row.append(" ")
        list.append(temp_row.copy())
        temp_row.clear()
    bomb_odds = bombs/(rows*columns)
    while bombs != 0:
        x = 0
        for row in list:
            y = 0
            for column in range(0, columns):
                indx = str(x) + str(y)
                if random() <= bomb_odds and row[column] != "X" and bombs != 0 and not(indx in safety):
                    row[column] = "X"
                    bombs -= 1
                y += 1
            x += 1
    current_row = 0
    for row in list:
        for column in range(0, columns):
            if row[column] != "X":
                row[column] = radial_check(list, current_row, column, "X")
                if isinstance(row[column], int):
                    row[column] = str(row[column])
        current_row += 1          
    return list


def radial_check(list, row, column, seek):
    count = 0
    for vert in range(-1, 2):
        if vert + row >= 0 and vert + row <= len(list) - 1:
            current_row = list[row + vert]
            for hor in range(-1, 2):
                if hor + column >= 0 and hor + column <= len(current_row) - 1:
                    if current_row[column + hor] == seek and not(hor == 0 and vert == 0):
                        count += 1
    
    if count != 0:
        return count
    else:
        return " "

def populate_main_window(frm_main, diff):
    columns = 0
    rows = 0
    bombs = 0
    global first_click
    first_click = True
    global game_board
    global dig
    dig = True
    if diff == "easy":
        columns = 9
        rows = 9
        bombs = 10
    elif diff == "medium":
        columns = 16
        rows = 16
        bombs = 40
    elif diff == "hard":
        columns = 30
        rows = 16
        bombs = 99

    for widget in frm_main.winfo_children():
        widget.destroy()
    difficulty_header = Frame(frm_main, bg= "#dddddd", pady= 1)
    difficulty_header.pack(fill="x")

    tools_header = Frame(frm_main, bg= "#dddddd", pady= 1)
    tools_header.pack(fill="x")

    game_header = Frame(frm_main, bg="#1eb328", pady= 1)
    game_header.pack(fill="x")

    button_board = {}
    button_board.clear()


    lbl_difficulty = Label(difficulty_header, text=f"Difficulty: {diff.title()}", bg= "#dddddd")

    lbl_tools = Label(tools_header, text="Current Tool: Dig", bg= "#dddddd")
    lbl_game_result = Label(tools_header, text="", bg= "#dddddd")

    btn_easy = Button(difficulty_header, text="Easy")
    btn_med = Button(difficulty_header, text="Medium")
    btn_hrd = Button(difficulty_header, text="Hard")

    btn_tools = Button(tools_header, text=f"Flag({bombs})")

    
    btn_easy.config(command= lambda: populate_main_window(frm_main, "easy"))
    btn_med.config(command= lambda: populate_main_window(frm_main, "medium"))
    btn_hrd.config(command= lambda: populate_main_window(frm_main, "hard"))

    def switch():
        global dig
        if dig == True:
            lbl_tools.config(text=f"Current Tool: Flag({flags})")
            btn_tools.config(text="Dig")
            dig = False
        elif dig == False:
            lbl_tools.config(text="Current Tool: Dig")
            btn_tools.config(text=f"Flag({flags})")
            dig = True

    def reveal(x, y):
        global first_click
        global game_board
        if first_click == True:
            safe =[]
            for safex in range(-1,2):
                for safey in range(-1,2):
                    if safex + x >= 0 and safey + y >= 0:
                        safe.append(f"{safex + x}{safey + y}")
            game_board = create_map(rows, columns, bombs, safe)
            first_click = False
            btn_tools.config(state="normal")
        row = game_board[x]
        global flags
        btn = button_board[f"{x}-{y}"]
        if btn.cget("text") == "" and dig == True:
            if row[y] == "X":
                btn.config(text = "M", font=("Wingdings", 6), bg= "#aeafb0", height = 2)
            else:
                btn.config(text = f"{row[y]}", bg= "#aeafb0")
            if row[y] == " ":
                for vert in range(-1, 2):
                    if vert + x >= 0 and vert + x <= len(game_board) - 1:
                        current_row = game_board[x + vert]
                        for hor in range(-1, 2):
                            if hor + y >= 0 and hor + y <= len(current_row) - 1:
                                if not(hor == 0 and vert == 0):
                                    reveal(x+vert, y+hor)
        elif (btn.cget("text") == "" and dig == False) and flags !=0:
            btn.config(text = "F", bg= "red")
            flags -= 1
            lbl_tools.config(text=f"Current Tool: Flag({flags})")
        elif btn.cget("text") == "F" and dig == False:
            btn.config(text = "", bg = "#024715")
            flags += 1
            lbl_tools.config(text=f"Current Tool: Flag({flags})")
        game_over_check(btn.cget("text"), button_board, lbl_game_result)


    btn_tools.config(command = switch)

    lbl_difficulty.pack(side="left")
    btn_easy.pack(side="left", padx= 1)
    btn_med.pack(side="left", padx= 1)
    btn_hrd.pack(side="left", padx= 1)


    lbl_tools.pack(side="left")
    btn_tools.pack(side="left")
    btn_tools.config(state= "disabled")
    lbl_game_result.pack(side="right")
    


    for r in range(rows):
        for c in range(columns):
            btn_space = Button(game_header, text=f"", bg= "#024715", width=2, height=1)
            btn_space.grid(row=r, column= c, padx=1, pady=1)
            btn_space.config(command= partial(reveal, r, c))
            button_board[f"{r}-{c}"] = btn_space


def game_over_check(content, button_board, label):
    if content == "M":
        end_game(button_board)
        label.config(text="You Lose", fg="red")
    else:
        count = 0
        for btn in button_board.values():
            if btn.cget("text") == "":
                count += 1
                break
        if count == 0:
            end_game(button_board)
            label.config(text="You Win!", fg="green")

def end_game(button_board):
    for btn in button_board.values():
        btn.config(state="disabled")

def main():
    root = tk.Tk()
    root.config(bg="#1eb328")

    # Create the main window.
    frm_main = Frame(root)
    frm_main.master.title("Minesweeper")
    frm_main.pack(padx=4, pady=3, fill=tk.BOTH, expand=1)

    # Call the populate_main_window function, which will add
    # labels, text entry boxes, and buttons to the main window.
    populate_main_window(frm_main, "easy")

    # Start the tkinter loop that processes user events
    # such as key presses and mouse button clicks.
    root.mainloop()

if __name__ == "__main__":
    main()