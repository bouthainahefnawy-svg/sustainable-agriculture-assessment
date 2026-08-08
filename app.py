import streamlit as st
import pandas as pd
import os


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Sustainable Agriculture Assessment",
    page_icon="🌱",
    layout="wide"
)


# =========================================================
# FILE NAME
# =========================================================

EXCEL_FILE = "Sustainability_Model.xlsx"


# =========================================================
# LOAD DATABASE
# =========================================================

database = pd.read_excel(
    EXCEL_FILE,
    sheet_name="database"
)

database.columns = database.columns.str.strip()

database["Indicator"] = (
    database["Indicator"]
    .astype(str)
    .str.strip()
)


# =========================================================
# LOAD PREVIOUS ASSESSMENT VALUES
# =========================================================

previous_inputs = {}

try:

    assessment = pd.read_excel(
        EXCEL_FILE,
        sheet_name="assessment"
    )

    assessment.columns = assessment.columns.str.strip()

    if "Indicator" in assessment.columns and "Input" in assessment.columns:

        for _, row in assessment.iterrows():

            indicator_name = str(
                row["Indicator"]
            ).strip().lower()

            if indicator_name == "nan":
                continue

            input_value = row["Input"]

            if pd.isna(input_value):
                continue

            previous_inputs[indicator_name] = input_value

except Exception:

    previous_inputs = {}


# =========================================================
# NUMERIC SCORE
# =========================================================

def calculate_numeric_score(indicator, value):

    data = database[
        database["Indicator"].str.lower()
        == indicator.lower()
    ].copy()

    data["Min"] = pd.to_numeric(
        data["Min"],
        errors="coerce"
    )

    data["Max"] = pd.to_numeric(
        data["Max"],
        errors="coerce"
    )

    data["Score"] = pd.to_numeric(
        data["Score"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["Min", "Max", "Score"]
    )

    for _, row in data.iterrows():

        minimum = row["Min"]
        maximum = row["Max"]
        score = row["Score"]

        # -----------------------------------------
        # Exact value
        # Example: 0 - 0
        # -----------------------------------------

        if minimum == maximum:

            if value == minimum:
                return score

        # -----------------------------------------
        # Normal range
        # Example: 0 - 25
        # -----------------------------------------

        elif minimum < maximum:

            if value >= minimum and value < maximum:
                return score

        # -----------------------------------------
        # Reverse range
        # Example: 150 - 100
        # Hardpan Layers
        # -----------------------------------------

        elif minimum > maximum:

            if value <= minimum and value > maximum:
                return score

    # -----------------------------------------
    # Include final upper boundary
    # -----------------------------------------

    if len(data) > 0:

        last_row = data.iloc[-1]

        minimum = last_row["Min"]
        maximum = last_row["Max"]
        score = last_row["Score"]

        if minimum < maximum:

            if value == maximum:
                return score

        elif minimum > maximum:

            if value == maximum:
                return score

    return None


# =========================================================
# CATEGORY SCORE
# =========================================================

def calculate_category_score(indicator, value):

    data = database[
        database["Indicator"].str.lower()
        == indicator.lower()
    ].copy()

    data["Category"] = (
        data["Category"]
        .astype(str)
        .str.strip()
    )

    match = data[
        data["Category"].str.lower()
        == value.lower()
    ]

    if len(match) > 0:

        return float(
            match.iloc[0]["Score"]
        )

    return None


# =========================================================
# MAIN INDEX
# =========================================================

def normalize_name(name):
    name = str(name).lower().strip()
    
    # Remove spaces, underscores and hyphens
    name = name.replace(" ", "")
    name = name.replace("_", "")
    name = name.replace("-", "")
    
    # Handle common singular/plural differences
    if name.endswith("s"):
        name = name[:-1]
    
    return name


def calculate_main_index(scores, indicators):

    values = []

    for indicator in indicators:

        target = normalize_name(indicator)

        found = False

        for key, score in scores.items():

            current = normalize_name(key)

            if current == target:

                values.append(score / 100.0)

                found = True
                break

        if not found:
            return None

    if len(values) != len(indicators):
        return None

    index = 1.0

    for value in values:
        index *= value

    return index

# =========================================================
# RATING
# =========================================================

def calculate_rating(index):

    if index is None:
        return None

    if index < 0.10:

        return "Very Low"

    elif index < 0.30:

        return "Low"

    elif index < 0.60:

        return "Moderate"

    else:

        return "High"


# =========================================================
# TITLE
# =========================================================

# =========================================================
# APP HEADER & SIDEBAR
# =========================================================

# Sidebar
st.sidebar.title("🌱 Sustainability")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Assessment",
        "📈 Results",
        "🌍 Overall Sustainability"
    ]
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Sustainable Agriculture Assessment System"
)


