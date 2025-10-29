import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go

# ----------------------------------------
# 🌈 PAGE CONFIG
# ----------------------------------------
st.set_page_config(
    page_title="💰 Ezhalni - Financial Health Dashboard",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------
# 🔗 API CONFIG
# ----------------------------------------
# Run health check on app load
API_URL = "https://financial-health-api-444234949353.europe-west1.run.app"


# ----------------------------------------
# 🔍 API HEALTH CHECK + Toast Notification
# ----------------------------------------
def check_api_status():
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            status = response.json().get("status", "unknown")
            if status == "healthy":
                show_api_notification("✅ API is connected successfully!", duration=3)
            else:
                show_api_notification("⚠️ API responded, but not healthy", duration=3)
        else:
            show_api_notification(f"🚨 API returned {response.status_code}", duration=3)
    except Exception as e:
        show_api_notification(f"❌ API unreachable: {e}", duration=3)


def show_api_notification(message="✅ API is connected successfully!", duration=3):
    """Animated notification that appears at the top for a few seconds"""
    st.markdown(f"""
        <style>
        .toast {{
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #e0f2fe;
            color: #1e3a8a;
            font-family: 'Poppins', sans-serif;
            border: 2px solid #bae6fd;
            border-radius: 10px;
            padding: 15px 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 9999;
            animation: fadein 0.5s, fadeout 0.5s {duration}s forwards;
        }}
        @keyframes fadein {{
            from {{ opacity: 0; top: 60px; }}
            to {{ opacity: 1; top: 80px; }}
        }}
        @keyframes fadeout {{
            from {{ opacity: 1; top: 80px; }}
            to {{ opacity: 0; top: 40px; }}
        }}
        </style>
        <div class="toast">{message}</div>
    """, unsafe_allow_html=True)

# 🔧 Run the check right after loading
check_api_status()

# ----------------------------------------
# 💰 CASH FLOW WATERFALL CHART FUNCTION
# ----------------------------------------
def create_cash_flow_waterfall(income, expenses, debt):
    data = [
        {'Category': 'Income', 'Amount': income},
        {'Category': 'Expenses', 'Amount': -expenses},
        {'Category': 'Debt Payment', 'Amount': -debt},
        {'Category': 'Available Cash', 'Amount': income - expenses - debt}
    ]

    df = pd.DataFrame(data)

    fig = go.Figure(go.Waterfall(
        x=df['Category'],
        y=df['Amount'],
        textposition="outside",
        text=df['Amount'].apply(lambda x: f"${x:,.0f}"),
        connector={"line": {"color": "#3b82f6"}},
        increasing={"marker": {"color": "#3b82f6"}},
        decreasing={"marker": {"color": "#1e3a8a"}},
        totals={"marker": {"color": "#fde68a"}}
    ))

    fig.update_layout(
        title="💰 Monthly Cash Flow Overview",
        title_font=dict(size=18, color="#1e3a8a", family="Poppins"),
        yaxis_title="Amount ($)",
        font=dict(size=13, family="Poppins", color="#1e3a8a"),
        height=400,
        plot_bgcolor="#F0F8FF",
        paper_bgcolor="#F0F8FF",
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=False
    )
    return fig

# 💰 Emergency Fund Coverage Gauge with Dynamic Status
def create_emergency_fund_gauge(emergency_months):
    if emergency_months < 3:
        status = "🔴 At Risk"
        gauge_color = ["#ef4444", "#fde68a"]
    elif 3 <= emergency_months < 6:
        status = "🟡 Stable"
        gauge_color = ["#fde68a", "#10b981"]
    else:
        status = "🟢 Secure"
        gauge_color = ["#10b981", "#60a5fa"]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=emergency_months,
        title={
            'text': f"💰 Emergency Fund Coverage (months)<br><span style='font-size:18px'>{status}</span>",
            'font': {'size': 18, 'color': '#1e3a8a', 'family': 'Poppins'}
        },
        number={
            'font': {'size': 50, 'color': '#1e3a8a', 'family': 'Poppins'}
        },
        gauge={
            'axis': {
                'range': [0, 6],
                'tickfont': {'size': 12, 'color': '#1e3a8a', 'family': 'Poppins'}
            },
            'bar': {'color': '#1e3a8a'},
            'steps': [
                {'range': [0, 3], 'color': gauge_color[0]},
                {'range': [3, 6], 'color': gauge_color[1]}
            ],
            'threshold': {
                'line': {'color': '#10b981', 'width': 4},
                'thickness': 0.75,
                'value': 4.5
            }
        }
    ))

    fig.update_layout(
        height=400,
        font=dict(size=13, color="#1e3a8a", family="Poppins"),
        paper_bgcolor="#F0F8FF",
        plot_bgcolor="#F0F8FF",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig
# ----------------------------------------
# 🧭 SIDEBAR NAVIGATION
# ----------------------------------------
st.sidebar.title("🧭 Navigation")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "📈 Financial Input", "📊 Insights", "💡 You vs others", "🧠 Plan"]
)
st.sidebar.markdown("---")
st.sidebar.caption("Built with ❤️ by Ezhalni team")

