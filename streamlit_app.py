import streamlit as st
import pandas as pd
import requests


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Satellite Population Intelligence",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONFIG
# ============================================================

API_URL = "http://127.0.0.1:8000"
DATA_FILE = "data/Indian_City_NightLights.csv"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #080d18;
    }

    /* Main container */
    .block-container {
        max-width: 1400px;
        padding-top: 30px;
        padding-bottom: 50px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0d1422;
        border-right: 1px solid #1e293b;
    }

    /* Headings */
    h1, h2, h3 {
        color: #f8fafc !important;
    }

    /* Normal text */
    p, label {
        color: #cbd5e1 !important;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background-color: #101827;
        border: 1px solid #1e293b;
        padding: 18px;
        border-radius: 14px;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: none;
        background-color: #2563eb;
        color: white;
        font-weight: 700;
        padding: 10px;
    }

    .stButton > button:hover {
        background-color: #1d4ed8;
        color: white;
    }

    /* Inputs */
    input {
        color: white !important;
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border: 1px solid #1e293b;
        border-radius: 12px;
    }

    /* Horizontal line */
    hr {
        border-color: #1e293b;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    data = pd.read_csv(DATA_FILE)

    return data


try:

    df = load_data()

except Exception as error:

    st.error(
        f"Could not load dataset: {error}"
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🛰️ ORBITAL")

    st.caption(
        "SATELLITE INTELLIGENCE PLATFORM"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "City Explorer",
            "Population AI",
            "Live Ingestion",
            "Analytics"
        ]
    )

    st.divider()

    st.markdown("### SYSTEM")

    st.write("🛰️ NASA VIIRS")
    st.write("🤖 Random Forest")
    st.write("⚡ FastAPI")
    st.write("🗄️ SQLite")

    st.divider()

    st.success("● API SYSTEM ONLINE")


# ============================================================
# TOP HEADER
# ============================================================

header1, header2 = st.columns(
    [5, 1]
)

with header1:

    st.markdown(
        "# 🛰️ Satellite Population Intelligence"
    )

    st.caption(
        "Real-time satellite observation processing, "
        "conflict resolution and AI-powered population estimation."
    )


with header2:

    st.success("● ONLINE")


st.divider()


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.subheader("Mission Overview")

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    total_cities = len(df)

    avg_brightness = df[
        "average_masked_mean"
    ].mean()

    max_brightness = df[
        "average_masked_max"
    ].max()

    min_brightness = df[
        "average_masked_min"
    ].min()


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "🏙️ Cities",
            f"{total_cities:,}"
        )


    with col2:

        st.metric(
            "💡 Average Brightness",
            f"{avg_brightness:.2f}"
        )


    with col3:

        st.metric(
            "☀️ Maximum Brightness",
            f"{max_brightness:.2f}"
        )


    with col4:

        st.metric(
            "🌑 Minimum Brightness",
            f"{min_brightness:.2f}"
        )


    st.divider()


    # --------------------------------------------------------
    # City selection
    # --------------------------------------------------------

    st.subheader("🏙️ City Analysis")


    cities = sorted(
        df["City"]
        .dropna()
        .astype(str)
        .unique()
    )


    selected_city = st.selectbox(
        "Select a city",
        cities
    )


    city_data = df[
        df["City"].astype(str)
        == selected_city
    ]


    if len(city_data) > 0:

        city = city_data.iloc[0]

        c1, c2, c3, c4 = st.columns(4)


        with c1:

            st.metric(
                "Latitude",
                f"{float(city['Latitude']):.4f}"
            )


        with c2:

            st.metric(
                "Longitude",
                f"{float(city['Longitude']):.4f}"
            )


        with c3:

            st.metric(
                "Night Light Mean",
                f"{float(city['average_masked_mean']):.2f}"
            )


        with c4:

            st.metric(
                "Night Light Max",
                f"{float(city['average_masked_max']):.2f}"
            )


    st.divider()


    # --------------------------------------------------------
    # Chart
    # --------------------------------------------------------

    st.subheader("💡 Night-Light Intensity")

    top_cities = (
        df.groupby("City")[
            "average_masked_mean"
        ]
        .mean()
        .sort_values(
            ascending=False
        )
        .head(15)
    )


    st.bar_chart(
        top_cities,
        height=400
    )


