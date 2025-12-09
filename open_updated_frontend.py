import webbrowser
import time

# URL of the Docusaurus frontend with the new banner
url = "http://localhost:3001/ai-native-book/"

print("Opening the updated frontend with improved banner in your browser...")
print(f"URL: {url}")

# Wait a moment to ensure the server is fully ready
time.sleep(2)

# Open the URL in the default browser
webbrowser.open(url)

print("Updated frontend with enhanced banner opened successfully!")