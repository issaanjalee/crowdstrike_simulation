# README

## CrowdStrike Host Details and IOC Creation Tool

This tool provides a graphical user interface (GUI) for fetching host details and creating Indicators of Compromise (IOC) using the CrowdStrike Falcon API. It leverages the Tkinter library for the GUI, FalconPy for API interactions, and supports JSON/CSV file handling.

### Features

- **Fetch Host Details:** Enter hostnames or IP addresses to retrieve detailed information from the CrowdStrike Falcon API.
- **Create IOCs:** Select a JSON or CSV file containing IOC data and add them to CrowdStrike using the Falcon API.

### Prerequisites

- Python 3.x
- Tkinter
- FalconPy
- ttkthemes
- json
- csv

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/issaanjalee/crowdstrike_simulation.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd crowdstrike-tool
   ```
3. **Install the required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Before running the tool, ensure you have valid CrowdStrike API credentials. Update the `client_id` and `client_secret` in the code:

```python
hosts = Hosts(
    creds={
        "client_id": "your_client_id",
        "client_secret": "your_client_secret",
    },
    base_url="https://api.us-2.crowdstrike.com",
)
```

### Usage

1. **Run the script:**
   ```bash
   python main.py
   ```
2. **Fetch Host Details:**
   - Enter hostnames or IP addresses (comma-separated) in the input field.
   - Click the "Search" button to retrieve and display host details.
3. **Create IOCs:**
   - Click the "Browse" button to select a JSON or CSV file containing IOC data.
   - Click the "Click to Add IOCs" button to process the file and add IOCs to CrowdStrike.

### GUI Components

- **Host Details Frame:**
  - Input field for entering hostnames or IP addresses.
  - "Search" button to fetch and display host details.
  - Results table to display host information.
- **JSON/CSV File Handling Frame:**
  - "Browse" button to select a JSON or CSV file.
  - Label to display the selected file name.
  - "Click to Add IOCs" button to add IOCs from the selected file.
- **Results Text Box:**
  - Displays the results or errors from IOC creation.

### File Structure

```
crowdstrike-tool/
│
├── main.py           # Main script file
├── requirements.txt  # List of required Python packages
├── README.md         # This README file
└── LICENSE           # License file
```

### Requirements

- Tkinter: `pip install tk`
- FalconPy: `pip install crowdstrike-falconpy`
- ttkthemes: `pip install ttkthemes`

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Acknowledgements

- [CrowdStrike Falcon API](https://www.crowdstrike.com/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [FalconPy](https://github.com/CrowdStrike/falconpy)
- [ttkthemes](https://github.com/RedFantom/ttkthemes)

