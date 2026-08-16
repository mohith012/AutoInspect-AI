import os
import argparse
from roboflow import Roboflow

def download_dataset(api_key, workspace, project, version, output_dir):
    """
    Downloads the dataset from Roboflow Universe using the provided API key.
    """
    print(f"Downloading dataset {workspace}/{project}:{version} to {output_dir}")
    os.makedirs(output_dir, exist_ok=True)
    
    rf = Roboflow(api_key=api_key)
    project_rf = rf.workspace(workspace).project(project)
    version_rf = project_rf.version(version)
    
    # Download the dataset in folder format (image classification)
    dataset = version_rf.download("folder", location=output_dir)
    print(f"Dataset downloaded successfully to {dataset.location}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Vehicle Damage Severity Dataset from Roboflow")
    parser.add_argument("--api-key", type=str, required=True, help="Roboflow API Key")
    parser.add_argument("--output-dir", type=str, default="../data/raw", help="Output directory for the dataset")
    
    args = parser.parse_args()
    
    # Dataset coordinates from Roboflow Universe (Vehicle Damage Severity Classification)
    # Target dataset: https://universe.roboflow.com/car-damage-severity/vehicle-damage-severity
    workspace = "car-damage-severity"
    project = "vehicle-damage-severity"
    version = 1  # Using version 1 by default, can be updated if a specific version is preferred
    
    download_dataset(args.api_key, workspace, project, version, args.output_dir)
