import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

output_dir = 'Presentation_Assets'
os.makedirs(output_dir, exist_ok=True)

# Styling Constants
box_width = 0.82
box_height = 0.08
x_center = 0.5
padding = 0.025
box_color = '#f4f8fe'     # IBM Blue Light
border_color = '#0f62fe'  # IBM Blue
text_color = '#001d6c'    # Dark Blue Text
arrow_color = '#0f62fe'   # IBM Blue

def create_flowchart(steps, title, filename):
    fig, ax = plt.subplots(figsize=(10, 12))
    fig.patch.set_facecolor('#f4f6f9')
    ax.set_facecolor('#f4f6f9')
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    n_steps = len(steps)
    y_centers = [0.88 - i * (0.76 / (n_steps - 1)) for i in range(n_steps)]

    for i, (step, y) in enumerate(zip(steps, y_centers)):
        # Box
        box = patches.FancyBboxPatch(
            (x_center - box_width/2, y - box_height/2),
            box_width, box_height, boxstyle=f"round,pad={padding}",
            linewidth=3, edgecolor=border_color, facecolor=box_color, zorder=3
        )
        ax.add_patch(box)
        
        # Text
        ax.text(x_center, y, step, ha="center", va="center", 
                fontsize=15, color=text_color, fontweight='bold', zorder=4)
                
        # Arrow
        if i < n_steps - 1:
            y_next = y_centers[i+1]
            arrow_start_y = y - box_height/2 - padding
            arrow_end_y = y_next + box_height/2 + padding
            
            ax.annotate('', xy=(x_center, arrow_end_y), xytext=(x_center, arrow_start_y),
                        arrowprops=dict(arrowstyle="-|>", color=arrow_color, lw=3,
                                        mutation_scale=25, shrinkA=0, shrinkB=0),
                        zorder=1)

    plt.title(title, fontsize=28, pad=20, fontweight='bold', color=border_color)
    plt.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight', 
                facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {filename}")

# Flowchart 1: API Collection (Slide 8)
api_steps = [
    "1. Request Data from SpaceX API\n(GET https://api.spacexdata.com/v4/launches)",
    "2. Receive JSON Response\n(Raw metadata of all launches)",
    "3. Normalize Data\n(pd.json_normalize to unnest JSON into Columns)",
    "4. Filter Records\n(Keep only 'Falcon 9' rocket launches)",
    "5. Handle Missing/Nested Values\n(API Calls for Core, Payload, Pad Data)",
    "6. Final Cleaned DataFrame\n(Saved as dataset_part_1.csv)"
]
create_flowchart(api_steps, "SpaceX API Data Collection Flowchart", 'Slide_08_API_Flowchart.png')

# Flowchart 2: Web Scraping (Slide 9)
scraping_steps = [
    "1. Request Wikipedia Page\n(Using requests.get to fetch HTML content)",
    "2. Parse HTML with BeautifulSoup\n(Create a soup object to navigate\nthe DOM tree)",
    "3. Locate Falcon 9 Launch Tables\n(Find all <table> elements with class 'wikitable')",
    "4. Extract Column Headers & Data Rows\n(Iterate through <th> and <tr>/<td> tags)",
    "5. Clean Extracted Values\n(Remove citations, references, and unicode chars)",
    "6. Build Dictionary & Convert to DataFrame\n(Saved as spacex_web_scraped.csv)"
]
create_flowchart(scraping_steps, "Wikipedia Web Scraping Flowchart", 'Slide_09_Scraping_Flowchart.png')

# Flowchart 3: Data Wrangling (Slide 10)
wrangling_steps = [
    "1. Load Raw API / Scraped Data\n(Imports CSVs into Pandas DataFrames)",
    "2. Calculate Missing Values\n(Identify NaNs in 'PayloadMass' and 'LandingPad')",
    "3. Impute Missing Data\n(Replace empty payload\nweights with historical mean)",
    "4. Engineer Target Variable 'Class'\n(Map varied landing outcomes to\n1 [Success] or 0 [Fail])",
    "5. Extract Year Feature\n(Parse Launch Dates to create a 'Year' column)",
    "6. Export Prepared Dataset\n(Saved as dataset_part_2.csv\nfor EDA & Mapping)"
]
create_flowchart(wrangling_steps, "Data Wrangling & Cleaning Flowchart", 'Slide_10_Wrangling_Flowchart.png')

# Flowchart 4: Predictive Analysis (Slide 15)
ml_steps = [
    "1. Prepare Feature Set (X) & Target (Y)\n(One-Hot Encode Categorical Vars\n=> dataset_part_3.csv)",
    "2. Standardize Features\n(Apply sklearn StandardScaler\nto feature columns)",
    "3. Train-Test Split\n(Divide data 80% Training / 20% Testing\nwith random_state=2)",
    "4. Define Classifier Models\n(Instantiate Logistic Regression, SVM,\nDecision Tree, KNN)",
    "5. Hyperparameter Tuning\n(Use GridSearchCV across all models\nto find optimal params)",
    "6. Evaluate & Select Best Model\n(Calculate Accuracy & Plot Confusion\nMatrix on Test Data)"
]
create_flowchart(ml_steps, "Predictive Machine Learning Pipeline", 'Slide_15_ML_Pipeline_Flowchart.png')

print("All flowcharts generated successfully!")
