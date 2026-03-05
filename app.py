import streamlit as st
import pandas as pd

st.markdown("""
<style>

/* Page background */
.main {
    background-color: #f5f7fb;
}

/* Section headers */
h1, h2, h3 {
    color: #1f2c44;
}

/* Cards */
.block-container {
    padding-top: 2rem;
}

/* Quote summary box */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    border: 1px solid #e3e6ef;
    padding: 10px;
}

/* Buttons */
.stButton>button {
    border-radius: 8px;
    background-color: #2f6fed;
    color: white;
    font-weight: bold;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-size: 28px;
}

/* Input boxes */
input {
    border-radius: 6px;
}

</style>
""", unsafe_allow_html=True)
st.image("aks logo.jpg", width=200)

st.title("Fabrication Quote Builder")
st.caption("Material • Labour • Galvanising Estimator")
st.divider()

steel_sections = {
    "50x50x3 SHS": 4.31,
    "75x75x3 SHS": 6.58,
    "100x100x4 SHS": 11.9,
    "125x125x5 SHS": 18.6,
    "150x150x5 SHS": 22.7,
    "200x200x6 SHS": 36.0
}

st.header("Client Details")

client = st.text_input("Client Name")
job = st.text_input("Job Description")

st.header("Steel price guide")

section = st.selectbox(
    "Select Section Size",
    list(steel_sections.keys())
)

length = st.number_input("Length (metres)", min_value=0.0)

kg_per_m = steel_sections[section]

weight = kg_per_m * length

tonnes = weight / 1000

steel_price_per_tonne = 3600

steel_cost = tonnes * steel_price_per_tonne

st.write(f"Weight: {weight:.2f} kg")
st.write(f"Steel Cost: ${steel_cost:.2f}")



st.header("Labour")

workshop_hours = st.number_input("Workshop Hours", min_value=0.0)
onsite_hours = st.number_input("Onsite Hours", min_value=0.0)

workshop_rate = 140
onsite_rate = 150

workshop_cost = workshop_hours * workshop_rate
onsite_cost = onsite_hours * onsite_rate

st.header("Welding")

joint_count = st.number_input("Number of Joints", min_value=0)

cost_per_joint = st.number_input("Cost per Joint ($)", value=5.0)

weld_length = st.number_input("Total Weld Length (metres)", min_value=0.0)

cost_per_metre = st.number_input("Cost per Metre of Weld ($)", value=12.0)

joint_cost = joint_count * cost_per_joint

weld_cost = weld_length * cost_per_metre

st.header("Externally sourced material allowance")

materials = st.number_input("Material Cost ($)", min_value=0.0)

st.header("Steel Materials")

steel_items = []

num_items = st.number_input("Number of Steel Sections", min_value=1, step=1)

for i in range(int(num_items)):
    
    st.subheader(f"Steel Item {i+1}")
    
    section = st.selectbox(
        f"Section Size {i+1}",
        list(steel_sections.keys()),
        key=f"section{i}"
    )
    
    length = st.number_input(
        f"Length (m) {i+1}",
        min_value=0.0,
        key=f"length{i}"
    )

    kg_per_m = steel_sections[section]
    
    weight = kg_per_m * length
    
    tonnes = weight / 1000
    
    steel_price_per_tonne = 3600
    
    cost = tonnes * steel_price_per_tonne
    
    steel_items.append({
    "description": f"{section} x {length}m",
    "weight": weight,
    "cost": cost
})
    
steel_cost = sum(item["cost"] for item in steel_items)

section_summary = {}

for item in steel_items:
    desc = item["description"].split(" x ")[0]
    length = float(item["description"].split(" x ")[1].replace("m",""))

    if desc not in section_summary:
        section_summary[desc] = {"length": 0, "weight": 0}

    section_summary[desc]["length"] += length
    section_summary[desc]["weight"] += item["weight"]

total_weight = sum(item["weight"] for item in steel_items)

tonnes = total_weight / 1000

galv_price_per_tonne = 1800

galv_cost = tonnes * galv_price_per_tonne

st.header("Extras")

extras = st.number_input("Consumables / Extras ($)", min_value=0.0)

total = workshop_cost + onsite_cost + materials + extras + joint_cost + weld_cost + steel_cost + galv_cost

st.header("Pricing")

markup = st.slider(
    "Profit / Markup (%)",
    min_value=0,
    max_value=50,
    value=20
)

final_total = total * (1 + markup / 100)

st.header("Quote Summary")

data = {
    "Item": [
        "Workshop Labour",
        "Onsite Labour",
        "Steel",
        "Total Steel Weight (kg)",
        "Hot Dip Galvanising",
        "Materials",
        "Extras"
    ],
    "Cost": [
        workshop_cost,
        onsite_cost,
        steel_cost,
        total_weight,
        galv_cost,
        materials,
        extras
    ]
}

df = pd.DataFrame(data)

st.table(df)

st.header("Steel Breakdown")

breakdown_data = {
    "Section": [],
    "Total Length (m)": [],
    "Total Weight (kg)": []
}

for section, values in section_summary.items():
    breakdown_data["Section"].append(section)
    breakdown_data["Total Length (m)"].append(round(values["length"],2))
    breakdown_data["Total Weight (kg)"].append(round(values["weight"],2))

breakdown_df = pd.DataFrame(breakdown_data)

st.table(breakdown_df)

st.subheader(f"Cost Before Markup: ${total:,.2f}")
st.subheader(f"Final Quote (with {markup}% markup): ${final_total:,.2f}")

if st.button("Generate Quote"):
    st.success("Quote Generated")