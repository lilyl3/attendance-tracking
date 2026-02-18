# Tracking Attendance

## Getting Started

### 1. Create a Virtual Environment
```bash
python3 -m venv att
```
### 2. Activte the Virtual Environment
On MacOS
```bash
source att/bin/activate
```
On Windows
```bash
att\Scripts\Activate
```
### 3. Install Dependencies
- All required packages are listed in: `requirements.txt`
```bash
pip install -r requirements.txt  
```
### 4. Run the application
```bash
streamlit run app.py
```
After running the command, you should see output similar to:
```
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```
- To access the app from a device connected on the same network, connect using the Network URL
- For Windows users, to enable network access
    - Open `Settings`
    - Go to `Network & Internet`
    - Select `Wi-Fi`
    - Click your connected network
    - Set the network profile to `Private`
---

## Importing Members

You can add members to the database using a `.csv` file containing `english_name` and `chinese_name` columns.

### CSV Format Example
```csv
english_name,chinese_name
John Smith,史密斯
Jane Doe,简多
```

### How to Run

Make sure your virtual environment is activated, then run:
```bash
python3 data_entry.py path/to/your_file.csv
```

