import json
import re
import sys
import pkgutil
import importlib.util

# Some common import → pip package remappings
IMPORT_TO_PACKAGE = {
    "cv2": "opencv-python",
    "sklearn": "scikit-learn",
    "PIL": "Pillow",
    "yaml": "PyYAML",
    "bs4": "beautifulsoup4",
    "Crypto": "pycryptodome",
    "tensorflow": "tensorflow",
    "torch": "torch",
    "matplotlib.pyplot": "matplotlib",
    "IPython": "ipython",
    "pymongo": "pymongo",
    "seaborn": "seaborn",
    "xgboost": "xgboost",
    "lightgbm": "lightgbm",
    "sentence_transformers": "sentence-transformers",
}

# Check if a module is a standard library
def is_std_lib(module_name):
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            return False
        return 'site-packages' not in (spec.origin or '')
    except ModuleNotFoundError:
        return False

# Parse notebook for imports
def extract_imports_from_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
    code = "\n".join("".join(cell['source']) for cell in code_cells)

    # Match both "import x" and "from x import y"
    pattern = re.compile(r'^\s*(?:from\s+([a-zA-Z_][\w\.]*)|import\s+([a-zA-Z_][\w\.]*))', re.MULTILINE)
    matches = pattern.findall(code)

    raw_modules = set()
    for match in matches:
        mod = match[0] or match[1]
        root_mod = mod.split('.')[0]
        raw_modules.add(root_mod)

    return sorted(raw_modules)

# Map imports to pip installable names
def determine_pip_packages(imports):
    pip_packages = set()
    unresolved = []

    for mod in imports:
        pip_name = IMPORT_TO_PACKAGE.get(mod, mod)
        if not is_std_lib(mod):
            pip_packages.add(pip_name)
        else:
            continue

    return sorted(pip_packages)

def generate_pip_install_command(pip_packages):
    if pip_packages:
        pip_line = "!pip install " + " ".join(pip_packages)
        return pip_line
    else:
        return "# No non-standard packages detected."

def main(notebook_path):
    imports = extract_imports_from_notebook(notebook_path)
    pip_packages = determine_pip_packages(imports)
    pip_cmd = generate_pip_install_command(pip_packages)
    print("[📦] Paste this at the top of your notebook:\n")
    print(pip_cmd)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_colab_pip_command.py <notebook.ipynb>")
    else:
        main(sys.argv[1])
        
# Activate your virtual environment:
# .\venv\Scripts\activate

#run the script
# python generate_colab_pip_command.py your_notebook.ipynb
