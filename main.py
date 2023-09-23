# TODO>> main logic of left frame
# TODO>> Welcome screen
# TODO>> IP/router Finder
# TODO>> terminal ssh
import customtkinter as ctk
import os
import socket
class App(ctk.CTk):
    def __init__(self):
    	# INIT of Self
        super().__init__()

		# Window config
        self.title("servmanGUI")
        self.geometry(f"{600}x{400}")
        self.resizable(False,False)
        # Variables
        main_tab_Home_about_text_var = """This tool uses ssh and internet connection to find every single
open port or responding IP that you want to find. 
Also it can find any router ip if you forgot.
        
        """
		# Frames
        main_left = ctk.CTkFrame(self,width=200,height=400)
        main_tab = ctk.CTkTabview(self,width=400,height=400,fg_color="black")
        
        # Fonts
        main_left_curr_wifi_conn_font = ctk.CTkFont(family="Connection_font",size=20,weight="bold")
        Big_text = ctk.CTkFont(family="big_text",size=30,weight="bold")
        
        # Tabs
        main_tab.add("Home")
        main_tab.add("Network")
        main_tab.add("Control")
        main_tab.add("Remote Terminal")
        
        # Left Frame Info
        main_left_curr_wifi_conn = ctk.CTkLabel(main_left, text="Disconnected",width=200,text_color="white", font=main_left_curr_wifi_conn_font)
        main_left_curr_wifi_speed = ctk.CTkLabel(main_left, text="Speed: Disconnected")
        main_left_curr_wifi_clients = ctk.CTkLabel(main_left, text="Clients: Disconnected")
        main_left_curr_wifi_LAN_ip = ctk.CTkLabel(main_left, text="IP: Disconnected")
        # Right Tabs
        
        ## Home Tab
        main_tab_Home_welcome_label = ctk.CTkLabel(main_tab.tab("Home"),text=f"Welcome, {os.getlogin()}",font=Big_text,width=387)
        main_tab_Home_about_text = ctk.CTkLabel(main_tab.tab("Home"),text=main_tab_Home_about_text_var,width=387)
        # Grid Applying
        main_left.grid(row=0,column=0,sticky="n"+"w"+"s"+"e")
        main_left_curr_wifi_conn.grid(row=0,column=0,sticky="w"+"e"+"n")
        main_left_curr_wifi_speed.grid(row=1,column=0,sticky="w"+"e"+"n")
        main_left_curr_wifi_clients.grid(row=2,column=0,sticky="w"+"e"+"n")
        main_left_curr_wifi_LAN_ip.grid(row=3,column=0)
        main_tab.grid(row=0,column=1,sticky="n"+"w"+"s"+"e")
        main_tab_Home_welcome_label.grid(row=0,column=0,sticky="n")
        main_tab_Home_about_text.grid(row=1,column=0,sticky="n")
                
        # Logic
        
        ## Functions
        def get_ip():
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                # doesn't even have to be reachable
                s.connect(('10.255.255.255', 1))
                IP = s.getsockname()[0]
            except:
                IP = '127.0.0.1'
            finally:
                s.close()
            return IP
        
if __name__ == "__main__":
    app = App()
    app.mainloop()

