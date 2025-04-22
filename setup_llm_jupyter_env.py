"""
✅ Installs CUDA-enabled PyTorch stack (stable with CUDA 12.1)
✅ Installs transformers, bitsandbytes, accelerate, and all core dependencies for LLM inference
✅ Verifies GPU availability
✅ Registers your .venv as a selectable Jupyter kernel
✅ Writes a GPU + tqdm test notebook to validate everything inside Jupyter
✅ Virtual environment kernel name set to: "resume-agent"
✅ Display name shown in Jupyter: "Python (Resume Agent)"
  """
import subprocess
import sys
import os
import json

import subprocess
import sys
import os
import json

def run(cmd, check=True):
    print(f"\n▶ Running: {cmd}")
    subprocess.run(cmd, shell=True, check=check)

def install_core_packages():
    print("\n📦 Installing core ML + HuggingFace packages (CUDA 12.1)...")

    run(f"{sys.executable} -m pip install --upgrade pip setuptools wheel")

    # 🔒 Install NumPy 1.26.4 explicitly to avoid ABI break with 2.x
    run(f"{sys.executable} -m pip install numpy==1.26.4")

    # ✅ Stable PyTorch stack with CUDA 12.1
    run(f"{sys.executable} -m pip install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cu121")

    # ✅ LLM support
    run(f"{sys.executable} -m pip install transformers accelerate bitsandbytes sentencepiece pydantic==1.10.13 huggingface_hub")

def install_jupyter_support():
    print("\n📘 Installing Jupyter + tqdm + ipywidgets...")
    run(f"{sys.executable} -m pip install notebook==7.1.2 ipywidgets==8.1.2 tqdm ipykernel pandas")

    print("\n✅ ipywidgets 8.x works natively with notebook 7.x — no manual enabling needed.")

def register_kernel(kernel_name="resume-agent", display_name="Python (Resume Agent)"):
    print(f"\n🧠 Registering virtualenv kernel: {kernel_name}")
    # Use double quotes for Windows compatibility
    run(f'{sys.executable} -m ipykernel install --user --name={kernel_name} --display-name "{display_name}"')

def create_test_notebook():
    print("\n🧪 Creating LLM+GPU+tqdm test notebook...")

    code = '''
import torch
from tqdm.notebook import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import numpy

print("Torch CUDA:", torch.version.cuda)
print("Is CUDA available:", torch.cuda.is_available())
print("Device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU")
print("NumPy Version:", numpy.__version__)

# Test tqdm bar
for i in tqdm(range(10), desc="Progress Test"):
    pass
'''

    nb = {
        "cells": [{
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": code.splitlines(True)
        }],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5
    }

    with open("test_llm_gpu_notebook.ipynb", "w") as f:
        json.dump(nb, f, indent=2)

    print("✅ Notebook saved as 'test_llm_gpu_notebook.ipynb'")

if __name__ == "__main__":
    print("\n🚀 Setting up Resume Agent Virtual Environment")
    install_core_packages()
    install_jupyter_support()
    register_kernel(kernel_name="resume-agent", display_name="Python (Resume Agent)")
    create_test_notebook()
    print("\n🎯 Setup complete! Run `jupyter notebook`, open 'test_llm_gpu_notebook.ipynb', and validate the environment.")
