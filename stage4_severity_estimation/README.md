# Stage 4: Damage Severity Estimation

This module is responsible for the AI-assisted visible damage severity estimation for the AutoInspect AI project. It classifies visually detected vehicle damage into one of three categories:
- `minor`
- `moderate`
- `severe`

**Important Note:** The system only estimates the severity of *visible* damage in the image. It does not detect hidden structural damage, internal mechanical damage, or make definitive claims about exact repairability or vehicle safety.

## Project Structure
- `configs/`: Contains configuration files like `severity_mapping.yaml`.
- `data/`: Contains the dataset (train/val/test splits).
- `models/`: Where the trained models are saved.
- `notebooks/`: Jupyter notebooks for data research, inspection, training, and evaluation.
- `results/`: Contains evaluation metrics, visualizations, and failure cases.
- `scripts/`: Utility scripts, such as `download_dataset.py`.
- `src/`: Core Python modules for dataset loading, preprocessing, model architecture, and inference.
- `tests/`: Unit tests for the Stage 4 pipeline.

## Getting Started

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download Dataset:**
   The primary dataset used is the Vehicle Damage Severity dataset from Kaggle.
   To download it, you need your Kaggle Username and API Key:
   ```bash
   cd scripts
   python download_kaggle_dataset.py --username YOUR_KAGGLE_USERNAME --key YOUR_KAGGLE_KEY
   ```
