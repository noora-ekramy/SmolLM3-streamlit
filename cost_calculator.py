import streamlit as st
import math

def cost_calculator_page():
    """Cost Calculator page for Hugging Face Inference Endpoints"""
    
    # Apply same dark theme
    st.markdown("""
    <style>
    html, body, .stApp {
        background-color: #161616; 
        height: 100%;
        margin: 0;
        padding: 0;
    }
    .stApp {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }
    .tagline {
        font-size: 20px;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        margin-top: -10px;
    }
    .subtagline {
        font-size: 14px;
        color: #FFFFFF;
        text-align: center;
        padding:20px;
        margin-bottom: 20px;
    }
     .header {
        font-size: 39px;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 10px;
    }
    .sidebar-section {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        background: linear-gradient(105.13deg, #292929 41.52% 41.52% , rgba(63, 63, 63, 0) 100%);
        backdrop-filter: blur(87.27272033691406px)
    }
    .metric-card {
        background: linear-gradient(105.13deg, #1C1C1C 41.52%, rgba(63, 63, 63, 0) 100%) ;
        color: white; 
        border: 2px solid var(--light-dark-1004, #FFFFFF0A);
        border-radius: 16px; 
        padding: 12px; 
      
    }
    .metric-card h3{
        color: #ffffff90 !important;
    }
    .metric-card h2{
        color: #FFFFFF !important;
    }
    .metric-card p{
        color: #ffffff90 !important;
    }
    .cost-breakdown{
        background: linear-gradient(105.13deg, #1C1C1C 41.52%, rgba(63, 63, 63, 0) 100%) !important;
        color: white; 
        border: 2px solid var(--light-dark-1004, #FFFFFF0A);
        border-radius: 16px; 
        padding: 12px; 
        margin: 10px 0
    }
    .cost-breakdown h4 {
        color: #FFFFFF !important;
    }
    .cost-breakdown span {
        color: #FFFFFF !important;
    }
    .warning-box {
        background-color: rgba(255, 193, 7, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid rgba(255, 193, 7, 0.3);
        margin: 1rem 0;
        color: #ffc107;
    }
    .st-emotion-cache-11ofl8m{
        background: linear-gradient(105.13deg, #1C1C1C 41.52%, rgba(63, 63, 63, 0) 100%) !important;
    }
    .st-emotion-cache-55l0h8{
       background:black
    }
    .st-emotion-cache-1hiktyo:hover:enabled, .st-emotion-cache-1hiktyo:focus:enabled {
        background: linear-gradient(105.13deg, #292929 41.52% 41.52% , rgba(63, 63, 63, 0) 100%) !important
    }
    
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="header">Endpoints Cost Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Calculate Costs and Performance for AI Endpoints</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtagline">Comprehensive cost analysis with auto-scaling and real-world usage patterns</div>', unsafe_allow_html=True)
    
    # Sidebar for parameters
    with st.sidebar:
        st.header("Configuration Parameters")
        
        # Usage Metrics Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("Usage Metrics")
        
        concurrent_users = st.slider(
            "Concurrent Users",
            min_value=1,
            max_value=10000,
            value=100,
            step=1,
            help="Number of users using the service simultaneously"
        )
        
        requests_per_user_hour = st.slider(
            "Requests per User per Hour",
            min_value=1,
            max_value=100,
            value=10,
            step=1,
            help="Average number of requests each user makes per hour"
        )
        
        avg_response_tokens = st.slider(
            "Average Response Length (tokens)",
            min_value=50,
            max_value=500,
            value=150,
            step=10,
            help="Average number of tokens in model responses"
        )
        
        daily_active_hours = st.slider(
            "Daily Active Hours",
            min_value=1,
            max_value=24,
            value=12,
            step=1,
            help="Number of hours per day the service is actively used"
        )
        
        days_per_month = st.slider(
            "Days per Month",
            min_value=1,
            max_value=31,
            value=30,
            step=1,
            help="Number of operational days per month"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Instance Configuration Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("Instance Configuration")
        
        instance_options = {
            "NVIDIA T4": {"cost": 0.50, "throughput_base": 30},
            "NVIDIA L4": {"cost": 0.80, "throughput_base": 45},
            "NVIDIA L40S": {"cost": 1.80, "throughput_base": 80},
            "NVIDIA A10G": {"cost": 1.00, "throughput_base": 60},
            "NVIDIA A100": {"cost": 2.50, "throughput_base": 150},
            "NVIDIA H100": {"cost": 4.50, "throughput_base": 250}
        }
        
        selected_instance = st.selectbox(
            "Instance Type",
            options=list(instance_options.keys()),
            index=2,  # Default to L40S
            help="Choose the GPU instance type for your endpoint"
        )
        
        # Model Size Factor
        model_size_options = {
            "Small (1B parameters)": 1.5,
            "Medium (3B parameters)": 1.0,
            "Large (7B parameters)": 0.7,
            "XL (13B+ parameters)": 0.4
        }
        
        selected_model_size = st.selectbox(
            "Model Size",
            options=list(model_size_options.keys()),
            index=1,  # Default to Medium
            help="Model size affects throughput performance"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Scaling Parameters Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("Scaling Parameters")
        
        scale_to_zero_options = {
            "15 minutes": 15,
            "30 minutes": 30,
            "1 hour": 60,
            "2 hours": 120,
            "4 hours": 240
        }
        
        scale_to_zero = st.selectbox(
            "Scale-to-Zero Timeout",
            options=list(scale_to_zero_options.keys()),
            index=2,  # Default to 1 hour
            help="Time before scaling down to zero replicas during inactivity"
        )
        
        max_replicas = st.slider(
            "Max Replicas Limit",
            min_value=1,
            max_value=100,
            value=10,
            step=1,
            help="Maximum number of replicas for auto-scaling"
        )
        
        min_replicas = st.slider(
            "Min Replicas",
            min_value=0,
            max_value=5,
            value=0,
            step=1,
            help="Minimum number of replicas (0 enables scale-to-zero)"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Advanced Parameters Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("Advanced Parameters")
        
        cold_start_delay = st.slider(
            "Cold Start Delay (minutes)",
            min_value=1,
            max_value=3,
            value=2,
            step=1,
            help="Time to start a new replica from cold state"
        )
        
        request_timeout = st.slider(
            "Request Timeout (seconds)",
            min_value=30,
            max_value=300,
            value=60,
            step=30,
            help="Maximum time to wait for a request response"
        )
        
        batch_size = st.slider(
            "Batch Size",
            min_value=1,
            max_value=32,
            value=1,
            step=1,
            help="Number of requests processed together"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Regional and Cost Modifiers Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("Regional & Cost Modifiers")
        
        regional_multipliers = {
            "US East": 1.0,
            "EU West": 1.1,
            "Asia Pacific": 1.2
        }
        
        selected_region = st.selectbox(
            "Region",
            options=list(regional_multipliers.keys()),
            index=0,
            help="Regional pricing affects overall costs"
        )
        
        data_transfer_gb = st.number_input(
            "Est. Data Transfer (GB/month)",
            min_value=0.0,
            max_value=10000.0,
            value=100.0,
            step=10.0,
            help="Estimated monthly data egress in GB"
        )
        
        storage_gb = st.number_input(
            "Model Storage (GB)",
            min_value=0.1,
            max_value=100.0,
            value=5.0,
            step=0.5,
            help="Storage required for model cache"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Calculate all metrics
    instance_cost_per_hour = instance_options[selected_instance]["cost"]
    base_throughput = instance_options[selected_instance]["throughput_base"]
    model_multiplier = model_size_options[selected_model_size]
    regional_multiplier = regional_multipliers[selected_region]
    scale_timeout_minutes = scale_to_zero_options[scale_to_zero]
    
    # Core calculations
    total_requests_per_hour = concurrent_users * requests_per_user_hour
    adjusted_throughput = base_throughput * model_multiplier * batch_size
    required_replicas = max(min_replicas, math.ceil(total_requests_per_hour / 60 / adjusted_throughput))
    actual_replicas = min(required_replicas, max_replicas)
    
    # Cost calculations
    base_hourly_cost = actual_replicas * instance_cost_per_hour
    regional_hourly_cost = base_hourly_cost * regional_multiplier
    daily_cost = regional_hourly_cost * daily_active_hours
    monthly_compute_cost = daily_cost * days_per_month
    
    # Additional costs
    data_transfer_cost = data_transfer_gb * 0.09  # $0.09/GB egress
    storage_cost = storage_gb * 0.10  # $0.10/GB/month
    total_monthly_cost = monthly_compute_cost + data_transfer_cost + storage_cost
    
    # Performance calculations
    max_requests_per_hour = actual_replicas * adjusted_throughput * 60
    avg_response_time = (request_timeout * 0.1) + (cold_start_delay * 60 if min_replicas == 0 else 0)
    utilization_percentage = (total_requests_per_hour / max_requests_per_hour) * 100 if max_requests_per_hour > 0 else 0
    
    # Speed calculations
    tokens_per_second = (adjusted_throughput * avg_response_tokens * actual_replicas) / 60
    requests_per_second = adjusted_throughput * actual_replicas / 60
    
    # Main content area
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #65daff; margin: 0;">Monthly Cost</h3>
            <h2 style="color: #a4ffff; margin: 5px 0;">${total_monthly_cost:.2f}</h2>
            <p style="color: #fcfcfc; margin: 0;">Total operational cost</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #65daff; margin: 0;">Required Replicas</h3>
            <h2 style="color: #a4ffff; margin: 5px 0;">{actual_replicas}</h2>
            <p style="color: #fcfcfc; margin: 0;">Auto-scaled instances</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #65daff; margin: 0;">Throughput</h3>
            <h2 style="color: #a4ffff; margin: 5px 0;">{max_requests_per_hour:,.0f}</h2>
            <p style="color: #fcfcfc; margin: 0;">Requests/hour capacity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #65daff; margin: 0;">Utilization</h3>
            <h2 style="color: #a4ffff; margin: 5px 0;">{utilization_percentage:.1f}%</h2>
            <p style="color: #fcfcfc; margin: 0;">Resource efficiency</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance Metrics
    st.subheader("Performance Metrics")
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric("Requests/Second", f"{requests_per_second:.1f}")
    
    with col6:
        st.metric("Tokens/Second", f"{tokens_per_second:.0f}")
    
    with col7:
        st.metric("Avg Response Time", f"{avg_response_time:.1f}s")
    
    with col8:
        st.metric("Cold Start Impact", f"{cold_start_delay:.0f} min" if min_replicas == 0 else "None")
    
    # Cost Breakdown
    st.subheader("Cost Breakdown")
    
    st.markdown(f"""
    <div class="cost-breakdown">
        <h4 style="color: #65daff; margin-top: 0;">Monthly Cost Analysis</h4>
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="color: #fcfcfc;">Compute Cost ({actual_replicas} × {selected_instance}):</span>
            <span style="color: #a4ffff; font-weight: bold;">${monthly_compute_cost:.2f}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="color: #fcfcfc;">Data Transfer ({data_transfer_gb:.1f} GB):</span>
            <span style="color: #a4ffff; font-weight: bold;">${data_transfer_cost:.2f}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="color: #fcfcfc;">Storage ({storage_gb:.1f} GB):</span>
            <span style="color: #a4ffff; font-weight: bold;">${storage_cost:.2f}</span>
        </div>
        <div style="display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 10px; margin-top: 15px;">
            <span style="color: #65daff; font-weight: bold;">Total Monthly Cost:</span>
            <span style="color: #a4ffff; font-weight: bold; font-size: 1.2em;">${total_monthly_cost:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Warnings and Recommendations
    if utilization_percentage > 90:
        st.markdown(f"""
        <div class="warning-box">
            <strong>High Utilization Warning:</strong> Your system is running at {utilization_percentage:.1f}% capacity. 
            Consider increasing max replicas or upgrading instance type to avoid performance issues.
        </div>
        """, unsafe_allow_html=True)
    
    if actual_replicas >= max_replicas:
        st.markdown(f"""
        <div class="warning-box">
            <strong>Scaling Limited:</strong> You've hit the max replica limit ({max_replicas}). 
            Increase the limit or upgrade instance type to handle higher demand.
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed Analysis
    with st.expander("Detailed Analysis & Formulas"):
        st.subheader("Calculation Details")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.write("**Core Formulas:**")
            st.code(f"""
Total Requests/Hour = {concurrent_users} × {requests_per_user_hour} = {total_requests_per_hour:,}

Adjusted Throughput = {base_throughput} × {model_multiplier} × {batch_size} = {adjusted_throughput:.1f} req/min

Required Replicas = ceil({total_requests_per_hour:,} ÷ 60 ÷ {adjusted_throughput:.1f}) = {required_replicas}

Actual Replicas = min({required_replicas}, {max_replicas}) = {actual_replicas}
            """)
        
        with col_b:
            st.write("**Cost Formulas:**")
            st.code(f"""
Hourly Cost = {actual_replicas} × ${instance_cost_per_hour} × {regional_multiplier} = ${regional_hourly_cost:.2f}

Daily Cost = ${regional_hourly_cost:.2f} × {daily_active_hours}h = ${daily_cost:.2f}

Monthly Compute = ${daily_cost:.2f} × {days_per_month} days = ${monthly_compute_cost:.2f}

Total Monthly = ${monthly_compute_cost:.2f} + ${data_transfer_cost:.2f} + ${storage_cost:.2f} = ${total_monthly_cost:.2f}
            """)
    
    # Usage Scenarios
    with st.expander("Common Usage Scenarios"):
        scenarios = {
            "Startup/Development": {
                "users": 10, "req_hour": 5, "hours": 8, "days": 22,
                "instance": "NVIDIA T4", "replicas_max": 2
            },
            "Small Business": {
                "users": 100, "req_hour": 10, "hours": 12, "days": 30,
                "instance": "NVIDIA L4", "replicas_max": 5
            },
            "Enterprise": {
                "users": 1000, "req_hour": 20, "hours": 16, "days": 30,
                "instance": "NVIDIA A100", "replicas_max": 20
            },
            "High-Scale Production": {
                "users": 5000, "req_hour": 15, "hours": 24, "days": 30,
                "instance": "NVIDIA H100", "replicas_max": 50
            }
        }
        
        st.write("**Scenario Comparison:**")
        for name, params in scenarios.items():
            scenario_cost = calculate_scenario_cost(params, instance_options, model_multiplier, regional_multiplier)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.write(f"**{name}**")
            with col2:
                st.write(f"{params['users']} users")
            with col3:
                st.write(f"{params['users'] * params['req_hour']} req/hour")
            with col4:
                st.write(f"{params['instance']}")
            with col5:
                st.write(f"${scenario_cost:.2f}/month")
    
    # Cost scaling analysis
    st.subheader("Cost Scaling Analysis")
    
    st.write("**Monthly Cost vs Concurrent Users:**")
    
    # Generate cost data for different user loads
    user_loads = [10, 50, 100, 250, 500, 1000, 2000, 5000]
    
    col1, col2, col3, col4 = st.columns(4)
    headers = ["Users", "Requests/Hour", "Replicas", "Monthly Cost"]
    
    for i, header in enumerate(headers):
        with [col1, col2, col3, col4][i]:
            st.write(f"**{header}**")
    
    for users in user_loads:
        temp_requests = users * requests_per_user_hour
        temp_replicas = max(min_replicas, math.ceil(temp_requests / 60 / adjusted_throughput))
        temp_replicas = min(temp_replicas, max_replicas)
        temp_cost = temp_replicas * instance_cost_per_hour * regional_multiplier * daily_active_hours * days_per_month
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write(f"{users:,}")
        with col2:
            st.write(f"{temp_requests:,}")
        with col3:
            st.write(f"{temp_replicas}")
        with col4:
            st.write(f"${temp_cost:.2f}")

def calculate_scenario_cost(params, instance_options, model_multiplier, regional_multiplier):
    """Calculate cost for a given scenario"""
    total_requests = params["users"] * params["req_hour"]
    base_throughput = instance_options[params["instance"]]["throughput_base"]
    adjusted_throughput = base_throughput * model_multiplier
    required_replicas = max(0, math.ceil(total_requests / 60 / adjusted_throughput))
    actual_replicas = min(required_replicas, params["replicas_max"])
    
    instance_cost = instance_options[params["instance"]]["cost"]
    monthly_cost = (actual_replicas * instance_cost * regional_multiplier * 
                   params["hours"] * params["days"])
    
    return monthly_cost

if __name__ == "__main__":
    cost_calculator_page()
