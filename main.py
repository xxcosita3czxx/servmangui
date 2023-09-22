import customtkinter as ctk
class App(ctk.CTk):
    def __init__(self):
    	# INIT of Self
        super().__init__()

		# Window config
        self.title("servmanGUI")
        self.geometry(f"{600}x{400}")
        # self.resizable(False,False)

		# Frames
        main_left = ctk.CTkFrame(self,width=200,height=400)
        main_tab = ctk.CTkTabview(self,width=400,height=400,fg_color="black")
        
        # Tabs
        main_tab.add("Home")
        main_tab.add("Network")
        main_tab.add("Control")
        main_tab.add("Remote Terminal")
        
        # Left Frame Info
        main_left_curr_wifi_conn = ctk.CTkLabel(main_left, text="Disconnected")
        main_left_curr_wifi_speed = ctk.CTkLabel(main_left, text="Speed: Disconnected")
        main_left_curr_wifi_clients = ctk.CTkLabel(main_left, text="Clients: Disconnected")

        # Right Tabs
        
        ## Home Tab
        main_tab_welcome_label = ctk.CTkLabel(main_tab.tab("Home"),text="Welcome user")
        # Grid Applying
        main_left.grid(row=0,column=0,sticky="n"+"w"+"s"+"e")
        main_left_curr_wifi_conn.grid(row=0,column=0,sticky="w"+"e"+"n")
        main_left_curr_wifi_speed.grid(row=1,column=0,sticky="w"+"e"+"n")
        main_left_curr_wifi_clients.grid(row=2,column=0,sticky="w"+"e"+"n")
        main_tab.grid(row=0,column=1,sticky="n"+"w"+"s"+"e")
        main_tab_welcome_label.grid(row=0,column=0)
        # Logic
        
if __name__ == "__main__":
    app = App()
    app.mainloop()

