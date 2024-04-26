from xlsx_utils import folder_to_json
import os
import sys

def get_opencti_credentials():
    opencti_url = os.getenv('OPENCTI_URL')
    opencti_token = os.getenv('OPENCTI_TOKEN')

    if not opencti_url or not opencti_token:
        raise EnvironmentError("Please set the OPENCTI_URL and OPENCTI_TOKEN environment variables.")

    return opencti_url, opencti_token


def main():
    try:
        url, token = get_opencti_credentials()
        # Assuming 'folder_to_json' needs these credentials, pass them as needed
        folder_path = sys.argv[1] if len(sys.argv) > 1 else "."
        folder_to_json(folder_path, url, token)  # Modify this line as per actual function signature
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()