# =========================================================
# HOME PAGE
# =========================================================
# =========================================================
# PROFESSIONAL HOME PAGE
# =========================================================

if page == "🏠 Home":

    # -----------------------------------------------------
    # HERO SECTION
    # -----------------------------------------------------

        # -----------------------------------------------------
    # HERO SECTION
    # -----------------------------------------------------

    hero_html = """
<div style="background:linear-gradient(135deg,#1b5e20,#388e3c);padding:45px 40px;border-radius:22px;text-align:center;margin-bottom:30px;box-shadow:0 6px 18px rgba(0,0,0,0.12);">
<div style="font-size:48px;margin-bottom:10px;">🌱</div>
<div style="color:white;font-size:34px;font-weight:700;margin-bottom:12px;">Sustainable Agriculture<br>Assessment System</div>
<div style="color:#e8f5e9;font-size:18px;font-weight:400;">Integrated Assessment of Agricultural Land Sustainability</div>
</div>
"""

    st.markdown(
        hero_html,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # INTRODUCTION
    # -----------------------------------------------------

       # -----------------------------------------------------
    # INTRODUCTION
    # -----------------------------------------------------

    intro_html = """
<div style="background:#ffffff;padding:25px 30px;border-radius:16px;border:1px solid #e0e0e0;margin-bottom:30px;">
<h3 style="color:#1b5e20;margin-bottom:10px;">About the Assessment System</h3>
<p style="font-size:16px;line-height:1.7;color:#555555;">This system provides an integrated assessment of agricultural land sustainability based on five major dimensions. The assessment combines multiple environmental and land-related indicators to generate individual sustainability indices and an overall sustainability index.</p>
</div>
"""

    st.markdown(
        intro_html,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # FIVE DIMENSIONS
    # -----------------------------------------------------

        # -----------------------------------------------------
    # FIVE SUSTAINABILITY DIMENSIONS
    # -----------------------------------------------------

    st.subheader("🌍 Sustainability Dimensions")

    dimensions = [
        ("🌱", "Soil", "Soil quality & suitability"),
        ("💧", "Water", "Water availability & quality"),
        ("☀️", "Climate", "Climatic conditions"),
        ("🛡️", "Protection", "Land protection conditions"),
        ("🏗️", "Infrastructure", "Accessibility & services")
    ]

    col1, col2, col3, col4, col5 = st.columns(5)

    for column, dimension in zip(
        [col1, col2, col3, col4, col5],
        dimensions
    ):

        icon, title, description = dimension

        with column:

            st.markdown(
                f"""
<div style="background:#f8faf8;border:1px solid #d8e6d8;border-radius:16px;padding:22px 12px;text-align:center;min-height:150px;">

<div style="font-size:34px;margin-bottom:8px;">{icon}</div>

<div style="font-size:18px;font-weight:700;color:#2e7d32;margin-bottom:8px;">{title}</div>

<div style="font-size:13px;color:#666666;line-height:1.5;">{description}</div>

</div>
""",
                unsafe_allow_html=True
            )

    # -----------------------------------------------------
    # START ASSESSMENT MESSAGE
    # -----------------------------------------------------

        # -----------------------------------------------------
    # START ASSESSMENT MESSAGE
    # -----------------------------------------------------

    st.markdown(
        """
<div style="background:#f1f8e9;border:1px solid #dcedc8;border-radius:16px;padding:24px;text-align:center;margin-top:30px;">

<div style="font-size:20px;font-weight:600;color:#33691e;">
Ready to assess your land?
</div>

<div style="font-size:14px;color:#666666;margin-top:8px;">
Use the navigation menu to start the sustainability assessment.
</div>

</div>
""",
        unsafe_allow_html=True
    )

# =========================================================
# ASSESSMENT PAGE
# =========================================================

elif page == "📊 Assessment":

    st.title(
        "📊 Sustainability Assessment"
    )

    st.write(
        "Enter or select the values of the sustainability indicators."
    )

    st.header("Assessment")

# =========================================================
# GET INDICATORS FROM DATABASE
# =========================================================

valid_indicators = []

for indicator in database["Indicator"].unique():

    name = str(indicator).strip()

    # Ignore separator rows
    if name == "" or name.startswith("."):
        continue

    valid_indicators.append(name)


# Remove duplicates
valid_indicators = list(
    dict.fromkeys(valid_indicators)
)


# =========================================================
# USER INPUTS
# =========================================================

# =========================================================
# USER INPUTS
# =========================================================

scores = {}

current_inputs = {}


# =========================================================
# INDICATOR GROUPS
# =========================================================

indicator_groups = {

    "🌱 Soil Assessment": [
        "ece",
        "soil depth",
        "texture",
        "caco3",
        "cec",
        "slope",
        "ph",
        "surface fragments",
        "surface fragment",
        "hardpan layers",
        "hardpan layer",
        "om"
    ],

    "🛡️ Protection Assessment": [
        "erosion",
        "flooding",
        "ndvi"
    ],

    "☀️ Climate Assessment": [
        "rainfall",
        "evapotranspiration",
        "wind speed",
        "temperature"
    ],

    "🏗️ Infrastructure Assessment": [
        "proximity to roads",
        "proximity to markets",
        "proximity to service centers",
        "energy availability"
    ],

    "💧 Water Assessment": [
        "water availability",
        "water quality"
    ]
}


# =========================================================
# DISPLAY INDICATORS BY GROUP
# =========================================================

for group_name, group_indicators in indicator_groups.items():

    st.markdown("---")

    st.header(group_name)

    for indicator in valid_indicators:

        normalized_indicator = normalize_name(
            indicator
        )

        # Check whether this indicator belongs
        # to the current group

        belongs_to_group = False

        for group_indicator in group_indicators:

            if normalize_name(group_indicator) == normalized_indicator:

                belongs_to_group = True
                break

        if not belongs_to_group:
            continue


        data = database[
            database["Indicator"].str.lower()
            == indicator.lower()
        ].copy()


        if len(data) == 0:
            continue


        # =================================================
        # INPUT TYPE
        # =================================================

        input_type = (
            data["Input Type"]
            .astype(str)
            .str.strip()
            .iloc[0]
            .lower()
        )


        # =================================================
        # NUMERIC INPUT
        # =================================================

        if input_type == "numeric":

            previous_value = previous_inputs.get(
                indicator.lower(),
                0.0
            )

            try:

                previous_value = float(
                    previous_value
                )

            except:

                previous_value = 0.0


            state_key = f"value_{indicator}"


            if state_key not in st.session_state:

                st.session_state[state_key] = (
                    previous_value
                )


            value = st.number_input(
                f"Enter {indicator}:",
                min_value=0.0,
                step=0.1,
                key=state_key
            )


            current_inputs[indicator] = value


            score = calculate_numeric_score(
                indicator,
                value
            )


            if score is not None:

                scores[indicator] = score

                st.success(
                    f"{indicator} Score = {score:g}"
                )

            else:

                st.warning(
                    f"No classification found for {indicator}."
                )


        # =================================================
        # CATEGORY INPUT
        # =================================================

        elif input_type == "category":

            categories = (
                data["Category"]
                .dropna()
                .astype(str)
                .str.strip()
                .unique()
                .tolist()
            )


            previous_value = previous_inputs.get(
                indicator.lower(),
                None
            )


            default_index = 0


            if previous_value is not None:

                previous_text = str(
                    previous_value
                ).strip().lower()


                for i, category in enumerate(categories):

                    if category.lower() == previous_text:

                        default_index = i

                        break


            state_key = f"value_{indicator}"


            if state_key not in st.session_state:

                st.session_state[state_key] = (
                    categories[default_index]
                )


            selected = st.selectbox(
                f"Select {indicator}:",
                categories,
                key=state_key
            )


            current_inputs[indicator] = selected


            score = calculate_category_score(
                indicator,
                selected
            )


            if score is not None:

                scores[indicator] = score

                st.success(
                    f"{indicator} Score = {score:g}"
                )


# =========================================================
# MAIN INDICATOR GROUPS
# =========================================================


# ---------------------------------------------------------
# SOIL
# ---------------------------------------------------------

soil_indicators = [
    "ece",
    "soil depth",
    "texture",
    "caco3",
    "cec",
    "slope",
    "ph",
    "surface fragment",
    "hardpan layer",
    "om"
]


# ---------------------------------------------------------
# PROTECTION
# ---------------------------------------------------------

protection_indicators = [

    "erosion",
    "flooding",
    "ndvi"

]


# ---------------------------------------------------------
# CLIMATE
# ---------------------------------------------------------

climate_indicators = [

    "rainfall",
    "evapotranspiration",
    "wind speed",
    "temperature"

]


# ---------------------------------------------------------
# INFRASTRUCTURE
# ---------------------------------------------------------

infrastructure_indicators = [

    "proximity to roads",
    "proximity to markets",
    "proximity to service centers",
    "energy availability"

]


# ---------------------------------------------------------
# WATER
# ---------------------------------------------------------

water_indicators = [

    "water availability",
    "water quality"

]


# =========================================================
# CALCULATE FIVE MAIN INDICES
# =========================================================

soil_index = calculate_main_index(
    scores,
    soil_indicators
)


protection_index = calculate_main_index(
    scores,
    protection_indicators
)


climate_index = calculate_main_index(
    scores,
    climate_indicators
)


infrastructure_index = calculate_main_index(
    scores,
    infrastructure_indicators
)


water_index = calculate_main_index(
    scores,
    water_indicators
)


# =========================================================
# FIVE RATINGS
# =========================================================

soil_rating = calculate_rating(
    soil_index
)


protection_rating = calculate_rating(
    protection_index
)


climate_rating = calculate_rating(
    climate_index
)


infrastructure_rating = calculate_rating(
    infrastructure_index
)


water_rating = calculate_rating(
    water_index
)


# =========================================================
# DISPLAY FIVE MAIN INDICES
# =========================================================
# =========================================================
# OVERALL SUSTAINABILITY INDEX
# =========================================================

overall_index = None

if (
    soil_index is not None
    and protection_index is not None
    and climate_index is not None
    and infrastructure_index is not None
    and water_index is not None
):

    overall_index = (
        soil_index
        * protection_index
        * climate_index
        * infrastructure_index
        * water_index
    )


# =========================================================
# OVERALL SUSTAINABILITY RATING
# =========================================================

overall_rating = calculate_rating(
    overall_index
)
# =========================================================
# RESULTS DASHBOARD
# =========================================================

if page == "📈 Results":

    st.title("📊 Sustainability Results Dashboard")

    st.write(
        "Integrated assessment results for the five main "
        "sustainability dimensions."
    )

    st.markdown("---")
    # =====================================================
    # BAR CHART
    # =====================================================
# =====================================================
# CHARTS SECTION
# =====================================================

st.markdown("---")

st.subheader("📊 Sustainability Visualization")

chart_col1, chart_col2 = st.columns(2)


# =====================================================
# BAR CHART
# =====================================================

with chart_col1:

    st.markdown("### 📊 Main Indicators Comparison")

    chart_data = pd.DataFrame({
        "Indicator": [
            "Soil",
            "Protection",
            "Climate",
            "Infrastructure",
            "Water"
        ],
        "Index": [
            soil_index,
            protection_index,
            climate_index,
            infrastructure_index,
            water_index
        ]
    })

    chart_data = chart_data.dropna()

    st.bar_chart(
        chart_data.set_index("Indicator"),
        y="Index"
    )


# =====================================================
# RADAR CHART
# =====================================================

with chart_col2:

    st.markdown("### 🌐 Sustainability Profile")

    import plotly.graph_objects as go

    radar_labels = [
        "Soil",
        "Protection",
        "Climate",
        "Infrastructure",
        "Water"
    ]

    radar_values = [
        soil_index,
        protection_index,
        climate_index,
        infrastructure_index,
        water_index
    ]

    radar_values = [
        value if value is not None else 0
        for value in radar_values
    ]

    radar_labels_closed = (
        radar_labels + [radar_labels[0]]
    )

    radar_values_closed = (
        radar_values + [radar_values[0]]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=radar_values_closed,
            theta=radar_labels_closed,
            fill="toself",
            name="Sustainability"
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=False,
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    # =====================================================
    # RADAR CHART
    # =====================================================

    
    # =====================================================
    # MAIN INDICATOR CARDS
    # =====================================================
    # =====================================================
    # OVERALL SUSTAINABILITY HERO CARD
    # =====================================================

    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
            padding: 30px;
            border-radius: 18px;
            text-align: center;
            margin-bottom: 30px;
            border: 1px solid #c8e6c9;
        ">
            <div style="
                font-size: 22px;
                font-weight: 600;
                color: #2e7d32;
            ">
                🌍 Overall Sustainability
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if overall_index is not None:

        overall_card = f"""
<div style="
background-color:#f1f8e9;
border:1px solid #c8e6c9;
border-radius:18px;
padding:30px;
text-align:center;
margin:10px 0 30px 0;
">

<div style="
font-size:52px;
font-weight:700;
color:#1b5e20;
margin-bottom:10px;
">
{overall_index:.3f}
</div>

<div style="
font-size:22px;
font-weight:600;
color:#2e7d32;
margin-bottom:8px;
">
{overall_rating}
</div>

<div style="
font-size:14px;
color:#666666;
">
Overall Sustainability Index
</div>

</div>
"""

        st.markdown(
            overall_card,
            unsafe_allow_html=True
        )

# =====================================================
# FUNCTION FOR INDICATOR CARD
# =====================================================

# =====================================================
# FUNCTION FOR INDICATOR CARD
# =====================================================

def indicator_card(icon, name, index, rating):

    if index is None:

        index_text = "N/A"
        rating_text = "Not available"

        card_color = "#f5f5f5"
        border_color = "#dddddd"

    else:

        index_text = f"{index:.3f}"
        rating_text = rating

        if rating == "Very Low":

            card_color = "#ffebee"
            border_color = "#ef9a9a"

        elif rating == "Low":

            card_color = "#fff3e0"
            border_color = "#ffcc80"

        elif rating == "Moderate":

            card_color = "#fffde7"
            border_color = "#fff176"

        elif rating == "High":

            card_color = "#e8f5e9"
            border_color = "#a5d6a7"

        else:

            card_color = "#f5f5f5"
            border_color = "#dddddd"


    card_html = f"""
<div style="
background-color:{card_color};
border:1px solid {border_color};
border-radius:16px;
padding:20px;
min-height:175px;
text-align:center;
box-shadow:0 2px 6px rgba(0,0,0,0.08);
">

<div style="
font-size:32px;
margin-bottom:5px;
">
{icon}
</div>

<div style="
font-size:18px;
font-weight:600;
color:#303030;
margin-bottom:12px;
">
{name}
</div>

<div style="
font-size:32px;
font-weight:700;
color:#1f2937;
">
{index_text}
</div>

<div style="
font-size:15px;
font-weight:600;
margin-top:8px;
color:#555555;
">
{rating_text}
</div>

</div>
"""

    st.markdown(
        card_html,
        unsafe_allow_html=True
    )
    # =====================================================
    # OVERALL SUSTAINABILITY
    # =====================================================

    st.markdown("---")

    st.subheader("🌍 Overall Sustainability")


    if overall_index is not None:

        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            st.write("")

        with col2:

            st.metric(
                "Overall Sustainability Index",
                f"{overall_index:.3f}"
            )

            st.success(
                f"Overall Rating: {overall_rating}"
            )

        with col3:
            st.write("")


    else:

        st.warning(
            "Complete all indicators to calculate "
            "the Overall Sustainability Index."
        )


    # =====================================================
    # RESULTS TABLE
    # =====================================================

    st.markdown("---")

    st.subheader("📋 Summary of Results")


    results_data = []

    if soil_index is not None:

        results_data.append([
            "Soil",
            soil_index,
            soil_rating
        ])


    if protection_index is not None:

        results_data.append([
            "Protection",
            protection_index,
            protection_rating
        ])


    if climate_index is not None:

        results_data.append([
            "Climate",
            climate_index,
            climate_rating
        ])


    if infrastructure_index is not None:

        results_data.append([
            "Infrastructure",
            infrastructure_index,
            infrastructure_rating
        ])


    if water_index is not None:

        results_data.append([
            "Water",
            water_index,
            water_rating
        ])


    if overall_index is not None:

        results_data.append([
            "Overall Sustainability",
            overall_index,
            overall_rating
        ])


    if len(results_data) > 0:

        results_table = pd.DataFrame(
            results_data,
            columns=[
                "Indicator",
                "Index",
                "Rating"
            ]
        )
        results_table["Index"] = results_table[
            "Index"
        ].round(3)

        st.dataframe(
            results_table,
            use_container_width=True,
            hide_index=True
        )
        
    
# =========================================================
# ASSESSMENT SUMMARY
# =========================================================

st.divider()

st.header("📊 Assessment Summary")


if len(scores) > 0:

    results = pd.DataFrame(
        list(scores.items()),
        columns=["Indicator", "Score"]
    )

    st.dataframe(
        results,
        use_container_width=True
    )