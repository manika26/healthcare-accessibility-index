import streamlit as st
import pandas as pd
import plotly.express as px
import json
import pickle
import plotly.io as pio

# ----------------------
# Load data & resources
# ----------------------
df = pd.read_csv("/Users/manika/Desktop/Python : Learning/healthcare-accessibility-index/data/clean/merge_healthcare_accessibility_index.csv")

# Load manual feature weights
with open("/Users/manika/Desktop/Python : Learning/healthcare-accessibility-index/data/clean/manual_feature_weights.json") as f:
    manual_weights = json.load(f)

# Load ML feature importances
with open("/Users/manika/Desktop/Python : Learning/healthcare-accessibility-index/data/clean/ml_feature_importances.json") as f:
    ml_weights = json.load(f)

# Load trained model
with open("/Users/manika/Desktop/Python : Learning/healthcare-accessibility-index/model/rf_model.pkl", "rb") as f:
    rf_model = pickle.load(f)

# ----------------------
# Streamlit UI
# ----------------------
st.set_page_config(layout="wide")
st.title("U.S. Statewise Healthcare Accessibility Explorer")
st.markdown("Compare **manual vs machine-learned access scores** and identify areas for improvement by state.")

# Load prebuilt figure
fig = pio.read_json("data/final_choropleth_map.json")
st.plotly_chart(fig, use_container_width=True)

# State selection
selected_state = st.selectbox("Select a State to Explore", df['state'].unique())
state_row = df[df['state'] == selected_state].iloc[0]

st.markdown("---")
st.header(f"Access Scores for {selected_state}")

# Compute model score using loaded model
features = list(ml_weights.keys())
input_features = state_row[features].values.reshape(1, -1)
predicted_score = rf_model.predict(input_features)[0]

st.markdown(f"- **Manual Access Score:** `{state_row['access_score']:.2f}`")
st.markdown(f"- **Model Predicted Score:** `{predicted_score:.2f}`")

# ----------------------
# Feature Contribution Table
# ----------------------
st.markdown("---")
st.subheader("Feature Contributions")

# Create comparison table
data = []
for feat in features:
    manual_contrib = state_row[feat] * manual_weights.get(feat, 0)
    model_contrib = state_row[feat] * ml_weights.get(feat, 0)
    data.append({
        "Feature": feat,
        "Raw Value": state_row[feat],
        "Manual given Weight": manual_weights.get(feat, 0),
        "Manual Contribution": manual_contrib,
        "Model given Weight": ml_weights.get(feat, 0),
        "Model Contribution": model_contrib
    })

contrib_df = pd.DataFrame(data).sort_values("Model Contribution", ascending=False)
st.dataframe(contrib_df.style.format("{}"), use_container_width=True)

# ----------------------
# Suggestion Block
# ----------------------
st.markdown("---")
st.subheader("Suggested Areas for Improvement")

lowest_feats = contrib_df.nsmallest(2, "Raw Value")["Feature"].tolist()
st.markdown(f"To improve healthcare access in **{selected_state}**, consider focusing on: **{lowest_feats[0]}** and **{lowest_feats[1]}** based on current performance.")
