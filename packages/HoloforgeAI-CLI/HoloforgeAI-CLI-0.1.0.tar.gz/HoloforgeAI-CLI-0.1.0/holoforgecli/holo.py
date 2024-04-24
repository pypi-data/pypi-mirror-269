import os
import sys
import shlex
from configparser import ConfigParser
import boto3
import requests
import json
import holoforgecli.ascii as ascii
import subprocess
import glob
import time
import asyncio

# ASCII Art frames
frames_as = [
    "*      > -    *",
    " *     >  -  *",
    "  *    >   -*",
    "   *   >    x",
    "    * -<    ",
    "     x <    ",
    "       v\n\n\n\n\n       *",
    "       v\n\n\n\n       *",
    "       v\n       |\n\n       *",
    "       v\n\n       |\n       *",
    "       v\n        \n       x",
    "       v",
    "HIGH SCORE"
]

frames_pm = [
    "(<-------Q",
    " (<------Q",
    "  (<-----Q",
    "   (<----Q",
    "    (<---Q",
    "     (<--Q",
    "      (<-Q",
    "       (<Q",
    "        (<",
    "Q------->)",
    "Q------>)",
    "Q----->)",
    "Q---->)",
    "Q--->)",
    "Q-->)",
    "Q->)",
    "Q>)",
    ">)",
]

def clear_screen():
    """Clears the console screen."""
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Mac and Linux
    else:
        os.system('clear')

def animate(frames, repeat=5, speed=0.5):
    """Animates the given frames."""
    for _ in range(repeat):
        for frame in frames:
            clear_screen()
            print(frame)
            time.sleep(speed)

cognito_client_id = '7cfvd1bg71hbecba3ddcfh7m8d'
cognito_user_pool_id = 'us-east-1_wG3DBTkA1'
api_url = 'https://j0pf5n0i0e.execute-api.us-east-1.amazonaws.com/Stage/api'

print(ascii.logo)

def save_credentials(filepath, username, password):
    config = ConfigParser()
    config['default'] = {'username': username, 'password': password}
    with open(filepath, 'w') as configfile:
        config.write(configfile)

def generate_curl_command(api_url, token):
    # Prepare the curl command
    headers = {
        'Authorization': token,
        'Cache-Control': 'no-cache, no-store, must-revalidate',  # Prevents caching
        'Pragma': 'no-cache'}

    curl_command = f"curl -H {shlex.quote(headers)} {shlex.quote(api_url)}"
    return curl_command

def make_get_request(api_url, token):
    headers = {'Authorization': token}
    response = requests.get(api_url, headers=headers)
    return response.json()

home_dir = os.path.expanduser('~')
credentials_file_path = os.path.join(home_dir, '.hfcredentials')

if not os.path.exists(credentials_file_path):
    print("Credentials file not found. Please enter your credentials.")
    username = input("Username: ")
    password = input("Password: ")
    save_credentials(credentials_file_path, username, password)
else:
    config = ConfigParser()
    config.read(credentials_file_path)
    username = config.get('default', 'username')
    password = config.get('default', 'password')

