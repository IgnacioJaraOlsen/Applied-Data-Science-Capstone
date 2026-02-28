import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
import textwrap

os.makedirs('Presentation_Assets', exist_ok=True)
db_path = 'notebooks/my_data1.db'

# Colors matching the PPT
BG_COLOR = '#f4f6f9'
HEADER_COLOR = '#0f62fe'
ROW_COLOR_1 = '#ffffff'
ROW_COLOR_2 = '#f4f8fe'
TEXT_COLOR_DARK = '#001d6c'
TEXT_COLOR_LIGHT = '#ffffff'

queries = [
    (24, "All Launch Site Names", "SELECT DISTINCT \"Launch_Site\" FROM SPACEXTBL;"),
    (25, "Launch Site Names Begin with 'CCA'", "SELECT * FROM SPACEXTBL WHERE \"Launch_Site\" LIKE 'CCA%' LIMIT 5;"),
    (26, "Total Payload Mass by NASA (CRS)", "SELECT SUM(\"PAYLOAD_MASS__KG_\") AS TOTAL_PAYLOAD_MASS FROM SPACEXTBL WHERE \"Customer\" = 'NASA (CRS)';"),
    (27, "Average Payload Mass (F9 v1.1)", "SELECT AVG(\"PAYLOAD_MASS__KG_\") AS AVERAGE_PAYLOAD_MASS FROM SPACEXTBL WHERE \"Booster_Version\" = 'F9 v1.1';"),
    (28, "First Successful Ground Landing Date", "SELECT MIN(\"Date\") AS FIRST_SUCCESSFUL_GROUND_PAD_LANDING FROM SPACEXTBL WHERE \"Landing_Outcome\" = 'Success (ground pad)';"),
    (29, "Successful Drone Ship Landings", "SELECT \"Booster_Version\" FROM SPACEXTBL WHERE \"Landing_Outcome\" = 'Success (drone ship)' AND \"PAYLOAD_MASS__KG_\" > 4000 AND \"PAYLOAD_MASS__KG_\" < 6000;"),
    (30, "Mission Outcomes", "SELECT \"Mission_Outcome\", COUNT(*) AS TOTAL_NUMBER FROM SPACEXTBL GROUP BY \"Mission_Outcome\";"),
    (31, "Boosters Carried Maximum Payload", "SELECT \"Booster_Version\" FROM SPACEXTBL WHERE \"PAYLOAD_MASS__KG_\" = (SELECT MAX(\"PAYLOAD_MASS__KG_\") FROM SPACEXTBL);"),
    (32, "2015 Failures (Drone Ship)", "SELECT substr(\"Date\", 6, 2) AS MONTH, \"Booster_Version\", \"Launch_Site\", \"Landing_Outcome\" FROM SPACEXTBL WHERE \"Landing_Outcome\" = 'Failure (drone ship)' AND substr(\"Date\", 0, 5) = '2015';"),
    (33, "Landing Outcomes Ranking", "SELECT \"Landing_Outcome\", COUNT(*) AS QUANTITY FROM SPACEXTBL WHERE \"Date\" BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY \"Landing_Outcome\" ORDER BY QUANTITY DESC;")
]

conn = sqlite3.connect(db_path)

for slide_num, title, query in queries:
    df = pd.read_sql_query(query, conn)
    
    df = df.astype(str)
    num_cols = len(df.columns)
    
    max_allowed_width = 10.0 if slide_num == 25 else 8.0
    
    fig_width = min(max_allowed_width, max(5.0, 2.0 * num_cols))
    wrap_width = max(8, int((fig_width * 9) / num_cols)) 
    fontsize = max(8, min(12, int((fig_width * 12) / num_cols)))
    
    # Wrap headers
    new_cols = []
    for col in df.columns:
        new_cols.append('\n'.join(textwrap.wrap(col.replace('_', ' '), width=wrap_width, break_long_words=False)))
    df.columns = new_cols
    
    # Wrap data cells BEFORE calculating lines
    for col in df.columns:
        df[col] = df[col].apply(lambda x: '\n'.join(textwrap.wrap(x, width=wrap_width, break_long_words=False)) if pd.notnull(x) else "")
        
    row_heights_dict = {}
    header_lines = max((col.count('\n') + 1 for col in df.columns), default=1)
    row_heights_dict[0] = header_lines + 0.5
    
    for r in range(len(df)):
        lines = 1
        for c in df.columns:
            val = str(df.iloc[r][c])
            lines = max(lines, val.count('\n') + 1)
        row_heights_dict[r + 1] = lines + 0.5
        
    total_lines = sum(row_heights_dict.values())

    fig_height = max(1.5, 0.28 * total_lines)
            
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    fig.patch.set_facecolor(BG_COLOR)
    ax.axis('off')
    ax.axis('tight')
    
    # Use bbox to add padding around the table, allowing for custom row heights
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', bbox=[0.02, 0.02, 0.96, 0.96])
    table.auto_set_font_size(False)
    table.set_fontsize(fontsize)
    
    for (row, col), cell in table.get_celld().items():
        cell.set_height(row_heights_dict[row] / total_lines)
        cell.set_edgecolor('#c9d1d9') # Slightly darker border for better visibility
        cell.set_linewidth(1.0)
        if row == 0:
            cell.set_text_props(weight='bold', color=TEXT_COLOR_LIGHT)
            cell.set_facecolor(HEADER_COLOR)
        else:
            cell.set_text_props(color=TEXT_COLOR_DARK)
            cell.set_facecolor(ROW_COLOR_1 if row % 2 == 0 else ROW_COLOR_2)
            
    fig.tight_layout()
    output_path = f'Presentation_Assets/Slide_{slide_num}_SQL_Table.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Generated {output_path}")

conn.close()
