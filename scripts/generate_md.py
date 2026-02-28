import sqlite3
import os

db_path = 'notebooks/my_data1.db'
output_file = 'Presentation_Assets/Final_Presentation_Content.md'

try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    def exec_query(query):
        try:
            c.execute(query)
            cols = [desc[0] for desc in c.description]
            rows = c.fetchall()
            return cols, rows
        except Exception as e:
            return ["Error"], [[str(e)]]

    # Precompute SQL answers
    # Slide 24: Unique launch sites
    c_24, r_24 = exec_query("SELECT DISTINCT \"Launch_Site\" FROM SPACEXTBL;")
    
    # Slide 25: 5 records CCA
    c_25, r_25 = exec_query("SELECT * FROM SPACEXTBL WHERE \"Launch_Site\" LIKE 'CCA%' LIMIT 5;")
    
    # Slide 26: Total payload NASA
    c_26, r_26 = exec_query("SELECT SUM(\"PAYLOAD_MASS__KG_\") AS TOTAL_PAYLOAD_MASS FROM SPACEXTBL WHERE \"Customer\" = 'NASA (CRS)';")
    
    # Slide 27: Average Payload F9 v1.1
    c_27, r_27 = exec_query("SELECT AVG(\"PAYLOAD_MASS__KG_\") AS AVERAGE_PAYLOAD_MASS FROM SPACEXTBL WHERE \"Booster_Version\" = 'F9 v1.1';")
    
    # Slide 28: First ground landing date
    c_28, r_28 = exec_query("SELECT MIN(\"Date\") AS FIRST_SUCCESSFUL_GROUND_PAD_LANDING FROM SPACEXTBL WHERE \"Landing_Outcome\" = 'Success (ground pad)';")
    
    # Slide 29: Drone ship success 4000 to 6000
    c_29, r_29 = exec_query("SELECT \"Booster_Version\" FROM SPACEXTBL WHERE \"Landing_Outcome\" = 'Success (drone ship)' AND \"PAYLOAD_MASS__KG_\" > 4000 AND \"PAYLOAD_MASS__KG_\" < 6000;")
    
    # Slide 30: Total outcomes
    c_30, r_30 = exec_query("SELECT \"Mission_Outcome\", COUNT(*) AS TOTAL_NUMBER FROM SPACEXTBL GROUP BY \"Mission_Outcome\";")
    
    # Slide 31: Max payload booster
    c_31, r_31 = exec_query("SELECT \"Booster_Version\" FROM SPACEXTBL WHERE \"PAYLOAD_MASS__KG_\" = (SELECT MAX(\"PAYLOAD_MASS__KG_\") FROM SPACEXTBL);")
    
    # Slide 32: 2015 drone ship failed
    c_32, r_32 = exec_query("SELECT substr(\"Date\", 6, 2) AS MONTH, \"Booster_Version\", \"Launch_Site\", \"Landing_Outcome\" FROM SPACEXTBL WHERE \"Landing_Outcome\" = 'Failure (drone ship)' AND substr(\"Date\", 0, 5) = '2015';")
    
    # Slide 33: Rank landing outcomes between dates
    c_33, r_33 = exec_query("SELECT \"Landing_Outcome\", COUNT(*) AS QUANTITY FROM SPACEXTBL WHERE \"Date\" BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY \"Landing_Outcome\" ORDER BY QUANTITY DESC;")

    def format_table(cols, rows):
        if not rows: return "*No data returned*"
        md = "| " + " | ".join(cols) + " |\n"
        md += "|-" * len(cols) + "|\n"
        for r in rows:
            md += "| " + " | ".join([str(x) for x in r]) + " |\n"
        return md

    md_content = """# Final Presentation Content

This document maps directly to the slides in `ds-capstone-template-coursera.pptx`. 
Copy and paste the text and image references into the corresponding slides.

---
## Slide 1: Title
**Title Text:** Winning Space Race with Data Science
**Subtitle:** [Your Name] | [Date]

---
## Slide 2: Outline
**Content:**
- Executive Summary
- Introduction
- Methodology
- Results
- Conclusion
- Appendix

---
## Slide 3: Executive Summary
**Summary of methodologies:**
- Collected data via SpaceX API and Web Scraping.
- Processed data by handling missing values and one-hot encoding categorical variables.
- Conducted EDA with Pandas and SQL.
- Created interactive maps with Folium and dashboards with Plotly Dash.
- Trained classification models (Logistic Regression, SVM, Decision Tree, KNN) to predict launch success.

**Summary of all results:**
- Payload mass and Launch Site are key factors in success.
- KSC LC-39A has the highest success rate.
- Overall launch success rate has trended upward over the years.
- Logistic Regression, SVM, and KNN tied as the best performing models for classifying successful launches.

---
## Slide 4: Introduction
**Project background and context:**
- SpaceX advertises Falcon 9 rocket launches at much lower costs than competitors.
- The savings are mostly due to reusing the first stage.
- Determining whether the first stage will land successfully is critical.

**Problems you want to find answers to:**
- Can we predict if the Falcon 9 first stage will land successfully based on past launch parameters?
- How do variables like payload mass, launch site, and orbit type affect the outcome?

---
## Slide 5: Section 1
*(Section Divider: Methodology)*

---
## Slide 6: Methodology
- **Data collection methodology:**
  - Collected data via SpaceX API (for core flight data) and web scraped from Wikipedia (for Falcon 9 hardware details).
- **Perform data wrangling:**
  - Filtered records for Falcon 9, handled missing values, and standardized categorical variables using One-Hot Encoding.
- **Perform exploratory data analysis (EDA) using visualization and SQL**
- **Perform interactive visual analytics using Folium and Plotly Dash**
- **Perform predictive analysis using classification models:**
  - Built, tuned (via GridSearchCV), and evaluated Logistic Regression, SVM, Decision Tree, and KNN models.

---
## Slide 7: Data Collection
- Requested raw data from SpaceX API.
- Filtered specifically for Falcon 9 launches.
- Web scraped Falcon 9 historical launch facts from Wikipedia.
- Cleaned the acquired data into a standardized Pandas DataFrame.

---
## Slide 8: Data Collection – SpaceX API
*(Insert Flowchart of SpaceX API Calls if you created one, or describe the sequence: Request -> JSON -> Filter -> DataFrame)*

---
## Slide 9: Data Collection - Scraping
*(Insert Flowchart of Web Scraping if you created one, or describe: BeautifulSoup -> Parse Tables -> Extract Column Data -> DataFrame)*

---
## Slide 10: Data Wrangling
- Analyzed missing variables (e.g. Landing Pad).
- Imputed or dropped missing data as appropriate.
- Engineered features such as `Class` (Success/Failed) from landing outcomes.
- Exported preprocessed data to CSV files (`dataset_part_2.csv`, `dataset_part_3.csv`) for further steps.

---
## Slide 11: EDA with Data Visualization
- Plotted multiple charts (Scatter, Line, Bar) to understand variable relationships.
- Investigated `PayloadMass` and `LaunchSite` as they strongly correlated with successful landings.
- Identified clear yearly trends showing continuous improvement in success rates.

---
## Slide 12: EDA with SQL
- Connected to SQLite database using `sqlite3` and `pandas`.
- Wrote and executed complex queries including `GROUP BY`, aggregations, and subqueries.
- Filtered data based on explicit criteria to answer business questions about maximum payload, booster versions, and launch site statuses.

---
## Slide 13: Build an Interactive Map with Folium
- Plotted launch sites on a global map using `folium.Marker` and `folium.Circle`.
- Grouped markers using `MarkerCluster` to show successful vs failed landings per site.
- Used `folium.PolyLine` to calculate and visualize distances from launch sites to coastlines, railways, and highways.

---
## Slide 14: Build a Dashboard with Plotly Dash
- Created an interactive dropdown to select launch sites.
- Implemented a Range Slider to filter launches by `Payload Mass`.
- Generated dynamic Pie charts and Scatter plots that respond instantly to user input.

---
## Slide 15: Predictive Analysis (Classification)
- Scaled data using `StandardScaler`.
- Split data into Training and Testing sets (80/20).
- Utilized `GridSearchCV` to find the best hyperparameters for LR, SVM, Decision Tree, and KNN.
- Compared the accuracy metrics and plotted the final confusion matrix.

---
## Slide 16: Results
- **Exploratory Data Analysis Results:** Launch success generally correlates positively with increasing payload masses and specifically with the KSC LC-39A launch site. Overall success rates have shown steady improvement year-over-year.
- **Interactive Analytics Demo:** Map clustering and Dash filtering dashboards visually confirmed that successful booster recoveries are tightly clustered among specific geographical coordinates and predominantly clear for mid-to-high block payload ranges.
- **Predictive Analysis Results:** Supervised classification models reached ~83.3% test accuracy. Logistic Regression, SVM, and KNN emerged as equally robust choices for predicting first-stage landing success based on historical constraints.

---
## Slide 17: Section 2
*(Section Divider: EDA Results)*

---
## Slide 18: Flight Number vs. Launch Site
**Insert Image:** `Slide_18_Flight_vs_Site.png`
**Explanation:** As flight numbers increase, success rates generally improve, reflecting accumulated experience and technical advancements.

---
## Slide 19: Payload vs. Launch Site
**Insert Image:** `Slide_19_Payload_vs_Site.png`
**Explanation:** Launch outcomes varied significantly depending on the site and the physical mass of the payload.

---
## Slide 20: Success Rate vs. Orbit Type
**Insert Image:** `Slide_20_SuccessRate_vs_Orbit.png`
**Explanation:** Certain orbit types (like ES-L1, GEO, HEO, SSO) have much higher success rates, possibly due to more standardized mission profiles.

---
## Slide 21: Flight Number vs. Orbit Type
**Insert Image:** `Slide_21_Flight_vs_Orbit.png`
**Explanation:** Over time, missions to specific orbits became more frequent, and we can visually see fewer failures corresponding to those clusters in newer flights.

---
## Slide 22: Payload vs. Orbit Type
**Insert Image:** `Slide_22_Payload_vs_Orbit.png`
**Explanation:** This scatter plot confirms that heavy payloads to GTO are common, but they pose unique challenges to booster recovery.

---
## Slide 23: Launch Success Yearly Trend
**Insert Image:** `Slide_23_Yearly_Trend.png`
**Explanation:** The success rate jumped dramatically between 2013 and 2016, maintaining consistently high averages through the subsequent years.

---
## Slide 24: All Launch Site Names
**Query:** `SELECT DISTINCT "Launch_Site" FROM SPACEXTBL;`
**Result:**
""" + format_table(c_24, r_24) + """
**Explanation:** Displays the names of the unique launch sites in the space mission.

---
## Slide 25: Launch Site Names Begin with 'CCA'
**Query:** `SELECT * FROM SPACEXTBL WHERE "Launch_Site" LIKE 'CCA%' LIMIT 5;`
**Result:**  *(top 5 rows extracted)*
""" + format_table(c_25, r_25) + """
**Explanation:** Filtering records specifically from the Cape Canaveral Air Force Station (CCAFS) launch facilities.

---
## Slide 26: Total Payload Mass by NASA (CRS)
**Query:** `SELECT SUM("PAYLOAD_MASS__KG_") AS TOTAL_PAYLOAD_MASS FROM SPACEXTBL WHERE "Customer" = 'NASA (CRS)';`
**Result:**
""" + format_table(c_26, r_26) + """
**Explanation:** Displays the total payload mass carried by boosters launched by NASA (CRS).

---
## Slide 27: Average Payload Mass (F9 v1.1)
**Query:** `SELECT AVG("PAYLOAD_MASS__KG_") AS AVERAGE_PAYLOAD_MASS FROM SPACEXTBL WHERE "Booster_Version" = 'F9 v1.1';`
**Result:**
""" + format_table(c_27, r_27) + """
**Explanation:** Displays the average payload mass explicitly for the Booster Version F9 v1.1.

---
## Slide 28: First Successful Ground Landing Date
**Query:** `SELECT MIN("Date") AS FIRST_SUCCESSFUL_GROUND_PAD_LANDING FROM SPACEXTBL WHERE "Landing_Outcome" = 'Success (ground pad)';`
**Result:**
""" + format_table(c_28, r_28) + """
**Explanation:** Identifies the historical milestone date when a core was first successfully recovered on a ground pad.

---
## Slide 29: Successful Drone Ship Landings (Payload 4000-6000)
**Query:** `SELECT "Booster_Version" FROM SPACEXTBL WHERE "Landing_Outcome" = 'Success (drone ship)' AND "PAYLOAD_MASS__KG_" > 4000 AND "PAYLOAD_MASS__KG_" < 6000;`
**Result:**
""" + format_table(c_29, r_29) + """
**Explanation:** Lists specific booster versions that proved capable of landing on a drone ship while carrying mid-to-heavy payloads.

---
## Slide 30: Total Number of Successful and Failure Mission Outcomes
**Query:** `SELECT "Mission_Outcome", COUNT(*) AS TOTAL_NUMBER FROM SPACEXTBL GROUP BY "Mission_Outcome";`
**Result:**
""" + format_table(c_30, r_30) + """
**Explanation:** An aggregate view of overall mission success rates across all documented flights.

---
## Slide 31: Boosters Carried Maximum Payload
**Query:** `SELECT "Booster_Version" FROM SPACEXTBL WHERE "PAYLOAD_MASS__KG_" = (SELECT MAX("PAYLOAD_MASS__KG_") FROM SPACEXTBL);`
**Result:**
""" + format_table(c_31, r_31) + """
**Explanation:** Identifies the heavy-lift variants (Block 5 series) responsible for carrying the maximum recorded payloads (15,600 kg) to orbit.

---
## Slide 32: 2015 Failures (Drone Ship)
**Query:** `SELECT substr("Date", 6, 2) AS MONTH, "Booster_Version", "Launch_Site", "Landing_Outcome" FROM SPACEXTBL WHERE "Landing_Outcome" = 'Failure (drone ship)' AND substr("Date", 0, 5) = '2015';`
**Result:**
""" + format_table(c_32, r_32) + """
**Explanation:** Isolates early drone ship landing failures during the year 2015 to highlight the experimental phases of booster recovery.

---
## Slide 33: Rank Landing Outcomes Between 2010-06-04 and 2017-03-20
**Query:** `SELECT "Landing_Outcome", COUNT(*) AS QUANTITY FROM SPACEXTBL WHERE "Date" BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY "Landing_Outcome" ORDER BY QUANTITY DESC;`
**Result:**
""" + format_table(c_33, r_33) + """
**Explanation:** Ranked count of landing outcomes between the date 2010-06-04 and 2017-03-20.

---
## Slide 34: Section 3
*(Section Divider: Interactive Map)*

---
## Slide 35: Global Launch Site Distribution
**Insert Image:** `Slide_35_Global_Map.png`
**Explanation:** Most launch sites are positioned near coastlines (Florida, California) for safety over open water.

---
## Slide 36: Launch Outcomes by Regional Cluster
**Insert Image:** `Slide_36_Color_Labeled_Map.png`
**Explanation:** Launch Site KSC LC-39A exhibits a noticeably higher cluster of green (success) markers compared to older pads.

---
## Slide 37: Proximity to Transport and Coastlines
**Insert Image:** `Slide_37_Proximity_Map.png`
**Explanation:** Pads are strategically placed right against railways for heavy transport and next to coastlines safely isolated from major cities.

---
## Slide 38: Section 4
*(Section Divider: Dash Dashboard)*

---
## Slide 39: Launch Success for All Sites
**Title:** Launch Success for All Sites
**Insert Image:** `Slide_39_Dash_Pie_All.png` (or take screenshot from `spacex_dash_app.py`)
**Explanation:** KSC LC-39A and CCAFS LC-40 are responsible for the highest proportion of successful Falcon 9 launches.

---
## Slide 40: Launch Success for KSC LC-39A
**Title:** Launch Success for KSC LC-39A
**Insert Image:** `Slide_40_Dash_Pie_Site.png` (or take screenshot from `spacex_dash_app.py`)
**Explanation:** Analyzing KSC LC-39A alone shows an exceptionally strong ratio of successes to failures, marking it as a highly reliable site.

---
## Slide 41: Payload vs. Success Correlation
**Title:** Payload vs. Success Correlation
**Insert Image:** `Slide_41_Dash_Scatter.png` (or take screenshot from `spacex_dash_app.py`)
**Explanation:** The scatter plot illustrates that heavier payloads (often carried by advanced booster versions) do not necessarily guarantee failure; recent versions handle high payloads successfully.

---
## Slide 42: Section 5
*(Section Divider: Predictive Analysis)*

---
## Slide 43: Classification Accuracy
**Insert Image:** `Slide_43_Classification_Accuracy.png`
**Explanation:** All evaluated models (Logistic Regression, SVM, Decision Tree, KNN) achieved a roughly similar baseline accuracy, though Logistic Regression, SVM, and KNN tied for the highest test accuracy (83.3%), outperforming the Decision Tree.

---
## Slide 44: Confusion Matrix
**Insert Image:** `Slide_44_Confusion_Matrix.png`
**Explanation:** The matrix confirms that the prediction model successfully identified the large majority of actual successful landings with minimal false positives.

---
## Slide 45: Conclusions
- **Payload & Location:** Launch Site KSC LC-39A is the most successful pad. Payloads around the 2k-4k range have high reliability.
- **Trends:** Over the years, the number of failures dropped severely, proving SpaceX improved their recovery systems over time.
- **Machine Learning:** Predictive modelling yielded strong accuracy (~83%), with Logistic Regression, SVM, and KNN proving to be the most reliable indicators of re-usability.

---
## Slide 46: Appendix
*(Optional: include any references to IBM, GitHub links, or extra Python snippets)*
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print("Final Presentation Content explicitly generated!")
    
except Exception as e:
    print("Error:", e)
