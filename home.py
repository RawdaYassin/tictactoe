import tkinter as tk
from tkinter import ttk
import util

# Global variable to store the selected algorithm
selected_algorithm = None

def on_alg_button_click(algorithm):
    global selected_algorithm
    selected_algorithm = algorithm
    root.destroy()  # Close the selection window
    util.main(selected_algorithm)  # Pass the selected algorithm to the main function

def create_algorithm_selection_window():
    global root
    root = tk.Tk()
    root.title("Tic-Tac-Toe AI Selector")
    root.geometry("300x300")  # Set window size
    root.configure(bg="#f0f0f0")  # Set background color

    # Create a frame for the algorithm selection
    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Create a label for instructions
    label = tk.Label(frame, text=f"Choose an algorithm to solve \nthe Tic-Tac-Toe problem", font=("Helvetica", 14, "bold"), bg="#f0f0f0", fg="#333")
    label.pack(pady=20)

    # Create a style for buttons
    style = ttk.Style()
    style.configure("TButton",
                    font=("Helvetica", 12),
                    padding=5,
                    relief="flat",
                    background="#007bff",
                    foreground="black")
    style.map("TButton",
              background=[('pressed', '#0056b3'), ('active', '#0069d9')],
              foreground=[('pressed', 'black'), ('active', 'black')])

    # Create algorithm buttons
    alg_buttons = [
        ("MiniMax", "minimax"),
        ("MiniMax Alpha Beta", "minimax_alpha_beta"),
        ("MiniMax First Heuristic", "minimax_heuristic_basic"),
        ("MiniMax Second Heuristic", "minimax_heuristic_advanced")
    ]

    for alg_name, alg_value in alg_buttons:
        button = ttk.Button(frame, text=alg_name, command=lambda alg=alg_value: on_alg_button_click(alg))
        button.pack(pady=5, fill=tk.X, padx=10)

    root.mainloop()

if __name__ == "__main__":
    create_algorithm_selection_window()
