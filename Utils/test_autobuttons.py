import tkinter as tk

# Your list of strings inside square brackets
button_labels = ["Button 1", "Button 2", "Button 3"]

# Create a tkinter window
window = tk.Tk()

# Create an empty list to store the buttons
buttons = []

# Create buttons based on the strings and place them using grid
for i, label in enumerate(button_labels):
    button = tk.Button(window, text=label)
    button.grid(row=i, column=0)
    buttons.append(button)  # Add the button to the list
print(buttons)
# Start the tkinter main loop
window.mainloop()