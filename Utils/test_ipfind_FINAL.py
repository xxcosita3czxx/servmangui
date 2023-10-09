import platform
import subprocess
import threading
import netifaces

def check_ip_existence(ip, result_list):
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

def scan_lan_ips(subnet, num_threads=4,start_ip = 1,end_ip = 255):
    # Create a list to store results
    if end_ip - start_ip + 1 < num_threads:
        raise ValueError("Must be same or less threads than checked ip adresses")
    result_list = []

    # Calculate the number of IPs each thread should check
    ips_per_thread = (end_ip - start_ip + 1) // num_threads

    # Create and start threads
    threads = []
    for i in range(num_threads):
        start = start_ip + i * ips_per_thread
        end = start + ips_per_thread - 1
        thread = threading.Thread(target=check_ip_range, args=(subnet, start, end, result_list))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return result_list

def check_ip_range(subnet, start, end, result_list):
    for i in range(start, end + 1):
        ip = subnet + "." + str(i)
        check_ip_existence(ip, result_list)

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
if __name__ == "__main__":
    # Example usage:

    lan_ips = scan_lan_ips(subnet,num_threads=255,start_ip=1,end_ip=255)

    router_gateway_ip = get_router_gateway_ip()
