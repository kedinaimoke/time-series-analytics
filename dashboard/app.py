import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

from storage.query_service import QueryService

st.set_page_config(
    page_title="Time-Series Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st_autorefresh(
    interval=5000,
    key="sensor_refresh"
)

st.title("Time-Series Analytics with Caching Layer")

st.markdown(
    """
    **Technologies Used:** InfluxDB + Redis + Spark

    Presented in this project is a real-time monitoring dashboard for sensor analytics.
    """
)

service = QueryService()

try:
    data = service.get_all_latest_metrics()
except Exception as e:
    st.error(f"Backend error: {e}")
    st.stop()

if not data:
    st.warning(
        "No sensor data found (InfluxDB may still be loading or empty)."
    )
    st.stop()

df = pd.DataFrame(data)

avg_temp = df["temperature"].mean()
avg_cpu = df["cpu_usage"].mean()
avg_energy = df["energy_consumption"].mean()

anomalies = df[
    (df["temperature"] > 27)
    | (df["temperature"] < 20)
    | (df["cpu_usage"] > 55)
]

anomaly_count = len(anomalies)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Sensors",
        len(df)
    )

with col2:
    st.metric(
        "Avg Temperature",
        f"{avg_temp:.2f} °C"
    )

with col3:
    st.metric(
        "Avg CPU Usage",
        f"{avg_cpu:.1f}%"
    )

with col4:
    st.metric(
        "Anomalies",
        anomaly_count
    )

with col5:
    st.metric(
        "Cache Gain",
        "~92% (11x)"
    )

st.subheader("Latest Sensor Readings")

st.dataframe(
    df,
    width='stretch'
)

st.subheader("Sensor Health Status")

status_cols = st.columns(len(df))

for i, row in enumerate(df.to_dict("records")):

    healthy = (
        row["temperature"] <= 27
        and row["temperature"] >= 20
        and row["cpu_usage"] <= 55
    )

    with status_cols[i]:

        if healthy:
            st.success(
                f"{row['sensor_id']}\n\n🟢 Healthy"
            )
        else:
            st.error(
                f"{row['sensor_id']}\n\n🔴 Anomaly"
            )

left, right = st.columns(2)

with left:

    st.subheader("Temperature by Sensor")

    fig_temp = px.bar(
        df,
        x="sensor_id",
        y="temperature",
        color="temperature",
        title="Temperature by Sensor"
    )

    st.plotly_chart(
        fig_temp,
        width='stretch'
    )

with right:

    st.subheader("CPU Usage by Sensor")

    fig_cpu = px.bar(
        df,
        x="sensor_id",
        y="cpu_usage",
        color="cpu_usage",
        title="CPU Usage by Sensor"
    )

    st.plotly_chart(
        fig_cpu,
        width='stretch'
    )

st.subheader("Energy Consumption")

fig_energy = px.bar(
    df,
    x="sensor_id",
    y="energy_consumption",
    color="energy_consumption",
    title="Energy Consumption"
)

st.plotly_chart(
    fig_energy,
    width='stretch'
)

st.subheader("24-Hour Historical Temperature Trends")

selected_sensor = st.selectbox(
    "Select Sensor",
    df["sensor_id"].tolist()
)

history = service.get_temperature_history(
    selected_sensor
)

if history:

    history_df = pd.DataFrame(history)

    fig_history = px.line(
        history_df,
        x="time",
        y="temperature",
        title=f"{selected_sensor} Temperature (Last 24 Hours)"
    )

    st.plotly_chart(
        fig_history,
        use_container_width=True
    )

else:

    st.warning(
        "No historical data available."
    )

st.subheader("Detected Anomalies")

if len(anomalies) > 0:

    st.error(
        f"{len(anomalies)} anomaly/anomalies detected"
    )

    st.markdown(
        """
        **Detection Rules**
        - Temperature > 27°C
        - Temperature < 20°C
        - CPU Usage > 55%
        """
    )

    st.dataframe(
        anomalies,
        width='stretch'
    )

else:

    st.success(
        "Yay! No anomalies detected"
    )

st.subheader("Spark Analytics Summary")

analytics_df = df[
    [
        "sensor_id",
        "temperature",
        "cpu_usage",
        "humidity",
        "energy_consumption"
    ]
]

st.dataframe(
    analytics_df.describe(),
    width='stretch'
)

st.subheader("System Architecture")

st.code(
    """
Sensor Generator
        ↓
     InfluxDB
(Time-Series Storage)
        ↓
      Redis
(Cache Layer)
        ↓
Query Service
        ↓
Streamlit Dashboard
        ↓
    Spark
(Historical Analytics)
"""
)

st.markdown("---")

st.caption(
    """
Big Data Architectures Project

Technologies:
• InfluxDB
• Redis
• Spark
• Streamlit
• Python

Created by:
Jane Kedina Imoke
&
Ricardo Ramos Morales
"""
)

service.close()
