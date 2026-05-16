import streamlit as st
import matplotlib.pyplot as plt

# Import your existing simulation logic
from src.lcg import generate_times
from src.queues import FCFS, LCFS
from src.warmup import run_simulation_with_warmup
from charts.gantt import plot_gantt_chart, plot_waiting_bar_chart

st.set_page_config(page_title="Discrete Event Simulator", layout="wide")
st.title("Discrete Event Simulator Dashboard")

# Sidebar for GUI Controls
st.sidebar.header("Simulation Parameters")
n = st.sidebar.number_input("Number of Customers (n)", min_value=1, value=20)
seed = st.sidebar.number_input("Random Seed", value=42)
server_count = st.sidebar.slider("Number of Servers", min_value=1, max_value=5, value=1)
discipline = st.sidebar.selectbox("Queue Discipline", [FCFS, LCFS])
warmup_count = st.sidebar.number_input("Warm-up Count (k)", min_value=0, value=0)

if st.sidebar.button("Run Simulation", type="primary"):
    # 1. Generate times
    total_customers = n + warmup_count
    inter_arrival_times, service_times = generate_times(total_customers, seed)

    # 2. Run simulation
    sim_data = run_simulation_with_warmup(
        inter_arrival_times,
        service_times,
        server_count,
        discipline,
        warmup_count
    )

    results = sim_data["results"]
    
    # 3. Display Metrics
    st.subheader("Performance Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg System Wait (W)", f"{sim_data['W']:.3f} min")
    col2.metric("Avg Queue Length (Q)", f"{sim_data['Q']:.3f} customers")
    
    # Calculate average utilization
    avg_u = sum(sim_data["utilizations"]) / len(sim_data["utilizations"]) if sim_data["utilizations"] else 0
    col3.metric("Average Server Utilization (U)", f"{avg_u:.1f}%")

    # 4. Display Charts
    st.subheader("Visualizations")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.write("**Gantt Chart**")
        plot_gantt_chart(results)
        st.pyplot(plt.gcf())
        plt.clf() # Clear the figure so it doesn't overlap
        
    with chart_col2:
        st.write("**Waiting Time Bar Chart**")
        plot_waiting_bar_chart(results)
        st.pyplot(plt.gcf())
        plt.clf()

    # 5. Display Event Table
    st.subheader("Event Table")
    # Convert list of dicts to a format Streamlit renders beautifully
    st.dataframe(results, use_container_width=True)