import json
import re

with open("notebooks/SpaceX-Machine-Learning-Prediction-Part-5-v1.ipynb", "r") as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "score" in source.lower():
            print("--- CODE ---")
            print(source)
            if 'outputs' in cell:
                print("--- OUTPUT ---")
                for out in cell['outputs']:
                    if 'text' in out:
                        print("".join(out['text']))
                    elif 'data' in out and 'text/plain' in out['data']:
                        print("".join(out['data']['text/plain']))
