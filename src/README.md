#  Healthcare Accessibility Index (USA)

This project analyzes and ranks all U.S. states (plus D.C.) based on their **access to healthcare services**, combining multiple public data sources.

---

##  Goal

To develop a data-driven **Healthcare Accessibility Score** using key factors such as:

- Population size
- Median household income
- Insurance coverage
- Broadband access (for telehealth)
- Health center availability
- Travel time to nearest facility (simulated)

---

##  Data Sources

- **HRSA**: Health Centers by State  
- **Census**: Population, Income  
- **KFF**: Insurance Coverage  
- **FCC**: Broadband Availability  
- **OpenRouteService**: Simulated travel time

---

##  Features Used

| Feature                | Description                              |
|------------------------|------------------------------------------|
| `insured_pct`          | % of population with health insurance    |
| `broadband_pct`        | % of population with internet access     |
| `median_income($1k)`   | State median income (scaled)             |
| `facilities_per_100k`  | Healthcare sites per 100k people         |
| `avg_travel_time_min`  | Simulated average travel time (inverted) |

All features are **min-max normalized**, weighted, and combined into a single `access_score`.

---

##  How It Works

1. **Clean individual datasets**
   - Fix headers, remove national rows, normalize column names.

2. **Calculate state-level metrics:**
   - Insurance % = 1 - Uninsured %
   - Facility-to-population ratio
   - Normalize broadband and income
   - Use ORS API to fetch average travel time per state

3. **Normalize travel time** (lower is better) and invert score

4. **Score each state**
   - All components normalized to a common scale
   - Weights applied equally or custom (adjustable)

5. **Rank and export**
   - Final CSV exported with all scores

---   

##  How Scoring Works

| Feature               | Weight |
|-----------------------|--------|
| Insured %             | 25%    |
| Broadband %           | 20%    |
| Median Income         | 20%    |
| Facility Availability | 25%    |
| Travel Time (inverted)| 10%    |

Score range: **0–100**  
Higher score = better access to healthcare.

---

##  Sample Output

Top 10 States:

| State   | Score |
|---------|-------|
| Vermont | 92.1  |
| New York| 90.4  |
| ...     | ...   |

Bottom 10 States:

| State     | Score |
|-----------|-------|
| Mississippi | 62.3 |
| Alabama     | 64.0 |
| ...         | ...   |

---
##  Tools & Libraries

- `pandas`, `numpy`
- `matplotlib`, `seaborn`
- `openrouteservice` (API)
- `VS Code`, `Jupyter Notebook`
- GitHub for version control

---

---

### Machine Learning Model (Random Forest)
We used a **Random Forest Regressor** to learn the importance of each feature in predicting access scores based on the manually defined scores.

🔍 **Why Random Forest?**
- It's interpretable: we can extract **feature importances**
- Handles non-linearity and interactions between features
- Doesn't require feature scaling

The model was trained using:
- Features: insured %, broadband %, income, facilities, travel time
- Target: manually defined access scores

We then used the trained model to:
- Predict scores for each state
- Identify which features contribute the most/least to access

---

###  Streamlit Dashboard
An interactive Streamlit app lets users:
- Visualize access scores across U.S. states
- Select a state and compare **manual vs. model-predicted** scores
- View contribution of each feature
- See **recommendations** on which factors to improve

---

##  Running the App

To run the dashboard:
```bash
 "streamlit run app/streamlit_app.py"


---
## Future Work

- Add interactive dashboard (Streamlit or Dash) -> done
- Expand to county-level access scoring
- Add provider availability by specialty

---

## Maintainer

Made with by [Manika Sharma](https://github.com/manika26)

---
