import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from falconpy import Hosts, IOC
from ttkthemes import ThemedStyle
import json
import csv

# Initialize Tkinter
root = tk.Tk()
root.title("CrowdStrike Host Details and IOC Creation")
root.geometry("1100x600")
root.resizable(width=False, height=False)

style = ThemedStyle(root)
style.set_theme("clearlooks")

# FalconPy client for host details
hosts = Hosts(
    creds={
        "client_id": "replace",
        "client_secret": "replace",
    },
    base_url="https://api.us-2.crowdstrike.com",
)


# FalconPy client for IOC creation
def connect_api(creds: dict):
    falcon_api = IOC(creds=creds, base_url="https://api.us-2.crowdstrike.com")
    return falcon_api


# Function to fetch and display host details
def fetch_host_details():
    SEARCH_FILTER = search_entry.get()

    # Split the input into a list of hostnames
    hostnames = SEARCH_FILTER.split(",")

    # Clear previous results
    for item in results_tree.get_children():
        results_tree.delete(item)

    # Retrieve and display details for each hostname
    for hostname in hostnames:
        hostname = hostname.strip()  # Remove leading/trailing whitespace
        if hostname:
            # Retrieve a list of hosts that have hostnames matching the filter
            hosts_search_result = hosts.query_devices_by_filter(
                filter=f"hostname:'{hostname}'"
            )

            # Check for success or error in the API response
            if hosts_search_result["status_code"] == 200:
                hosts_found = hosts_search_result["body"]["resources"]
                if hosts_found:
                    for host_id in hosts_found:
                        # Retrieve the details for each match
                        host_detail = hosts.get_device_details(ids=[host_id])["body"][
                            "resources"
                        ][0]

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
                        results_tree.insert(
                            "",
                            "end",
                            values=(
                                hostname,
                                aid,
                                os_version,
                                local_ip,
                                system_manufacturer,
                                system_product_name,
                                machine_domain,
                                status,
                                last_seen,
                            ),
                        )
                else:
                    results_tree.insert(
                        "",
                        "end",
                        values=(
                            f"No hosts found for {hostname}",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                        ),
                    )
            else:
                error_detail = hosts_search_result["body"]["errors"]
                for error in error_detail:
                    error_code = error["code"]
                    error_message = error["message"]
                    results_tree.insert(
                        "",
                        "end",
                        values=(
                            f"[Error {error_code}]",
                            error_message,
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                        ),
                    )


# Function to convert CSV to JSON
def csv_to_json(csv_file):
    json_data = []
    with open(csv_file, "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            json_data.append(row)
    return json_data


# Function to run the Falcon script to add IOCs
def run_falcon_script():
    if not indicator_file:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Please select a JSON or CSV file.")
        return

    try:
        if indicator_file.lower().endswith(".json"):
            with open(indicator_file, "r") as file:
                indicator_data = json.load(file)
        elif indicator_file.lower().endswith(".csv"):
            indicator_data = csv_to_json(indicator_file)
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(
                tk.END, "Unsupported file format. Please select a JSON or CSV file."
            )
            return

    except Exception as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Error loading IOC data: " + str(e))
        return

    falcon = connect_api(
        {
            "client_id": "442e875bdf584df8abc4d6f7e119bb75",
            "client_secret": "MGKV2J16IClDR3ui8q507o4pLHceZznNQy9Fxasf",
        }
    )

    if isinstance(indicator_data, list):
        for entry in indicator_data:
            indicator_entry = {
                "source": entry.get("source", ""),
                "action": entry.get("action", ""),
                "expiration": entry.get("expiration", ""),
                "description": entry.get("description", ""),
                "type": entry.get("type", ""),
                "value": entry.get("value", ""),
                "platforms": entry.get("platforms", ""),
                "severity": entry.get("severity", ""),
                "applied_globally": entry.get("applied_globally", ""),
            }

            response = falcon.indicator_create(**indicator_entry)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, json.dumps(response, indent=2))
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Invalid IOC data format.")


# Function to browse and select a JSON or CSV file
def browse_json_file():
    global indicator_file
    indicator_file = filedialog.askopenfilename(
        filetypes=[("JSON Files", "*.json"), ("CSV Files", "*.csv")]
    )
    if indicator_file:
        selected_file_label.config(text="Selected File: " + indicator_file)
    else:
        selected_file_label.config(text="No file selected")


# Create a frame for host details
host_details_frame = ttk.LabelFrame(root, text="Host Details")
host_details_frame.pack(padx=20, pady=20, fill="both", expand="yes")

# Create labels and entries for entering hostnames or IP addresses
search_label = ttk.Label(
    host_details_frame,
    text="Enter Hostnames or IP Addresses (comma-separated):",
    font=("Calibri", 12),
)
search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
search_entry = ttk.Entry(host_details_frame, font=("Calibri", 12))
search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Create a search button to fetch host details
search_button = ttk.Button(
    host_details_frame, text="Search", command=fetch_host_details, style="TButton"
)
search_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

# Create a results table for host details
results_tree = ttk.Treeview(
    host_details_frame,
    columns=(
        "Hostname",
        "AID",
        "OS Version",
        "Local IP",
        "System Manufacturer",
        "System Product",
        "Domain",
        "Status",
        "Last Seen",
    ),
    show="headings",
)
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
results_tree.column("#9", width=200)
results_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Create a frame for JSON/CSV file handling
json_frame = ttk.LabelFrame(root, text="JSON/CSV File Handling")
json_frame.pack(padx=20, pady=20, fill="both", expand="yes")

# Create a label for selecting a JSON or CSV file
json_label = ttk.Label(
    json_frame, text="Select JSON or CSV File:", font=("Calibri", 12)
)
json_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Create a button to browse and select a JSON or CSV file
select_file_button = ttk.Button(
    json_frame, text="Browse", command=browse_json_file, style="TButton"
)
select_file_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Label to display the selected JSON or CSV file
selected_file_label = ttk.Label(
    json_frame, text="No file selected", font=("Calibri", 12)
)
selected_file_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

# Create a button to run the Falcon script
run_script_button = ttk.Button(
    json_frame, text="Click to Add IOCs", command=run_falcon_script, style="TButton"
)
run_script_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")

# Create a text box to display the Falcon script results
result_text = tk.Text(root, wrap=tk.WORD, width=60, height=10)
result_text.pack(padx=20, pady=10, fill="both", expand="yes")

# Start the Tkinter main loop
root.mainloop()
