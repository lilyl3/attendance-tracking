import yaml
import subprocess
from yaml.loader import SafeLoader
from pyngrok import ngrok

# Load config
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Set ngrok token
ngrok.set_auth_token(config["ngrok"]["auth_token"])

# Start Streamlit
subprocess.Popen(["streamlit", "run", "app.py"])

# Open tunnel
public_url = ngrok.connect(8501)
print("Public URL:", public_url)