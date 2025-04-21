import json
import re
import sys
import os
import subprocess

# Optional: more complete map if needed
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
}

def extract_imports_from_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
    code = "\n".join("".join(cell['source']) for cell in code_cells)

    import_lines = set()

    pattern = re.compile(r'^\s*(?:from\s+(\S+)|import\s+(\S+))', re.MULTILINE)
    matches = pattern.findall(code)

    for match in matches:
        imported_module = match[0] or match[1]
        base_module = imported_module.split('.')[0]
        import_lines.add(base_module)

    return sorted(import_lines)

def get_installed_packages():
    output = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], encoding='utf-8')
    frozen = output.strip().split('\n')
    return {line.split('==')[0].lower(): line for line in frozen if '==' in line}

def map_imports_to_requirements(imports, installed_packages):
    requirements = set()

    for imp in imports:
        pypi_name = IMPORT_TO_PACKAGE.get(imp, imp)
        key = pypi_name.lower()
        if key in installed_packages:
            requirements.add(installed_packages[key])
        else:
            print(f"[⚠️  Warning] Could not resolve: {imp} -> {pypi_name} (Not found in current environment)")

    return sorted(requirements)

def write_requirements_file(requirements, output_path='requirements.txt'):
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in requirements:
            f.write(line + '\n')
    print(f"[✅] Created '{output_path}' with {len(requirements)} packages.")

def main(notebook_path):
    if not os.path.exists(notebook_path):
        print(f"[❌] File not found: {notebook_path}")
        return

    print(f"[🔍] Parsing imports from: {notebook_path}")
    imports = extract_imports_from_notebook(notebook_path)
    print(f"[📦] Detected imports: {imports}")

    print(f"[📂] Checking current environment for installed packages...")
    installed_packages = get_installed_packages()

    print(f"[🔁] Mapping imports to PyPI package names...")
    requirements = map_imports_to_requirements(imports, installed_packages)

    write_requirements_file(requirements)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_requirements_from_ipynb.py <notebook.ipynb>")
    else:
        main(sys.argv[1])

# Activate your virtual environment:
# .\venv\Scripts\activate

#run the script
# python generate_requirements_from_ipynb.py your_notebook.ipynb
