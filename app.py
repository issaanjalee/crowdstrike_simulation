import tkinter as tk
from tkinter import ttk
from falconpy import Hosts
from ttkthemes import ThemedStyle

# Initialize Tkinter
root = tk.Tk()
root.title("CrowdStrike Host Details")
root.geometry("950x500")  # Set window size
root.resizable(width=False, height=False)  # Make the window non-resizable

# Apply a themed style to the window
style = ThemedStyle(root)
style.set_theme("black")

# Create a function to fetch and display host details
def fetch_host_details():
    SEARCH_FILTER = search_entry.get()

    # Split the input into a list of hostnames
    hostnames = SEARCH_FILTER.split(',')

    # Clear previous results
    for item in results_tree.get_children():
        results_tree.delete(item)

    # Retrieve and display details for each hostname
    for hostname in hostnames:
        hostname = hostname.strip()  # Remove leading/trailing whitespace
        if hostname:
            # Retrieve a list of hosts that have hostnames matching the filter
            hosts_search_result = hosts.query_devices_by_filter(filter=f"hostname:'{hostname}'")

            # Check for success or error in the API response
            if hosts_search_result["status_code"] == 200:
                hosts_found = hosts_search_result["body"]["resources"]
                if hosts_found:
                    for host_id in hosts_found:
                        # Retrieve the details for each match
                        host_detail = hosts.get_device_details(ids=[host_id])["body"]["resources"][0]

                        # Extract relevant details
                        hostname = host_detail["hostname"]
                        aid = host_detail["device_id"]
                        os_version = host_detail["os_version"]
                        local_ip = host_detail["local_ip"]
                        system_manufacturer = host_detail["system_manufacturer"]
                        system_product_name = host_detail["system_product_name"]
                        machine_domain = host_detail["machine_domain"]
                        status = host_detail["status"]
                        last_seen = host_detail["last_seen"]

                        # Insert the details into the results tree
                        results_tree.insert("", "end", values=(hostname, aid, os_version, local_ip,
                                                              system_manufacturer, system_product_name,
                                                              machine_domain, status, last_seen))
                else:
                    results_tree.insert("", "end", values=(f"No hosts found for {hostname}", "", "", "", "", "", "", "", ""))
            else:
                error_detail = hosts_search_result["body"]["errors"]
                for error in error_detail:
                    error_code = error["code"]
                    error_message = error["message"]
                    results_tree.insert("", "end", values=(f"[Error {error_code}]", error_message, "", "", "", "", "", "", ""))

# Create and configure widgets
search_label = tk.Label(root, text="Enter Hostnames (comma-separated):", font=("Calibri", 12), bg="grey", fg="white")
search_entry = tk.Entry(root, font=("Calibri", 12))
search_button = tk.Button(root, text="Search", command=fetch_host_details, relief=tk.RIDGE, bd=3, width=10)
search_button.configure(font=("Calibri", 12))

# Place widgets in the window
search_label.pack(padx=10, pady=10, fill=tk.BOTH)
search_entry.pack(padx=10, pady=10, fill=tk.BOTH)
search_button.pack(padx=10, pady=10)

# Set up FalconPy client
hosts = Hosts(creds={
    'client_id': "442e875bdf584df8abc4d6f7e119bb75",
    'client_secret': "MGKV2J16IClDR3ui8q507o4pLHceZznNQy9Fxasf"
}, base_url="https://api.us-2.crowdstrike.com")

# Create a results table using Treeview
results_tree = ttk.Treeview(root, columns=("Hostname", "AID", "OS Version", "Local IP", "System Manufacturer", "System Product",
                                           "Domain", "Status", "Last Seen"), show="headings")
results_tree.heading("#1", text="Hostname")
results_tree.heading("#2", text="AID")
results_tree.heading("#3", text="OS Version")
results_tree.heading("#4", text="Local IP")
results_tree.heading("#5", text="System Manufacturer")
results_tree.heading("#6", text="System Product")
results_tree.heading("#7", text="Domain")
results_tree.heading("#8", text="Status")
results_tree.heading("#9", text="Last Seen")
results_tree.column("#1", width=100)
results_tree.column("#2", width=100)
results_tree.column("#3", width=100)
results_tree.column("#4", width=100)
results_tree.column("#5", width=120)
results_tree.column("#6", width=120)
results_tree.column("#7", width=100)
results_tree.column("#8", width=100)
results_tree.column("#9", width=150)
results_tree.pack(padx=10, pady=10, expand=True)

# Start the Tkinter main loop
root.mainloop()
