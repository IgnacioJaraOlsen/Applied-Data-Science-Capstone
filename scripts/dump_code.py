import json

with open("notebooks/SpaceX-Machine-Learning-Prediction-Part-5-v1.ipynb", "r") as f:
    nb = json.load(f)

with open("scripts/notebook_code.py", "w") as out:
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            out.write("".join(cell['source']) + "\n\n")
