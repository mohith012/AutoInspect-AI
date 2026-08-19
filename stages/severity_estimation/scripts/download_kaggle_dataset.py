import os
import argparse
import subprocess

def download_kaggle_dataset(username, key, dataset_name, output_dir):
    """
    Downloads a Kaggle dataset using the kaggle CLI.
    Sets the KAGGLE_USERNAME and KAGGLE_KEY environment variables temporarily.
    """
    print(f"Downloading Kaggle dataset '{dataset_name}' to {output_dir}")
    os.makedirs(output_dir, exist_ok=True)
    
    # Set environment variables for Kaggle API authentication
    env = os.environ.copy()
    env["KAGGLE_USERNAME"] = username
    env["KAGGLE_KEY"] = key
    
    # Run the kaggle datasets download command
    command = ["kaggle", "datasets", "download", "-d", dataset_name, "-p", output_dir, "--unzip"]
    
    try:
        subprocess.run(command, env=env, check=True)
        print("Dataset downloaded and extracted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to download dataset. Ensure the 'kaggle' package is installed and credentials are correct. Error: {e}")
    except FileNotFoundError:
        print("The 'kaggle' command was not found. Please run 'pip install kaggle' first.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Vehicle Damage Severity Dataset from Kaggle")
    parser.add_argument("--username", type=str, required=True, help="Kaggle Username")
    parser.add_argument("--key", type=str, required=True, help="Kaggle API Key")
    parser.add_argument("--output-dir", type=str, default="../data/raw", help="Output directory for the dataset")
    
    args = parser.parse_args()
    
    # The dataset identifier on Kaggle
    dataset_name = "aniruddhsharma/vehicle-damage-severity-dataset"
    
    download_kaggle_dataset(args.username, args.key, dataset_name, args.output_dir)
