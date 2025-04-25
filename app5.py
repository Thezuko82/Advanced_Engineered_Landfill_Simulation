import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Engineered Landfill Simulation", layout="wide")
st.title("🌍 Advanced Engineered Landfill Simulation")

# Sidebar Controls
st.sidebar.header("🔧 Control Panel")
st.sidebar.markdown("Adjust parameters to see how the landfill responds.")

velocity_leachate = st.sidebar.slider("Leachate Flow Velocity (m/day)", 0.1, 10.0, 2.0, 0.1)
diffusion_gas = st.sidebar.slider("Gas Diffusion Rate (m²/day)", 0.01, 2.0, 0.3, 0.01)
liner_type = st.sidebar.selectbox("Select Liner Type", ["Clay (1e-7 m/s)", "Geomembrane (1e-9 m/s)", "Composite (1e-10 m/s)"])
design_option = st.sidebar.radio("Design Comparison", ["Design A - Basic", "Design B - Composite", "Design C - Eco-Advanced"])

liner_values = {"Clay (1e-7 m/s)": 1e-7, "Geomembrane (1e-9 m/s)": 1e-9, "Composite (1e-10 m/s)": 1e-10}
k = liner_values[liner_type]

# Simulation Domain
x = np.linspace(0, 5, 50)  # distance in meters
t = np.linspace(0.1, 40, 80)  # time in days
X, T = np.meshgrid(x, t)

# Simulated Leachate Flow
C_leachate = np.exp(-((X - velocity_leachate * T) ** 2) / (4 * T)) * np.exp(-k * 10)

# Simulated Gas Migration
C_gas = np.exp(-diffusion_gas * T / 10) * np.cos(np.pi * X / 20)**2

# Combine frames for animation
frames = []
for i in range(1, len(t), 2):
    frames.append(go.Frame(
        data=[
            go.Heatmap(z=C_leachate[:i, :], colorscale='Blues', zmin=0, zmax=1, showscale=False),
            go.Heatmap(z=C_gas[:i, :], colorscale='Oranges', zmin=0, zmax=1, opacity=0.4, showscale=False)
        ],
        name=f"t = {round(t[i], 1)} days"
    ))

# Layout and plot definition
layout = go.Layout(
    title="🌀 Leachate & Gas Migration in Landfill",
    xaxis_title="Distance (m)",
    yaxis_title="Time (days)",
    margin=dict(l=40, r=40, t=60, b=40),
    height=550,
    updatemenus=[{
        "type": "buttons",
        "buttons": [{
            "label": "▶ Play",
            "method": "animate",
            "args": [None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}]
        }, {
            "label": "⏸ Pause",
            "method": "animate",
            "args": [[None], {"mode": "immediate", "frame": {"duration": 0, "redraw": False}, "transition": {"duration": 0}}]
        }]
    }]
)

fig = go.Figure(
    data=[
        go.Heatmap(z=C_leachate[:1, :], colorscale='Blues', zmin=0, zmax=1, name="Leachate"),
        go.Heatmap(z=C_gas[:1, :], colorscale='Oranges', zmin=0, zmax=1, opacity=0.4, name="Gas")
    ],
    layout=layout,
    frames=frames
)

st.plotly_chart(fig, use_container_width=True)

# 📘 Design Comparison
st.markdown("---")
st.subheader("📘 Design Comparison Summary")
if design_option == "Design A - Basic":
    st.markdown("""
    - Single clay liner.
    - Economical but vulnerable to leachate seepage.
    - Basic gas venting layer.
    """)
elif design_option == "Design B - Composite":
    st.markdown("""
    - Composite liner (clay + geomembrane).
    - Enhanced leachate containment.
    - Includes leachate collection and gas venting systems.
    """)
elif design_option == "Design C - Eco-Advanced":
    st.markdown("""
    - Multi-barrier system with GCL, HDPE liner, and biocover.
    - Excellent environmental performance.
    - Higher construction and maintenance cost.
    """)

# 📷 Schematic Illustration
st.markdown("---")
st.subheader("📷 Engineered Landfill Schematic")
st.image(
    "https://www.geoengineer.org/storage/wcp_assignment/177/editor_photos/4273/Fig1.jpg",
    caption="Figure: Biodegradation in Municipal Solid Waste landfills (Source: Geoengineer.org)",
    use_column_width=True
)

st.markdown("""
This simulation demonstrates the conceptual behavior of engineered landfill systems. For detailed design, refer to EPA, CPCB, and BIS design codes.
""")