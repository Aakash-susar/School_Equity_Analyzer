import streamlit as st
import pandas as pd
import joblib

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="School Equity Analyzer",
    page_icon="🏫",
    layout="wide"
)

# ==================================================
# LOAD MODELS
# ==================================================

regression_model = joblib.load(
    "../models/regression_model.pkl"
)

kmeans_model = joblib.load(
    "../models/kmeans_model.pkl"
)

scaler = joblib.load(
    "../models/scaler.pkl"
)

cluster_scaler = joblib.load(
    "../models/cluster_scaler.pkl"
)

# ==================================================
# HELPER FUNCTIONS
# ==================================================

def predict_equity(df):

    scaled_df = scaler.transform(df)

    return regression_model.predict(
        scaled_df
    )[0]


def get_risk_category(score):

    if score < 40:
        return "🔴 High Risk"

    elif score < 70:
        return "🟠 Medium Risk"

    return "🟢 Low Risk"


def get_recommendations(score):

    if score < 40:
        return [
            "Increase school funding",
            "Improve internet accessibility",
            "Reduce student-teacher ratio",
            "Provide academic support programs",
            "Implement dropout prevention initiatives"
        ]

    elif score < 70:
        return [
            "Monitor student performance",
            "Improve digital learning resources",
            "Strengthen teacher support programs",
            "Enhance student engagement"
        ]

    return [
        "Maintain current performance",
        "Continue digital access initiatives",
        "Monitor school outcomes regularly",
        "Expand enrichment opportunities"
    ]

# ==================================================
# TITLE
# ==================================================

st.title(
    "🏫 School Equity Analyzer"
)

st.markdown(
    """
Analyze a school and predict:

✅ Equity Score

✅ Risk Category

✅ School Segment

✅ Improvement Recommendations
"""
)

# ==================================================
# SIDEBAR INPUTS
# ==================================================

st.sidebar.header(
    "School Information"
)

funding = st.sidebar.number_input(
    "Funding Per Student ($)",
    min_value=5000,
    max_value=35000,
    value=15000
)

teacher_ratio = st.sidebar.slider(
    "Student Teacher Ratio",
    10,
    30,
    18
)

low_income = st.sidebar.slider(
    "Low Income Percentage",
    0,
    100,
    40
)

minority = st.sidebar.slider(
    "Minority Percentage",
    0,
    100,
    40
)

internet = st.sidebar.slider(
    "Internet Access Percentage",
    50,
    100,
    80
)

school_type = st.sidebar.selectbox(
    "School Type",
    ["Public", "Private"]
)

grade_level = st.sidebar.selectbox(
    "Grade Level",
    ["Elementary", "Middle", "High"]
)

# ==================================================
# ENCODING
# ==================================================

school_type_private = (
    1 if school_type == "Private"
    else 0
)

school_type_public = (
    1 if school_type == "Public"
    else 0
)

grade_level_high = (
    1 if grade_level == "High"
    else 0
)

grade_level_middle = (
    1 if grade_level == "Middle"
    else 0
)

# ==================================================
# PREDICTION
# ==================================================