# Function to handle SAM initialization and folder renaming
def init_and_customize_sam():
    project_name = input("Enter the name of the project: ").strip()
    python_version='3.12'

    # SAM init with basic non-interactive options
     # Run SAM init command
    try:
        subprocess.run([
            'sam', 'init',
            '--runtime', f'python{python_version}',
            '--dependency-manager', 'pip',
            '--name', project_name,
            '--app-template', 'hello-world',
            '--package-type', 'Zip'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during SAM initialization: {e}")
        return
    hello_world_path = os.path.join(os.getcwd(), project_name, 'hello_world')
    functions_path = os.path.join(os.getcwd(), project_name, 'functions')
    
    # Check if the 'hello-world' folder exists and rename it to 'functions'
    if os.path.exists(hello_world_path):
        os.rename(hello_world_path, functions_path)
        print("Created 'functions' folder.")
        clear_directory(functions_path)
    else:
        print(f"Expected Functions folder hello_world not found at {hello_world_path}")

# Function to delete all files in a given directory
def clear_directory(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return
    
    # Iterate over all files in the directory and remove them
    files = glob.glob(os.path.join(directory_path, '*'))
    for f in files:
        try:
            os.remove(f)
        except Exception as e:
            print(f"Error deleting file {f}: {e}")


# Handle 'init' command
if len(sys.argv) == 2 and sys.argv[1] == 'init':
    init_and_customize_sam()
    sys.exit(0)

# Parse command-line arguments
if len(sys.argv) != 3 or sys.argv[1] != 'pull':
    print("""Usage: 
          holo pull <appId> - pull code to local environment
          holo init - setup SAM environment""")
    sys.exit(1)

appId = sys.argv[2]
api_url = f"https://j0pf5n0i0e.execute-api.us-east-1.amazonaws.com/Stage/app?appId={appId}"

#animate(frames_pm, repeat=1, speed=0.4)


# Authenticate with AWS Cognito
client = boto3.client('cognito-idp')
response = client.initiate_auth(
    ClientId=cognito_client_id,
    AuthFlow='USER_PASSWORD_AUTH',
    AuthParameters={
        'USERNAME': username,
        'PASSWORD': password
    }
)

# Extract the ID token
id_token = response['AuthenticationResult']['IdToken']

# Make a GET request to the API Gateway
api_response= None
headers = {
        'Authorization': id_token,
        'Cache-Control': 'no-cache, no-store, must-revalidate',  # Prevents caching
        'Pragma': 'no-cache'}
api_response = requests.get(api_url, headers=headers)
print(api_response.text)
api_response_content = json.loads(api_response.text)  # Replace with api_response.json() if response is confirmed to be JSON
# Check if 'yaml' key exists in the response body
if 'yaml' in api_response_content['body']:
    yaml_content = api_response_content['body']['yaml']
    # Define the file path (template.yaml in the current working directory)
    yaml_file_path = os.path.join(os.getcwd(), 'template.yaml')
    
    # Write the yaml content to template.yaml, overwriting if it exists
    with open(yaml_file_path, 'w') as file:
        file.write(yaml_content)
    print(f"YAML content has been saved to {yaml_file_path}.")

# Check if 'lambda_functions' key exists in the response body
if 'lambda_functions' in api_response_content['body']:
    
    lambda_functions = api_response_content['body']['lambda_functions']
    #print(lambda_functions)
    for lfunction in lambda_functions:
        #print(lfunction)
        function_name = lfunction['name']
        function_directory_path = os.path.join(os.getcwd(), 'functions', function_name)
        function_path = os.path.join(os.getcwd(), 'functions', lfunction['name'], 'app.py')
        if not os.path.exists(function_directory_path):
            # If it doesn't exist, create the directory and any necessary parents
            os.makedirs(function_directory_path)
            init_file_path = os.path.join(function_directory_path, '__init__.py')
            with open(init_file_path, 'w') as init_file:
                pass
            print(f"Directory created: {function_directory_path}")
        function_content = lfunction['code']
        # Write the function to the function name folder, overwriting if it exists
        with open(function_path, 'w') as file:
            file.write(function_content)
        print(f"{lfunction['name']} has been saved to {function_path}.")
        if 'reqtxt' in lfunction:
            reqtxt_path = os.path.join(os.getcwd(), 'functions', lfunction['name'], 'requirements.txt')
            reqtxt_content = lfunction['reqtxt']
            # Write the requirements.txt to the function name folder, overwriting if it exists
            with open(reqtxt_path, 'w') as file:
                file.write(reqtxt_content)
            print(f"requirements.txt has been saved to {reqtxt_path}.")
    api_response = None
    

# Function to handle the initialization and customization of SAM based on your existing code
def init_and_customize_sam(project_name):
    python_version = '3.12'
    try:
        subprocess.run([
            'sam', 'init',
            '--runtime', f'python{python_version}',
            '--dependency-manager', 'pip',
            '--name', project_name,
            '--app-template', 'hello-world',
            '--package-type', 'Zip'
        ], check=True)
        print(f"Project {project_name} initialized successfully.")
        # Implement renaming logic here as needed
    except subprocess.CalledProcessError as e:
        print(f"Error during SAM initialization: {e}")

# Main function to handle command routing
def main():
    if len(sys.argv) < 2:
        print("Usage:\n  holo <command> [options]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'init':
        if len(sys.argv) < 3:
            print("Usage: holo init <project_name>")
            sys.exit(1)
        project_name = sys.argv[2]
        init_and_customize_sam(project_name)
    
    elif command == 'pull':
        if len(sys.argv) < 3:
            print("Usage: holo pull <appId>")
            sys.exit(1)
        app_id = sys.argv[2]
        pull_code(app_id)  # Implement this function based on your existing logic
    
    else:
        print(f"Unknown command: {command}")
        print("Usage:\n  holo init <project_name>\n  holo pull <appId>")
        sys.exit(1)

if __name__ == "__main__":
    main()
