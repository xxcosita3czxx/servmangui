# TODO>> Network tab (Utils/test_ipfind_FINAL.py)
# TODO>> terminal ssh
import customtkinter as ctk
import os
import socket
import speedtest
import threading
import pywifi
import json



try: # The error handler
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
            ip = self.get_ip()
            subnet = ".".join(ip.split('.')[:-1])
            
            config_raw_r=json.load(open("config.json","r"))
            
            # Frames
            self.main_left = ctk.CTkFrame(self,width=200,height=400)
            self.main_tab = ctk.CTkTabview(self,width=400,height=400,fg_color="black")
            
            # Fonts
            self.main_left_curr_wifi_conn_font = ctk.CTkFont(family="Connection_font",size=20,weight="bold")
            self.Big_text = ctk.CTkFont(family="big_text",size=30,weight="bold")
            
            # Tabs
            self.main_tab.add("Home")
            self.main_tab.add("Network")
            self.main_tab.add("Control")
            self.main_tab.add("Remote Terminal")
            
            # Left Frame Info
            self.main_left_curr_wifi_conn = ctk.CTkLabel(self.main_left, text="Wait",width=200,text_color="white", font=self.main_left_curr_wifi_conn_font)
            self.main_left_curr_wifi_speed = ctk.CTkLabel(self.main_left, text="Speed: Wait")
            self.main_left_curr_wifi_LAN_ip = ctk.CTkLabel(self.main_left, text="IP: Wait")
            # Right Tabs
            
            ## Home Tab
            self.main_tab_Home_welcome_label = ctk.CTkLabel(self.main_tab.tab("Home"),text=f"Welcome, {os.getlogin()}",font=self.Big_text,width=387)
            self.main_tab_Home_about_text = ctk.CTkLabel(self.main_tab.tab("Home"),text=main_tab_Home_about_text_var,width=387)

            ## Network Tab
            self.main_tab_Network_refresh_button = ctk.CTkButton(self.main_tab.tab("Network"),text="refresh",width=387)
            # Grid Applying
            self.main_left.grid(row=0,column=0,sticky="n"+"w"+"s"+"e")
            self.main_left_curr_wifi_conn.grid(row=0,column=0,sticky="w"+"e"+"n")
            self.main_left_curr_wifi_speed.grid(row=1,column=0,sticky="w"+"e"+"n")
            self.main_left_curr_wifi_LAN_ip.grid(row=2,column=0)
            self.main_tab.grid(row=0,column=1,sticky="n"+"w"+"s"+"e")
            self.main_tab_Home_welcome_label.grid(row=0,column=0,sticky="n")
            self.main_tab_Home_about_text.grid(row=1,column=0,sticky="n")
            self.main_tab_Network_refresh_button.grid(row=0,column=0)

        # Logic
        
        ## Functions
        def get_ssid(self):
            wifi = pywifi.PyWiFi()
            iface = wifi.interfaces()[0]  # Assuming you have one WiFi interface
            ssid = iface.scan_results()[0].ssid
            return ssid
        def get_ip(self):
            try:
                # Create a socket to the Google DNS server (8.8.8.8)
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()
                return local_ip
            except socket.error:
                return None
        def truncate_float(self,float_number, decimal_places):
            multiplier = 10 ** decimal_places
            return int(float_number * multiplier) / multiplier
        def get_Up_Down(self):
            try:
                st = speedtest.Speedtest()
                download_speed = st.download()/1000000  # Convert to Mbps
                upload_speed = st.upload()/1000000  # Convert to Mbps
                return  "DOWN:"+str(self.truncate_float(download_speed,2)) +" // "+"UP:"+str(self.truncate_float(upload_speed,2))
            except:
                return "Disconnected"

        ## Updating Functions
        def main_left_update_ip(self):
            self.main_left_curr_wifi_LAN_ip.configure(text=f"IP: {self.get_ip()}")
            app.after(1000,self.main_left_update_ip)
        def main_left_update_ssid(self):
            self.main_left_curr_wifi_conn.configure(text=f"{self.get_ssid()}")
            app.after(1000,self.main_left_update_ssid)
        def main_left_update_speed(self):
            self.main_left_curr_wifi_speed.configure(text=self.get_Up_Down())
    if __name__ == "__main__":
        app = App()
        app.main_left_update_ip()
        app.main_left_update_ssid()
        speedthread = threading.Thread(target=app.main_left_update_speed)
        speedthread.setDaemon(True)
        speedthread.start()
        app.mainloop()

except PermissionError:
    print("Rerun with sudo/Administrator privs")
except KeyboardInterrupt:
    print("See you next time :3")