if st.button("🚀 Analyze School"):

    input_df = pd.DataFrame({
        "funding_per_student_usd": [funding],
        "student_teacher_ratio": [teacher_ratio],
        "percent_low_income": [low_income],
        "percent_minority": [minority],
        "internet_access_percent": [internet],
        "school_type_Private": [school_type_private],
        "school_type_Public": [school_type_public],
        "grade_level_High": [grade_level_high],
        "grade_level_Middle": [grade_level_middle]
    })

    # ==========================================
    # EQUITY PREDICTION
    # ==========================================

    equity_score = predict_equity(
        input_df
    )

    risk_category = get_risk_category(
        equity_score
    )

    # ==========================================
    # WHAT IF ANALYSIS
    # ==========================================

    improvements = {}

    funding_df = input_df.copy()

    funding_df["funding_per_student_usd"] = 30000

    funding_score = predict_equity(
        funding_df
    )

    improvements["Increase Funding"] = round(
        funding_score - equity_score,
        2
    )

    internet_df = input_df.copy()

    internet_df["internet_access_percent"] = 100

    internet_score = predict_equity(
        internet_df
    )

    improvements["Improve Internet Access"] = round(
        internet_score - equity_score,
        2
    )

    teacher_df = input_df.copy()

    teacher_df["student_teacher_ratio"] = 10

    teacher_score = predict_equity(
        teacher_df
    )

    improvements["Reduce Student-Teacher Ratio"] = round(
        teacher_score - equity_score,
        2
    )

    income_df = input_df.copy()

    income_df["percent_low_income"] = 0

    income_score = predict_equity(
        income_df
    )

    improvements["Support Low-Income Students"] = round(
        income_score - equity_score,
        2
    )

    best_action = max(
    improvements,
    key=improvements.get
)

    best_gain = improvements[
        best_action
    ]

    if best_gain <= 0:

        best_action = (
            "No Immediate Intervention Required"
        )

    # ==========================================
    # CLUSTER PREDICTION
    # ==========================================

    estimated_test_score = max(
        40,
        min(
            100,
            equity_score * 0.95
        )
    )

    estimated_dropout = max(
        0.5,
        min(
            15,
            15 - (equity_score / 8)
        )
    )

    cluster_df = pd.DataFrame({
        "funding_per_student_usd": [funding],
        "avg_test_score_percent": [estimated_test_score],
        "student_teacher_ratio": [teacher_ratio],
        "internet_access_percent": [internet],
        "dropout_rate_percent": [estimated_dropout],
        "equity_score": [equity_score]
    })

    cluster_scaled = cluster_scaler.transform(
        cluster_df
    )

    cluster = kmeans_model.predict(
        cluster_scaled
    )[0]

    cluster_names = {
        0: "Developing Schools",
        1: "Balanced Schools",
        2: "High Equity Schools",
        3: "High Risk Schools"
    }

    school_segment = cluster_names[
        cluster
    ]

    # ==========================================
    # RESULTS
    # ==========================================

    st.header(
        "📊 Analysis Results"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Equity Score",
            f"{equity_score:.2f}"
        )

    with col2:
        st.metric(
            "Risk Category",
            risk_category
        )

    with col3:
        st.metric(
            "School Segment",
            school_segment
        )

    # ==========================================
    # SCHOOL ASSESSMENT
    # ==========================================

    st.subheader(
        "📈 School Assessment"
    )

    if equity_score >= 70:

        st.success(
            "This school demonstrates strong educational equity and resource availability."
        )

    elif equity_score >= 40:

        st.warning(
            "This school requires moderate improvement in educational outcomes."
        )

    else:

        st.error(
            "This school is at significant risk and may require immediate intervention."
        )

    # ==========================================
    # BASIC RECOMMENDATIONS
    # ==========================================

    st.subheader(
        "💡 General Recommendations"
    )

    recommendations = get_recommendations(
        equity_score
    )

    for rec in recommendations:

        st.write(
            f"✅ {rec}"
        )

    # ==========================================
    # WHAT IF ANALYSIS
    # ==========================================

    st.subheader(
        "📈 What-If Analysis"
    )

    what_if_df = pd.DataFrame({
        "Intervention": list(
            improvements.keys()
        ),
        "Potential Equity Gain": list(
            improvements.values()
        )
    })

    st.dataframe(
        what_if_df,
        use_container_width=True
    )

    # ==========================================
    # AI RECOMMENDATION
    # ==========================================

    st.subheader(
        "🤖 Recommendation Engine"
    )

    if best_gain <= 0:

        st.success(
            """
    🏆 Excellent Performance

    The school is already operating near
    optimal conditions.

    No major intervention is currently required.
    """
        )

    else:

        st.success(
            f"""
    🏆 Recommended Action:
    {best_action}

    📈 Expected Equity Improvement:
    +{best_gain} points
    """
        )