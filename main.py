##############################################################################################
#                                # Server Manager GUI #                                      #
##############################################################################################
# TODO's for myself ->>
#
# TODO>> Add popups on every network button
# TODO>> terminal ssh
# TODO>> FREE SPOT
#
##############################################################################################

import customtkinter as ctk
import os
import socket
import speedtest
import pywifi
import json
import platform
import subprocess
import threading
import netifaces
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
        
            self.ip = self.get_ip()
            self.subnet = ".".join(self.ip.split('.')[:-1])
            
            config_raw_r=json.load(open("config.json","r"))
            self.num_threads = config_raw_r["num_threads"]
            self.ip_start = config_raw_r["start_ip"]
            self.ip_end = config_raw_r["end_ip"]
            self.ip_buttons_ids = []
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
            self.main_tab_Network_refresh_button = ctk.CTkButton(self.main_tab.tab("Network"),text="refresh",width=387,command=self.refresh_button_middleman)
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
            
            except Exception as e:
                print(f"EXCEPTION OCCURED: {e} , Contact me ASAP!")
                return "Disconnected"

        def check_ip_existence(self,ip, result_list):
            try:
                # Use the 'ping' command on Linux or Windows to check if the IP exists
                if platform.system() == "Linux":
                    print(f"checking {ip}")
                    output = subprocess.check_output(["ping", "-c", "1", ip], stderr=subprocess.STDOUT, text=True)
                    if "1 packets transmitted," in output and "0 received" not in output:
                        result_list.append(ip)
                        print(f"Checked IP: {ip}")
                elif platform.system() == "Windows":
                    output = subprocess.check_output(["ping", "-n", "1", ip], stderr=subprocess.STDOUT, text=True)
                    if "Received = 1" in output:
                        result_list.append(ip)
                        print(f"Checked IP: {ip}")
            except subprocess.CalledProcessError as e:
                pass
            except Exception as e:
                print(f"Error checking IP {ip}: {e}")

        def scan_lan_ips(self,subnet, num_threads=4,start_ip = 1,end_ip = 255):
            # Create a list to store results
            if end_ip - start_ip + 1 < num_threads:
                raise ValueError("Must be same or less threads than checked ip adresses")
            result_list = []

            # Calculate the number of IPs each thread should check
            ips_per_thread = (end_ip - start_ip + 1) // num_threads

            # Create and start threads
            try:
                threads = []
                for i in range(num_threads):
                    start = start_ip + i * ips_per_thread
                    end = start + ips_per_thread - 1
                    thread = threading.Thread(target=self.check_ip_range, args=(subnet, start, end, result_list))
                    thread.start()
                    threads.append(thread)

                # Wait for all threads to finish
                for thread in threads:
                    thread.join()

                return result_list
            except KeyboardInterrupt:
                print("DO NOT INTERRUPT THE THREADS")
            except Exception as e:
                print("Whoops, we got an exception: "+e)
        def check_ip_range(self,subnet, start, end, result_list):
            for i in range(start, end + 1):
                ip = subnet + "." + str(i)
                self.check_ip_existence(ip, result_list)

        def update_network_list(self,window,button_labels):
            for button in self.ip_buttons_ids:
                button.destroy()
            self.ip_buttons_ids.clear()
            for i, label in enumerate(button_labels):
                button = ctk.CTkButton(window, text=label,anchor="w",width=387,fg_color="gray")
                button.grid(row=i+1, column=0,sticky="w")
                self.ip_buttons_ids.append(button)
                
        def get_router_gateway_ip():
            try:
                # Get the default gateway's IP address (cross-platform)
                gateways = netifaces.gateways()
                if 'default' in gateways and netifaces.AF_INET in gateways['default']:
                    return gateways['default'][netifaces.AF_INET][0]
                return None
            except Exception as e:
                print(f"Error getting router gateway IP: {e}")
                return None
        def refresh_button_middleman(self):
            try:
                self.update_network_list(self.main_tab.tab("Network"),self.scan_lan_ips(subnet=self.subnet,num_threads=self.num_threads,start_ip=self.ip_start,end_ip=self.ip_end))
            except Exception as e:
                print(f"whoops? {e}")
        
        ## Updating Functions
        def main_left_update_ip(self):
            self.main_left_curr_wifi_LAN_ip.configure(text=f"IP: {self.ip}")
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
except Exception as e:
    print(f"Whoops, you got an main thread error: {e}")