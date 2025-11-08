import tkinter as tk
from ttkbootstrap import ttk, Style

STYLE = "darkly"

def main():
    root = tk.Tk()
    style = Style(theme=STYLE)

    root.title("Tic Tac Toe (NumPad Layout — empty buttons)")
    root.geometry("320x380")
    root.resizable(False, False)

    current_player = tk.StringVar(value="X")
    board = [[None for _ in range(3)] for _ in range(3)]
    buttons = [[None for _ in range(3)] for _ in range(3)]
    game_active = {"val": True}

    status = ttk.Label(root, text="X's turn", font=("Helvetica", 14))
    status.pack(pady=8)

    frame = ttk.Frame(root)
    frame.pack()

    style.configure("TicTacToe.TButton", font=("Helvetica", 20, "bold"), padding=10)

    key_to_pos = {
        "7": (0, 0), "8": (0, 1), "9": (0, 2),
        "4": (1, 0), "5": (1, 1), "6": (1, 2),
        "1": (2, 0), "2": (2, 1), "3": (2, 2),
        "KP_7": (0, 0), "KP_8": (0, 1), "KP_9": (0, 2),
        "KP_4": (1, 0), "KP_5": (1, 1), "KP_6": (1, 2),
        "KP_1": (2, 0), "KP_2": (2, 1), "KP_3": (2, 2),
    }

    def check_win():
        lines = [
            [(i, 0), (i, 1), (i, 2)] for i in range(3)
        ] + [
            [(0, i), (1, i), (2, i)] for i in range(3)
        ] + [
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]
        ]
        for line in lines:
            (a, b, c) = line
            v1, v2, v3 = board[a[0]][a[1]], board[b[0]][b[1]], board[c[0]][c[1]]
            if v1 and v1 == v2 == v3:
                return v1, line
        if all(board[r][c] for r in range(3) for c in range(3)):
            return "Draw", None
        return None, None

    def on_click(r, c):
        if not game_active["val"] or board[r][c]:
            return
        player = current_player.get()
        board[r][c] = player
        buttons[r][c].config(text=player, bootstyle=("primary" if player == "X" else "danger"))

        winner, line = check_win()
        if winner:
            if winner == "Draw":
                status.config(text="Draw!")
            else:
                status.config(text=f"{winner} wins!")
                for (rr, cc) in line:
                    buttons[rr][cc].config(bootstyle="success")
            game_active["val"] = False
            return

        nextp = "O" if player == "X" else "X"
        current_player.set(nextp)
        status.config(text=f"{nextp}'s turn")

    for r in range(3):
        for c in range(3):
            b = ttk.Button(
                frame,
                text="",
                width=6,
                style="TicTacToe.TButton",
                bootstyle="secondary",
                command=lambda r=r, c=c: on_click(r, c),
            )
            b.grid(row=r, column=c, padx=6, pady=6)
            buttons[r][c] = b

    def reset():
        for r in range(3):
            for c in range(3):
                board[r][c] = None
                buttons[r][c].config(text="", bootstyle="secondary")
        current_player.set("X")
        status.config(text="X's turn")
        game_active["val"] = True

    controls = ttk.Frame(root)
    controls.pack(pady=10)
    reset_btn = ttk.Button(controls, text="Restart", bootstyle="info", command=reset)
    reset_btn.pack()

    def on_key(event):
        key = event.keysym
        if key == "0" or key == "KP_0":
            reset()
            return
        if key in key_to_pos:
            r, c = key_to_pos[key]
            on_click(r, c)
            return
        ch = event.char
        if ch and ch in key_to_pos:
            r, c = key_to_pos[ch]
            on_click(r, c)

    root.bind("<Key>", on_key)

    root.mainloop()


if __name__ == "__main__":
    main()
