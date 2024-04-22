import os

def create_env(token):
    # Get the directory of the current script
    # script_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the parent directory
    # parent_dir = os.path.dirname(script_dir)

    # Path to the .env file
    # env_file_path = os.path.join(parent_dir, ".env")

    # Define the content of the .env file
    # env_content = f"ED_API_TOKEN={token}\n"
    os.environ["ED_API_TOKEN"] = token
    print(os.environ)
    
    # Write the content to the .env file
    # with open(env_file_path, "w") as env_file:
    #     env_file.write(env_content)

    print(f"Created token: {token}")

def main():
    link = "https://edstem.org/us/settings/api-tokens"
    # provide user instructions
    print("To get the token, follow these steps:")
    print(f"1. Go to {link}\n")
    print("2. Sign in if needed\n")
    print("3. Click on 'Create Token'\n")
    print("4. Copy the token and paste it below\n")
    # Get the token from user input
    token = input("Enter your token: ")

    # Create the .env file with the token
    create_env(token)

if __name__ == "__main__":
    main()
