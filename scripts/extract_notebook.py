import json
import os

notebook_path = r"c:\Users\ijara\Documentos\Codigos\python\coursera\Applied Data Science Capstone\notebooks\lab-jupyter-launch-site-location-v2.ipynb"
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

code_cells = []
for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        # ignore magic commands
        source = [line for line in cell.get('source', []) if not line.startswith('!') and not line.startswith('%')]
        code_cells.append("".join(source))

output_path = "scripts/extracted_folium_notebook.py"
if not os.path.exists("scripts"):
    os.makedirs("scripts")
with open(output_path, 'w', encoding='utf-8') as f:
    for i, code in enumerate(code_cells):
        f.write(f"# Cell {i}\n")
        f.write(code)
        f.write("\n\n")

print(f"Code extracted to {output_path}")
