import tkinter as tk
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
    root.title("Tic-Tac-Toe Game")

    # Create a frame for the algorithm selection
    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Create a label for instructions
    label = tk.Label(frame, text="Choose an algorithm to solve the Tic-Tac-Toe problem:", font=("Arial", 14))
    label.pack(pady=10)

    # Create algorithm buttons
    alg_buttons = [
        ("MiniMax", "minimax"),
        ("MiniMax Alpha Beta", "minimax_alpha_beta"),
        ("MiniMax First Heuristic", "minimax_heuristic_basic"),
        ("MiniMax Second Heuristic", "minimax_heuristic_advanced")
    ]

    for alg_name, alg_value in alg_buttons:
        button = tk.Button(frame, text=alg_name, font=("Arial", 12), width=25, height=2, command=lambda alg=alg_value: on_alg_button_click(alg))
        button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_algorithm_selection_window()