# ============================================================
# CITY EXPLORER
# ============================================================

elif page == "City Explorer":

    st.title("🏙️ City Explorer")

    st.caption(
        "Explore satellite characteristics of individual cities."
    )


    cities = sorted(
        df["City"]
        .dropna()
        .astype(str)
        .unique()
    )


    selected_city = st.selectbox(
        "Select City",
        cities
    )


    city = df[
        df["City"].astype(str)
        == selected_city
    ].iloc[0]


    st.header(selected_city)


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Latitude",
            f"{float(city['Latitude']):.4f}"
        )


    with col2:

        st.metric(
            "Longitude",
            f"{float(city['Longitude']):.4f}"
        )


    with col3:

        st.metric(
            "Mean Brightness",
            f"{float(city['average_masked_mean']):.2f}"
        )


    with col4:

        st.metric(
            "Maximum Brightness",
            f"{float(city['average_masked_max']):.2f}"
        )


    st.subheader("Night-Light Profile")


    profile = pd.DataFrame(
        {
            "Feature": [
                "Minimum",
                "Mean",
                "Maximum",
                "Standard Deviation"
            ],

            "Value": [
                city["average_masked_min"],
                city["average_masked_mean"],
                city["average_masked_max"],
                city["average_masked_stdDev"]
            ]
        }
    )


    st.dataframe(
        profile,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# POPULATION AI
# ============================================================

elif page == "Population AI":

    st.title("🤖 Population Intelligence")

    st.caption(
        "Estimate population using the trained Random Forest model."
    )


    cities = sorted(
        df["City"]
        .dropna()
        .astype(str)
        .unique()
    )


    selected_city = st.selectbox(
        "Select City",
        cities
    )


    city = df[
        df["City"].astype(str)
        == selected_city
    ].iloc[0]


    mean = float(
        city["average_masked_mean"]
    )

    maximum = float(
        city["average_masked_max"]
    )

    minimum = float(
        city["average_masked_min"]
    )

    std = float(
        city["average_masked_stdDev"]
    )


    brightness_range = maximum - minimum

    brightness_ratio = maximum / max(
        minimum,
        0.001
    )

    brightness_product = mean * maximum


    st.subheader("Satellite Features")


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "Mean",
            f"{mean:.2f}"
        )


    with c2:

        st.metric(
            "Maximum",
            f"{maximum:.2f}"
        )


    with c3:

        st.metric(
            "Minimum",
            f"{minimum:.2f}"
        )


    with c4:

        st.metric(
            "Std Dev",
            f"{std:.2f}"
        )


    st.divider()


    if st.button(
        "🤖 Generate Population Estimate"
    ):

        payload = {

            "average_masked_mean":
                mean,

            "average_masked_max":
                maximum,

            "average_masked_min":
                minimum,

            "average_masked_stdDev":
                std,

            "Brightness_Range":
                brightness_range,

            "Brightness_Ratio":
                brightness_ratio,

            "Brightness_Product":
                brightness_product
        }


        try:

            response = requests.post(
                f"{API_URL}/predict",
                json=payload,
                timeout=15
            )


            if response.status_code == 200:

                result = response.json()

                prediction = result.get(
                    "prediction"
                )


                st.success(
                    "Population prediction generated successfully."
                )


                if isinstance(
                    prediction,
                    dict
                ):

                    population = (
                        prediction.get("population")
                        or prediction.get("estimated_population")
                        or prediction.get("predicted_population")
                        or prediction.get("prediction")
                    )

                else:

                    population = prediction


                if population is not None:

                    st.metric(
                        f"Estimated Population — {selected_city}",
                        f"{float(population):,.0f}"
                    )

                else:

                    st.json(result)


            else:

                st.error(
                    f"API returned status "
                    f"{response.status_code}"
                )

                st.code(
                    response.text
                )


        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI. "
                "Make sure the backend is running."
            )


        except Exception as error:

            st.error(
                f"Prediction error: {error}"
            )