# ----------------------------------------
# 🏠 HOME PAGE - IMPROVED DESIGN
# ----------------------------------------
if page == "🏠 Home":
    # --- STYLE ---
    st.markdown("""
        <style>
            .block-container{padding-top:0.5rem!important; padding-bottom:2rem!important;}
            body{background-color:#F0F8FF;color:#222;}

            .welcome{
                font-size:48px;font-weight:bold;color:#1e3a8a;
                margin-top:5px;margin-bottom:8px;text-shadow:2px 2px 6px rgba(0,0,0,.3);
                text-align:center;
            }
            .subtitle{
                font-size:20px;font-weight:700;text-align:center;margin-top:0px;margin-bottom:30px;color:#3b82f6;
            }

            /* Cards */
            .card{
                border:1px solid #bfdbfe;border-radius:16px;padding:20px;
                box-shadow:0 6px 18px rgba(30,58,138,.08);transition:all .3s ease;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            .card:hover{transform:translateY(-4px);box-shadow:0 12px 24px rgba(30,58,138,.15);}
            .card.blue{background:#e6f3f9;}
            .card.peach{background:#fde68a;}
            .card.gold{background:#60a5fa;}

            .kicker{font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#64748b;margin-bottom:6px;font-weight:600;}
            .title{font-size:18px;font-weight:900;color:#1e3a8a;margin:0;line-height:1.3;}

            .pillrow{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px;justify-content:center;}
            .pill{font-size:10px;padding:5px 10px;border-radius:999px;border:1px solid #3b82f6;background:#dbeafe;color:#1e3a8a;font-weight:600;}

            /* No hover/effects on images */
            .stImage img{border:none!important;box-shadow:none!important;transition:none!important;transform:none!important;}
            
            /* Call to action box */
            .cta-box{
                background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                color: white;
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 6px 18px rgba(30,58,138,.3);
                margin-top: 25px;
            }
            .cta-box h3{
                margin: 0 0 8px 0;
                font-size: 22px;
                font-weight: 800;
            }
            .cta-box p{
                margin: 0;
                font-size: 15px;
                opacity: 0.95;
            }
            .arrow{
                font-size: 24px;
                animation: bounce 2s infinite;
            }
            @keyframes bounce {
                0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
                40% {transform: translateY(-10px);}
                60% {transform: translateY(-5px);}
            }
        </style>
    """, unsafe_allow_html=True)

    # --- HEADER (MINIMAL SPACING) ---
    logo_col, spacer = st.columns([1, 3])
    with logo_col:
        try:
            st.image("images/logo.png", width=250)
        except:
            st.markdown("### 💰 Ezhalni")
    
    st.markdown("<div class='welcome'>Welcome to Ezhalni! 👋</div>", unsafe_allow_html=True)

    # --- MAIN LAYOUT (Image bigger than cards) ---
    col_cards, col_image = st.columns([1, 1.3], gap="large")

    with col_cards:
        # Top two cards
        card1, card2 = st.columns(2, gap="small")
        
        with card1:
            st.markdown("""
            <div class="card blue">
                <div class="kicker">YOUR MONEY STORY</div>
                <div class="title">All your budgets in one easy app</div>
            </div>
            """, unsafe_allow_html=True)

        with card2:
            st.markdown("""
            <div class="card peach">
                <div class="kicker">OUR MISSION</div>
                <div class="title">🚀 Save more stress less live smarter</div>
            </div>
            """, unsafe_allow_html=True)

        # Bottom card with pills
        st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card gold">
            <div class="kicker">WHY YOU'LL LOVE IT</div>
            <div class="title">💡 Goals that actually happen</div>
            <div class="pillrow">
              <span class="pill">🚀 Fast setup</span>
              <span class="pill">🧭 Goal-guided</span>
              <span class="pill">🤖 Smart insights</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Call to Action Box
        st.markdown("""
        <div class="cta-box">
            <h3>Ready to Get Started?</h3>
            <div class="arrow">⬅️</div>
        </div>
        """, unsafe_allow_html=True)

    with col_image:
        # Right-side illustration (bigger)
        try:
            st.image("images/www.png", use_container_width=True)
        except:
            st.info("💼 Financial illustration")

