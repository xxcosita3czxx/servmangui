import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
    	# INIT of Self
        super().__init__()

		# Window config
        self.title("servmanGUI")
        self.geometry(f"{600}x{400}")
        self.resizable(False,False)

		# Frames
if __name__ == "__main__":
    app = App()
    app.mainloop()
