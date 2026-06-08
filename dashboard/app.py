import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import streamlit as st
import pandas as pd
import plotly.express as px

from storage.query_service import QueryService

st.set_page_config(
    page_title="Time-Series Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Time-Series Analytics with Caching Layer")

st.markdown(
    """
    **Technologies:** InfluxDB + Redis + Apache Spark

    Real-time monitoring dashboard for sensor analytics.
    """
)

service = QueryService()

# data = service.get_all_latest_metrics()
try:
    data = service.get_all_latest_metrics()
except Exception as e:
    st.error(f"Backend error: {e}")
    st.stop()

if not data:
    st.warning("No sensor data found (InfluxDB may still be loading or empty).")
    st.stop()

if not data:
    st.error("No sensor data found.")
    st.stop()

df = pd.DataFrame(data)

avg_temp = df["temperature"].mean()
avg_cpu = df["cpu_usage"].mean()
avg_energy = df["energy_consumption"].mean()

anomaly_count = len(
    df[
        (df["temperature"] > 27)
        | (df["temperature"] < 20)
        | (df["cpu_usage"] > 55)
    ]
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Sensors",
    len(df)
)

col2.metric(
    "Avg Temperature",
    f"{avg_temp:.2f} °C"
)

col3.metric(
    "Avg CPU Usage",
    f"{avg_cpu:.1f}%"
)

col4.metric(
    "Anomalies",
    anomaly_count
)

st.subheader("📋 Latest Sensor Readings")

st.dataframe(
    df,
    use_container_width=True
)

left, right = st.columns(2)

with left:

    st.subheader("🌡 Temperature by Sensor")

    fig_temp = px.bar(
        df,
        x="sensor_id",
        y="temperature",
        title="Temperature"
    )

    st.plotly_chart(
        fig_temp,
        use_container_width=True
    )

with right:

    st.subheader("🖥 CPU Usage by Sensor")

    fig_cpu = px.bar(
        df,
        x="sensor_id",
        y="cpu_usage",
        title="CPU Usage"
    )

    st.plotly_chart(
        fig_cpu,
        use_container_width=True
    )

st.subheader("⚡ Energy Consumption")

fig_energy = px.line(
    df,
    x="sensor_id",
    y="energy_consumption",
    markers=True
)

st.plotly_chart(
    fig_energy,
    use_container_width=True
)

st.subheader("🚨 Detected Anomalies")

anomalies = df[
    (df["temperature"] > 27)
    | (df["temperature"] < 20)
    | (df["cpu_usage"] > 55)
]

if len(anomalies) > 0:

    st.error(
        f"{len(anomalies)} anomaly/anomalies detected"
    )

    st.dataframe(
        anomalies,
        use_container_width=True
    )

else:

    st.success(
        "No anomalies detected"
    )

st.markdown("---")

st.caption(
    "Big Data Architectures Project • InfluxDB + Redis + Spark"
)

service.close()
