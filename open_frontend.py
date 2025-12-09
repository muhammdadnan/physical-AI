import webbrowser
import time

# URL of the Docusaurus frontend
url = "http://localhost:3000/ai-native-book/"

print("Opening the frontend in your browser...")
print(f"URL: {url}")

# Wait a moment to ensure the server is fully ready
time.sleep(2)

# Open the URL in the default browser
webbrowser.open(url)

print("Frontend opened successfully!")