# ----------------------------------------
# 📈 FINANCIAL INPUT PAGE
# ----------------------------------------
elif page == "📈 Financial Input":
    # Apply custom CSS for beautiful light blue theme
    st.markdown("""
        <style>
        .stApp {
            background-color: #F0F8FF;
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(135deg, #3b82f6 0%, #1e3a8a 100%);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(30, 58, 138, 0.3);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            box-shadow: 0 6px 12px rgba(30, 58, 138, 0.4);
            transform: translateY(-2px);
        }
        
        /* Headers */
        h1 {
            color: #1e3a8a !important;
            font-weight: 700 !important;
            padding: 1rem 0 !important;
        }
        h2, h3 {
            color: #1e3a8a !important;
            font-weight: 600 !important;
        }
        
        /* Input fields */
        .stNumberInput > div > div > input,
        .stSlider > div > div > div > input {
            border-radius: 8px;
            border: 2px solid #3b82f6;
        }
        
        /* Cards for inputs */
        div[data-testid="stHorizontalBlock"] {
            background-color: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(30, 58, 138, 0.1);
            margin-bottom: 1rem;
        }
        
        /* Slider styling */
        .stSlider {
            padding: 1rem 0;
        }
        
        /* Status messages */
        .stAlert {
            border-radius: 12px;
            border-left: 4px solid #3b82f6;
        }
        
        /* Labels */
        label {
            color: #1e3a8a !important;
            font-weight: 500 !important;
        }
        
        /* Result box */
        .result-box {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(30, 58, 138, 0.15);
            margin: 2rem 0;
            border-left: 6px solid;
        }
        
        .status-healthy {
            border-left-color: #10b981;
        }
        
        .status-risk {
            border-left-color: #ef4444;
        }
        
        /* Confidence badge */
        .confidence-badge {
            display: inline-block;
            background-color: #fde68a;
            color: #1e3a8a;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            margin-top: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("📋 Enter Your Financial Details")
    st.markdown("---")

    # Input section with better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👤 Personal Information")
        age = st.number_input("Age", min_value=18, max_value=100, value=28, step=1)
        
        st.markdown("### 💰 Income & Expenses")
        income = st.number_input("Monthly Income ($)", min_value=0, value=6000, step=100)
        expenses = st.number_input("Monthly Expenses ($)", min_value=0, value=2500, step=100)
    
    with col2:
        st.markdown("### 💳 Savings & Debt")
        savings = st.number_input("Total Savings ($)", min_value=0, value=50000, step=500)
        debt = st.number_input("Monthly Loan Payment ($)", min_value=0, value=0, step=50)

    st.markdown("### 📊 Loan Details")
    col3, col4 = st.columns(2)
    
    with col3:
        interest_rate = st.slider("Loan Interest Rate (%)", 0.0, 20.0, 5.0, 0.1)
    with col4:
        loan_term = st.slider("Loan Term (months)", 6, 120, 0, 6)

    st.markdown("---")
    
    # Center the button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        submitted = st.button("💡 Analyze My Financial Health")

    if submitted:
        with st.spinner("🔄 Analyzing your data... please wait"):
            payload = {
                "age": age,
                "monthly_income_usd": income,
                "monthly_expenses_usd": expenses,
                "savings_usd": savings,
                "monthly_emi_usd": debt,
                "loan_interest_rate_pct": interest_rate,
                "loan_term_months": loan_term
            }

            try:
                response = requests.post(f"{API_URL}/predict", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    prediction = result.get('prediction', 'Unknown')
                    confidence = round(result.get('confidence', 0) * 100, 1)
                    model_source = result.get('source', 'N/A')
                    
                    # Display result in a beautiful card
                    if prediction.lower() in ['at risk', 'atrisk', 'at_risk']:
                        st.markdown(f"""
                            <div class="result-box status-risk">
                                <h2 style='color: #ef4444; margin: 0;'>🚨 Financial Status: At Risk</h2>
                            </div>
                        """, unsafe_allow_html=True)
                    else:  # Healthy
                        st.markdown(f"""
                            <div class="result-box status-healthy">
                                <h2 style='color: #10b981; margin: 0;'>✅ Financial Status: Healthy</h2>
                            </div>
                        """, unsafe_allow_html=True)

                    # Save session data
                    st.session_state["last_result"] = result
                    st.session_state["last_input"] = payload
                else:
                    st.error("⚠️ Could not connect to the prediction API.")
            except Exception as e:
                st.error(f"🚨 Error: {e}")

# ----------------------------------------
# 📊 INSIGHTS PAGE (Updated Color Theme)
# ----------------------------------------
elif page == "📊 Insights":

    # 🎨 Custom Page Styling (Blue Theme)
    st.markdown("""
        <style>
        /* 🌤️ Page background */
        [data-testid="stAppViewContainer"] {
            background-color: #F0F8FF !important;
        }

        /* 🩵 Sidebar */
        [data-testid="stSidebar"] {
            background-color: #F8FAFC !important;
        }

        /* ✨ KPI Cards */
        div[data-testid="metric-container"] {
            background: linear-gradient(145deg, #F8FAFC, #E0F2FE);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(30, 58, 138, 0.15);
            border: 1px solid rgba(30, 58, 138, 0.1);
            transition: all 0.25s ease;
        }

        div[data-testid="metric-container"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(30, 58, 138, 0.25);
        }

        /* 💙 Metric Cards Inner Styling */
        [data-testid="stMetricValue"] {
            color: #1e3a8a !important;
            font-weight: 700 !important;
            font-size: 24px !important;
        }
        [data-testid="stMetricLabel"] {
            color: #3b82f6 !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }

        /* 🔲 Card Wrapper */
        div[data-testid="stHorizontalBlock"] > div {
            background-color: #ffffff !important;
            border: 2px solid #1e3a8a !important;
            border-radius: 12px !important;
            padding: 20px !important;
            box-shadow: 0 4px 10px rgba(30, 58, 138, 0.15) !important;
            transition: all 0.3s ease-in-out;
        }

        div[data-testid="stHorizontalBlock"] > div:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 18px rgba(30, 58, 138, 0.25) !important;
        }

        div[data-testid="stHorizontalBlock"] {
            gap: 2rem !important;
        }

        /* 💙 Text and Fonts */
        html, body, [class*="css"] {
            font-family: "Poppins", sans-serif !important;
        }
        h1, h4, p, span {
            color: #1e3a8a !important;
        }

        /* 🎨 Gradient for Section Titles */
        h2, h3 {
            font-weight: 700 !important;
            background: linear-gradient(90deg, #1e3a8a, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }

        /* 📦 Section Box */
        .section-box {
            background: #E0F2FE;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 4px 10px rgba(30, 58, 138, 0.1);
            margin-bottom: 25px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 🌟 Header
    st.markdown(f"""
        <h1 style='display:flex;align-items:center;gap:10px;color:#1e3a8a;'>
            <svg xmlns="http://www.w3.org/2000/svg" fill="#3b82f6" height="32" width="32" viewBox="0 0 24 24">
                <path d="M3 17h2v-7H3v7zm4 0h2V7H7v10zm4 0h2v-4h-2v4zm4 0h2V4h-2v13zm4 0h2v-9h-2v9z"/>
            </svg>
            <b>Financial Insights Dashboard</b>
        </h1>
    """, unsafe_allow_html=True)
    st.markdown("Gain a clear and visually balanced overview of your financial health 💙")
    st.markdown("---")

    # 🧠 Data Retrieval
    if "last_result" not in st.session_state:
        st.warning("Please analyze your data first from the Financial Input page.")
    else:
        result = st.session_state["last_result"]
        metrics = result.get("metrics", {})
        prediction = result.get("prediction", "Unknown")
        confidence = result.get("confidence", 0)
        health_score = result.get("health_score", 0)
        payload = st.session_state.get("last_input", {})

        # Extract
        income = payload.get("monthly_income_usd", 0)
        expenses = payload.get("monthly_expenses_usd", 0)
        savings = payload.get("savings_usd", 0)
        debt = payload.get("monthly_emi_usd", 0)
        expense_ratio = metrics.get("expense_ratio", 0)
        emergency_months = metrics.get("emergency_months", 0)
        loan_to_income = metrics.get("loan_to_income", 0)
        cash_flow = income - expenses
        savings_rate = (savings / (income * 12)) * 100 if income > 0 else 0

        # 💎 KPI Section
        st.markdown("## 💎 Key Financial Indicators")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("💳 Health Status", prediction)
        k2.metric("💸 Cash Flow", f"${cash_flow:,.0f}")
        k3.metric("📊 Health Score", f"{health_score}/100")
        k4.metric("💾 Savings Rate", f"{savings_rate:.1f}%")
        st.caption("A quick overview of your key financial metrics.")
        st.markdown("---")

        # 📊 Financial Overview (Side-by-Side)
        st.markdown("### 💰 Financial Overview")
        col1, col2 = st.columns(2)

        with col1:
            df = pd.DataFrame({
                "Category": ["Income", "Expenses", "Debt", "Savings"],
                "Amount": [income, expenses, debt, savings]
            })
            fig1 = px.bar(
                df, x="Category", y="Amount",
                color="Category",
                color_discrete_map={
                    "Income": "#1e3a8a", "Expenses": "#3b82f6",
                    "Debt": "#60a5fa", "Savings": "#fde68a"
                },
                title="Your Financial Composition"
            )
            fig1.update_layout(
                title_font=dict(size=18, color="#1e3a8a", family="Poppins"),
                font=dict(size=13, family="Poppins", color="#1e3a8a"),
                yaxis_title="Amount ($)",
                height=400,
                plot_bgcolor="#F0F8FF",
                paper_bgcolor="#F0F8FF",
                margin=dict(l=40, r=40, t=60, b=40),
                showlegend=True,
            )
            st.plotly_chart(fig1, config={"displayModeBar": False}, use_container_width=True)

        with col2:
            st.plotly_chart(create_cash_flow_waterfall(income, expenses, debt), use_container_width=True)

        # ⚖️ Ratios & Emergency Gauge
        st.markdown("### ⚖️ Financial Ratios & Coverage")
        col3, col4 = st.columns(2)

        with col3:
            df_ratios = pd.DataFrame({
                "Metric": ["Expense Ratio", "Loan-to-Income", "Emergency Months"],
                "Value": [expense_ratio, loan_to_income, emergency_months]
            })
            fig2 = px.bar(
                df_ratios, x="Metric", y="Value",
                color="Value",
                color_continuous_scale=["#93c5fd", "#3b82f6", "#1e3a8a"],
                title="📊 Financial Ratios Overview"
            )
            fig2.update_layout(
                title_font=dict(size=18, color="#1e3a8a", family="Poppins"),
                font=dict(size=13, family="Poppins", color="#1e3a8a"),
                yaxis_title="Value",
                height=400,
                plot_bgcolor="#F0F8FF",
                paper_bgcolor="#F0F8FF",
                margin=dict(l=40, r=40, t=60, b=40),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig2, config={"displayModeBar": False}, use_container_width=True)

        with col4:
            st.plotly_chart(create_emergency_fund_gauge(emergency_months), use_container_width=True, config={"displayModeBar": False})

        # 💡 AI Summary
        st.markdown("---")
        st.subheader("💡 AI Insights Summary")
        st.info(f"""
        - Your **financial health** is currently: **{prediction}**.
        - You maintain a **cash flow** of **${cash_flow:,.0f}** monthly.
        - Your **expense ratio** is `{expense_ratio:.2f}`, showing how much of your income is spent.
        - Your **loan-to-income ratio** is `{loan_to_income:.2f}`.
        - You have **{emergency_months:.1f} months** of emergency savings available.
        - Keep saving and track your spending to improve your score over time 💪
        """)

# ----------------------------------------
# 💡 YOU VS OTHERS PAGE
# ----------------------------------------
elif page == "💡 You vs others":
    # Apply custom CSS for beautiful light blue theme
    st.markdown("""
        <style>
        .stApp {
            background-color: #F0F8FF;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #1e3a8a !important;
            font-weight: 700 !important;
        }
        
        /* Metric cards */
        div[data-testid="stMetricValue"] {
            color: #1e3a8a !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }
        
        div[data-testid="stMetricLabel"] {
            color: #3b82f6 !important;
            font-weight: 600 !important;
        }
        
        /* Custom cards */
        .info-card {
            background: white;
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(30, 58, 138, 0.15);
            margin: 1rem 0;
            border-left: 6px solid #3b82f6;
        }
        
        .comparison-card {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(30, 58, 138, 0.15);
            margin: 1.5rem 0;
        }
        
        .cluster-badge {
            display: inline-block;
            background: linear-gradient(135deg, #3b82f6 0%, #1e3a8a 100%);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            font-weight: 600;
            font-size: 1.1rem;
            margin: 1rem 0;
            box-shadow: 0 4px 8px rgba(30, 58, 138, 0.3);
        }
        
        .status-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            margin: 0.5rem 0;
        }
        
        .status-healthy {
            background-color: #d1fae5;
            color: #065f46;
        }
        
        .status-risk {
            background-color: #fee2e2;
            color: #991b1b;
        }
        
        /* Table styling */
        .dataframe {
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 2px 8px rgba(30, 58, 138, 0.1) !important;
        }
        
        .dataframe thead tr th {
            background: linear-gradient(135deg, #3b82f6 0%, #1e3a8a 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 1rem !important;
        }
        
        .dataframe tbody tr:nth-child(even) {
            background-color: #f0f9ff !important;
        }
        
        .dataframe tbody tr:hover {
            background-color: #fde68a !important;
            transition: all 0.3s ease;
        }
        
        /* Metrics container */
        .metrics-container {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(30, 58, 138, 0.15);
            margin: 1.5rem 0;
        }
        
        /* Warning/Info boxes */
        .stAlert {
            border-radius: 12px;
            border-left: 4px solid #fde68a;
        }
        
        /* Comparison assessment badges */
        .assessment-better {
            color: #065f46;
            font-weight: 600;
        }
        
        .assessment-worse {
            color: #991b1b;
            font-weight: 600;
        }
        
        .assessment-similar {
            color: #1e3a8a;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("👥 You vs Others")
    st.markdown("### Compare your financial profile with similar users")

    if "last_input" not in st.session_state:
        st.warning("⚠️ Please analyze your data first from the '📈 Financial Input' page.")
    else:
        try:
            with st.spinner("🔄 Loading your comparison data..."):
                response = requests.post(f"{API_URL}/cluster", json=st.session_state["last_input"])
                
            if response.status_code == 200:
                cluster_info = response.json()
                
                # 🎯 Cluster Information Card
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                
                cluster_name = cluster_info.get('cluster_name', 'N/A')
                st.markdown(f'<div class="cluster-badge">🏷️ Your Group: {cluster_name}</div>', unsafe_allow_html=True)
                
                description = cluster_info.get('description', 'No description available')
                st.markdown(f"**📝 Description:** {description}")
                
                health_status = cluster_info.get('health_status', 'N/A')
                if 'healthy' in health_status.lower():
                    st.markdown(f'<div class="status-badge status-healthy">💚 {health_status}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="status-badge status-risk">⚠️ {health_status}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("---")

                # 📊 Comparison Section
                comp = cluster_info.get("comparison", {})
                group_name = comp.get('group_name', 'N/A')
                
                st.markdown('<div class="comparison-card">', unsafe_allow_html=True)
                st.subheader(f"📊 How You Compare with {group_name}")
                
                comparison_data = {
                    "Metric": ["Income", "Savings", "Debt"],
                    "Yours": [
                        comp.get("income", {}).get("yours", 0),
                        comp.get("savings", {}).get("yours", 0),
                        comp.get("debt", {}).get("yours", 0)
                    ],
                    "Group Avg": [
                        comp.get("income", {}).get("group_average", 0),
                        comp.get("savings", {}).get("group_average", 0),
                        comp.get("debt", {}).get("group_average", 0)
                    ],
                    "Assessment": [
                        comp.get("income", {}).get("assessment", ""),
                        comp.get("savings", {}).get("assessment", ""),
                        comp.get("debt", {}).get("assessment", "")
                    ]
                }

                df_comp = pd.DataFrame(comparison_data)
                st.dataframe(df_comp, use_container_width=True, hide_index=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("---")

                # 💡 Characteristics Section
                st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
                st.subheader("💡 Financial Profile Breakdown")
                
                ch = cluster_info.get("characteristics", {})

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("💵 Cash Flow", ch.get("cash_flow", "N/A"), 
                             help="Your monthly income minus expenses")
                    st.metric("🚨 Emergency Fund", ch.get("emergency_fund", "N/A"),
                             help="Savings relative to monthly expenses")
                with col2:
                    st.metric("📊 Expense Ratio", ch.get("expense_ratio", "N/A"),
                             help="Percentage of income spent on expenses")
                    st.metric("💳 Debt Level", ch.get("debt_level", "N/A"),
                             help="Debt burden relative to income")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Success message at bottom
                st.success("✅ Comparison analysis completed successfully!")

            else:
                st.error("⚠️ Could not fetch cluster data from the server.")
        except Exception as e:
            st.error(f"🚨 Error fetching comparison data: {e}")
# ----------------------------------------
# 🧠 PLAN PAGE - THEMED VERSION
# ----------------------------------------
elif page == "🧠 Plan":
    # Custom CSS for theme
    st.markdown("""
    <style>
        /* Main background */
        .stApp {
            background-color: #F0F8FF;
        }
        
        /* Title styling */
        h1 {
            color: #1e3a8a !important;
            font-weight: 700 !important;
            padding-bottom: 10px;
            border-bottom: 3px solid #fde68a;
        }
        
        /* Section headers */
        h2, h3 {
            color: #1e3a8a !important;
            font-weight: 600 !important;
        }
        
        /* Metric containers */
        [data-testid="stMetricValue"] {
            color: #1e3a8a !important;
            font-weight: 700 !important;
        }
        
        [data-testid="stMetricLabel"] {
            color: #3b82f6 !important;
            font-weight: 500 !important;
        }
        
        /* Cards and expanders */
        .streamlit-expanderHeader {
            background-color: white !important;
            border-left: 4px solid #3b82f6 !important;
            border-radius: 5px !important;
            padding: 10px !important;
            box-shadow: 0 2px 4px rgba(30, 58, 138, 0.1) !important;
        }
        
        /* Success boxes */
        .stSuccess {
            background-color: #f0fdf4 !important;
            border-left: 4px solid #86efac !important;
            color: #166534 !important;
        }
        
        /* Warning boxes */
        .stWarning {
            background-color: #fef3c7 !important;
            border-left: 4px solid #fde68a !important;
            color: #92400e !important;
        }
        
        /* Info boxes */
        .stInfo {
            background-color: #dbeafe !important;
            border-left: 4px solid #3b82f6 !important;
            color: #1e40af !important;
        }
        
        /* Error boxes */
        .stAlert {
            background-color: #fee2e2 !important;
            border-left: 4px solid #ef4444 !important;
        }
        
        /* Buttons */
        .stDownloadButton button {
            background-color: #3b82f6 !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        .stDownloadButton button:hover {
            background-color: #1e3a8a !important;
            box-shadow: 0 6px 8px rgba(30, 58, 138, 0.4) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Progress bar */
        .stProgress > div > div {
            background-color: #fde68a !important;
        }
        
        /* Text area */
        textarea {
            background-color: white !important;
            border: 2px solid #3b82f6 !important;
            border-radius: 8px !important;
            color: #1e3a8a !important;
        }
        
        /* Dividers */
        hr {
            border-color: #3b82f6 !important;
            opacity: 0.3 !important;
        }
        
        /* Captions */
        .caption {
            color: #64748b !important;
        }
        
        /* Custom card styling */
        .custom-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(30, 58, 138, 0.1);
            border-left: 5px solid #fde68a;
            margin-bottom: 20px;
        }
        
        /* Highlight box */
        .highlight-box {
            background: linear-gradient(135deg, #3b82f6 0%, #1e3a8a 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            box-shadow: 0 4px 6px rgba(30, 58, 138, 0.2);
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🧭 Personalized Financial Plan")

    # Check if data exists
    if "last_input" not in st.session_state or not st.session_state["last_input"]:
        st.warning("Please analyze your data first from the 'Financial Input' page.")
    else:
        user_input = st.session_state["last_input"]

        # Prepare payload
        plan_payload = {
            "age": user_input.get("age", 0),
            "monthly_income_usd": user_input.get("monthly_income_usd", 0),
            "monthly_expenses_usd": user_input.get("monthly_expenses_usd", 0),
            "savings_usd": user_input.get("savings_usd", 0),
            "monthly_emi_usd": user_input.get("monthly_emi_usd", 0),
            "loan_interest_rate_pct": user_input.get("loan_interest_rate_pct", 5.0),
            "loan_term_months": user_input.get("loan_term_months", 24)
        }

        # Validate inputs
        if (
            plan_payload["age"] <= 0 or
            plan_payload["monthly_income_usd"] <= 0 or
            plan_payload["monthly_expenses_usd"] <= 0
        ):
            st.warning("⚠️ Please enter valid non-zero values for age, income, and expenses.")
            st.info("💡 Go to the Financial Input page and click 'Analyze My Financial Health' again.")
        else:
            try:
                response = requests.post(f"{API_URL}/plan", json=plan_payload)

                if response.status_code == 200:
                    plan_data = response.json()
                    
                    if plan_data and isinstance(plan_data, dict):
                        # ============================================================
                        # 📊 FINANCIAL SUMMARY
                        # ============================================================
                        st.markdown("## 💡 Financial Summary")
                        summary = plan_data.get("summary", {})
                        structured = plan_data.get("structured", {})

                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            health_status = summary.get("health_status", "N/A")
                            status_color = "🟢" if health_status == "Healthy" else "🟡" if health_status == "At Risk" else "🔴"
                            st.metric(f"{status_color} Health Status", health_status)
                        with col2:
                            st.metric("📊 Health Score", f"{summary.get('health_score', 0)}/100")
                        with col3:
                            severity = structured.get("severity", "N/A").upper()
                            severity_emoji = "🔴" if severity == "CRITICAL" else "🟠" if severity == "HIGH" else "🟡" if severity == "MODERATE" else "🟢"
                            st.metric(f"{severity_emoji} Severity", severity)
                        with col4:
                            st.metric("🎯 Action Items", summary.get("action_items", 0))

                        st.markdown(f"""
                        <div class="custom-card">
                            <strong style="color: #1e3a8a; font-size: 18px;">🎯 Top Priority:</strong> 
                            <span style="color: #3b82f6; font-size: 16px;">{summary.get('top_priority', 'N/A')}</span>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("---")

                        # ============================================================
                        # ⚠️ ISSUES & ✅ STRENGTHS
                        # ============================================================
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("### ⚠️ Issues Identified")
                            issues = structured.get("issues", [])
                            if issues:
                                for issue in issues:
                                    issue_type = issue.get("type", "").upper()
                                    icon = "🔴" if issue_type == "CRITICAL" else "🟠"
                                    with st.expander(f"{icon} {issue.get('title', 'N/A')}", expanded=True):
                                        st.write(issue.get("description", "No details"))
                            else:
                                st.success("🎉 No issues found! You're doing great!")

                        with col2:
                            st.markdown("### ✅ Your Strengths")
                            strengths = structured.get("strengths", [])
                            if strengths:
                                for strength in strengths:
                                    with st.expander(f"✅ {strength.get('title', 'N/A')}", expanded=True):
                                        st.write(strength.get("description", ""))
                            else:
                                st.info("Focus on building your financial foundation first.")

                        st.markdown("---")

                        # ============================================================
                        # 📈 DETAILED RECOMMENDATIONS
                        # ============================================================
                        st.markdown("## 📈 Detailed Recommendations")
                        recs = plan_data.get("recommendations", {})

                        # Emergency Fund
                        st.markdown("### 🏦 Emergency Fund")
                        ef = recs.get("emergency_fund", {})
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Current", f"${ef.get('current_amount', 0):,.0f}")
                            st.caption(f"{ef.get('current_months', 0):.1f} months")
                        with col2:
                            st.metric("Target", f"${ef.get('target_amount', 0):,.0f}")
                            st.caption("6 months coverage")
                        with col3:
                            st.metric("Monthly Save", f"${ef.get('monthly_contribution', 0):,.0f}")
                            if ef.get('months_to_goal', 0) > 0:
                                st.caption(f"⏱️ {ef.get('months_to_goal', 0):.0f} months to goal")

                        # Progress bar
                        if ef.get('target_amount', 0) > 0:
                            progress = min(ef.get('current_amount', 0) / ef.get('target_amount', 1), 1.0)
                            st.progress(progress)
                            st.caption(f"{progress*100:.1f}% Complete")

                        st.markdown("---")

                        # Debt Management
                        st.markdown("### 💳 Debt Management")
                        debt = recs.get("debt", {})
                        
                        if debt.get("should_focus", False):
                            st.warning("⚠️ Debt reduction should be your priority!")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Current Payment", f"${debt.get('current_payment', 0):,.0f}/mo")
                            with col2:
                                st.metric("Recommended", f"${debt.get('total_payment', 0):,.0f}/mo")
                                st.caption(f"+${debt.get('extra_payment', 0):,.0f} extra")
                            with col3:
                                st.metric("Payoff Timeline", f"{debt.get('payoff_months', 0):.0f} months")
                        else:
                            st.success("✅ Your debt level is manageable!")

                        st.markdown("---")

                        # Investment Analysis
                        st.markdown("### 📊 Investment Strategy")
                        inv = recs.get("investment", {})
                        inv_type = recs.get("investment_type", {})

                        col1, col2 = st.columns(2)
                        with col1:
                            if inv.get("can_invest", False):
                                st.success("✅ You're ready to invest!")
                                st.metric("Recommended Monthly", f"${inv.get('recommended_monthly', 0):,.0f}")
                            else:
                                st.warning("⏳ Build your foundation first before investing")
                                st.caption("Focus on emergency fund and debt reduction")

                        with col2:
                            st.markdown(f"**Investment Type:** {inv_type.get('type', 'N/A')}")
                            st.metric("Risk Score", f"{inv_type.get('risk_score', 0)}/100")
                            st.caption(inv_type.get('reasoning', ''))

                        # Asset Allocation Chart
                        if inv_type.get('allocation'):
                            allocation = inv_type.get('allocation', {})
                            fig = go.Figure(data=[go.Pie(
                                labels=list(allocation.keys()),
                                values=list(allocation.values()),
                                hole=.3,
                                marker=dict(colors=['#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd', '#fde68a'])
                            )])
                            fig.update_layout(
                                title="Recommended Asset Allocation",
                                height=300,
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='#1e3a8a')
                            )
                            st.plotly_chart(fig, use_container_width=True)

                        st.markdown("---")

                        # Expense Reduction (if applicable)
                        expense_red = recs.get("expense_reduction")
                        if expense_red:
                            st.markdown("### 💰 Expense Reduction Opportunity")
                            st.warning("⚠️ Your expenses are high - consider reducing them!")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Current", f"${expense_red.get('current', 0):,.0f}/mo")
                            with col2:
                                st.metric("Target", f"${expense_red.get('recommended', 0):,.0f}/mo")
                            with col3:
                                st.metric("Potential Savings", f"${expense_red.get('savings_monthly', 0):,.0f}/mo")
                            
                            st.markdown("**Focus on reducing:**")
                            for category in expense_red.get('categories', []):
                                st.markdown(f"• {category}")
                            
                            st.markdown("---")

                        # Savings Recommendations
                        st.markdown("### 💎 Savings Plan")
                        savings = recs.get("savings", {})
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Current Savings Rate", f"{savings.get('current_rate', 0)*100:.1f}%")
                            st.caption(f"${savings.get('current_monthly', 0):,.0f}/month")
                        with col2:
                            st.metric("Target Savings Rate", f"{savings.get('target_rate', 0)*100:.1f}%")
                            st.caption(f"${savings.get('recommended_monthly', 0):,.0f}/month")

                        st.markdown("---")

                        # ============================================================
                        # 📝 NARRATIVE PLAN
                        # ============================================================
                        st.markdown("## 📝 Your Complete Action Plan")
                        narrative = plan_data.get("narrative", "")
                        
                        if narrative:
                            st.text_area(
                                "Detailed Financial Plan",
                                narrative,
                                height=400,
                                help="This is your personalized step-by-step financial plan"
                            )
                            
                            # Download button
                            st.download_button(
                                label="📥 Download Plan as Text",
                                data=narrative,
                                file_name=f"financial_plan_{datetime.now().strftime('%Y%m%d')}.txt",
                                mime="text/plain"
                            )

                        st.markdown("---")
                        st.markdown(f"""
                        <div style="text-align: center; color: #64748b; padding: 20px;">
                            <p>🕒 Plan generated at: {plan_data.get('generated_at', 'N/A')}</p>
                            <p style="color: #3b82f6; font-weight: 600;">✨ Generated by Ezhalni Financial Health AI</p>
                        </div>
                        """, unsafe_allow_html=True)

                    else:
                        st.warning("📋 No plan data returned from API.")
                else:
                    st.error(f"⚠️ Could not generate plan (HTTP {response.status_code})")

            except Exception as e:
                st.error(f"🚨 Error fetching plan: {e}")
                st.caption("Please try again or check your internet connection.")