# ============================================================
# LIVE INGESTION
# ============================================================

elif page == "Live Ingestion":

    st.title("📡 Process Satellite Observation")

    st.caption(
        "Send a real-time satellite observation to the FastAPI backend."
    )


    col1, col2 = st.columns(2)


    with col1:

        source_id = st.text_input(
            "Satellite Source ID",
            "SATELLITE_UI_01"
        )


        city_id = st.text_input(
            "City ID",
            "DELHI"
        )


        brightness_value = st.number_input(
            "Brightness Value",
            min_value=0.0,
            value=150.0,
            step=0.1
        )


    with col2:

        timestamp = st.text_input(
            "Observation Timestamp",
            "2026-08-15T12:00:00"
        )


        reliability_score = st.slider(
            "Reliability Score",
            min_value=0.0,
            max_value=1.0,
            value=0.90,
            step=0.01
        )


    st.divider()


    if st.button(
        "🚀 Submit Observation"
    ):

        payload = {

            "source_id":
                source_id,

            "timestamp":
                timestamp,

            "city_id":
                city_id,

            "brightness_value":
                brightness_value,

            "reliability_score":
                reliability_score
        }


        try:

            response = requests.post(
                f"{API_URL}/ingest",
                json=payload,
                timeout=15
            )


            result = response.json()


            if response.status_code == 200:

                if result["status"] == "accepted":

                    st.success(
                        "✅ Observation accepted successfully"
                    )


                    st.subheader(
                        "⚔️ Resolution Result"
                    )


                    winner = result[
                        "resolved_observation"
                    ]


                    c1, c2, c3 = st.columns(3)


                    with c1:

                        st.metric(
                            "Winning Source",
                            winner["source_id"]
                        )


                    with c2:

                        st.metric(
                            "Brightness",
                            winner["brightness_value"]
                        )


                    with c3:

                        st.metric(
                            "Reliability",
                            winner["reliability_score"]
                        )


                    st.info(
                        "✓ Event processed in real time."
                    )


                elif result["status"] == "duplicate":

                    st.warning(
                        "⚠️ Duplicate observation detected."
                    )


                    st.write(
                        "Event ID:"
                    )

                    st.code(
                        result["event_id"]
                    )


            else:

                st.error(
                    f"API Error: {response.status_code}"
                )

                st.json(result)


        except requests.exceptions.ConnectionError:

            st.error(
                "FastAPI is not running. "
                "Start it using: uvicorn app.main:app --reload"
            )


        except Exception as error:

            st.error(
                f"Error: {error}"
            )


# ============================================================
# ANALYTICS
# ============================================================

elif page == "Analytics":

    st.title("📊 Satellite Analytics")

    st.caption(
        "Analyze the complete satellite dataset."
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "Cities",
            len(df)
        )


    with c2:

        st.metric(
            "Average Brightness",
            f"{df['average_masked_mean'].mean():.2f}"
        )


    with c3:

        st.metric(
            "Maximum Brightness",
            f"{df['average_masked_max'].max():.2f}"
        )


    with c4:

        st.metric(
            "Minimum Brightness",
            f"{df['average_masked_min'].min():.2f}"
        )


    st.divider()


    st.subheader(
        "💡 Brightest Cities"
    )


    top20 = (
        df.groupby("City")[
            "average_masked_mean"
        ]
        .mean()
        .sort_values(
            ascending=False
        )
        .head(20)
    )


    st.bar_chart(
        top20,
        height=450
    )


    st.subheader(
        "🏙️ City Satellite Data"
    )


    display_columns = [
        "City",
        "Latitude",
        "Longitude",
        "average_masked_mean",
        "average_masked_max",
        "average_masked_min",
        "average_masked_stdDev"
    ]


    display_columns = [
        column
        for column in display_columns
        if column in df.columns
    ]


    st.dataframe(
        df[display_columns],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🛰️ Real-Time Satellite Population Intelligence "
    "• NASA VIIRS • Random Forest • FastAPI • SQLite"
)