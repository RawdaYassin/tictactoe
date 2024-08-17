import tkinter as tk

def on_alg_button_click(algorithm):
    # Open the algorithm page based on the selected algorithm
    if algorithm == "MiniMax":
        open_MiniMax_page()
    elif algorithm == "MiniMax-Alpha-Beta":
        open_MiniMax_Alpha_Beta_page()
    elif algorithm == "MiniMax-Hauristic-Basic":
        open_MiniMax_Hauristic_Basic_page()
    elif algorithm == "MiniMax-Hauristic-Advanced":
        open_MiniMax_Hauristic_Advanced_page()


def open_MiniMax_page():
    root.destroy()
    import minimax

def  open_MiniMax_Alpha_Beta_page():
    root.destroy()
    import minimax_alpha_beta

def open_MiniMax_Hauristic_Basic_page():
    root.destroy()
    import minimax_hauristic_basic

def open_MiniMax_Hauristic_Advanced_page():
    root.destroy()
    import minimax_hauristic_advanced

root = tk.Tk()
root.title("Tic-Tac-Toe Game")

# Create a frame for the algorithm selection
frame = tk.Frame(root)
frame.pack(pady=20)

# Create a label for instructions
label = tk.Label(frame, text="Choose an algorithm to solve the Tic-Tac-Toe problem:", font=("Arial", 14))
label.pack(pady=10)

# Create algorithm buttons
alg_buttons = [
    ("MiniMax",open_MiniMax_page),
    ("MiniMax-Alpha-Beta",  open_MiniMax_Alpha_Beta_page),
    ("MiniMax-Hauristic-Basic",open_MiniMax_Hauristic_Basic_page),
    ("MiniMax-Hauristic-Advanced", open_MiniMax_Hauristic_Advanced_page)
]

for alg_name, alg_func in alg_buttons:
    button = tk.Button(frame, text=alg_name, font=("Arial", 12), width=25, height=2, command=lambda alg=alg_name: on_alg_button_click(alg))
    button.pack(pady=5)

root.mainloop()