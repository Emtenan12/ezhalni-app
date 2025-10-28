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
    available = income - expenses - debt

    measures = ["absolute", "relative", "relative", "total"]
    y_values = [income, -expenses, -debt, available]

    fig = go.Figure(go.Waterfall(
        name="Cash Flow",
        orientation="v",
        measure=measures,
        x=["Income", "Expenses", "Debt Payment", "Available Cash"],
        y=y_values,
        text=[f"${income:,.0f}", f"-${expenses:,.0f}",
              f"-${debt:,.0f}", f"${available:,.0f}"],
        textposition="outside",
        connector={"line": {"color": "rgba(97,84,164,0.4)"}},

        increasing={"marker": {"color": "#00CC96"}},  # 🟩 Income
        decreasing={"marker": {"color": "#EF553B"}},  # 🔴 Expenses & Debt
        totals={"marker": {"color": "#6154a4" if available >= 0 else "#EF553B"}}
    ))

    fig.update_layout(
        title="💰 Monthly Cash Flow Overview",
        title_font=dict(size=18, color="#4b3f72", family="Poppins"),
        yaxis_title="Amount ($)",
        font=dict(size=13, family="Poppins"),
        height=400,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=False
    )

    return fig

# 💰 Emergency Fund Coverage Gauge with Dynamic Status
def create_emergency_fund_gauge(emergency_months):
    # ✅ Determine status and colors dynamically
    if emergency_months < 3:
        status = "🟥 At Risk"
        gauge_color = ["#ff6b6b", "#ffd93d"]
    elif 3 <= emergency_months < 6:
        status = "🟨 Stable"
        gauge_color = ["#ffd93d", "#6bcB77"]
    else:
        status = "🟩 Secure"
        gauge_color = ["#6bcB77", "#4b3f72"]

    # ✅ Create the gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=emergency_months,
        title={
            'text': f"💰 Emergency Fund Coverage (months)<br><span style='font-size:18px'>{status}</span>",
            'font': {'size': 18, 'color': '#4b3f72', 'family': 'Poppins'}
        },
        number={
            'font': {'size': 50, 'color': '#4b3f72', 'family': 'Poppins'}
        },
        gauge={
            'axis': {
                'range': [0, 6],
                'tickfont': {'size': 12, 'color': '#4b3f72', 'family': 'Poppins'}
            },
            'bar': {'color': '#6154a4'},
            'steps': [
                {'range': [0, 3], 'color': gauge_color[0]},
                {'range': [3, 6], 'color': gauge_color[1]}
            ],
            'threshold': {
                'line': {'color': '#00C49A', 'width': 4},
                'thickness': 0.75,
                'value': 4.5
            }
        }
    ))

    # ✅ Layout styling (consistent with your dashboard theme)
    fig.update_layout(
        height=400,
        font=dict(size=13, color="#4b3f72", family="Poppins"),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
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
    ["🏠 Home", "📈 Financial Input", "📊 Insights", "💡 Cluster", "🧠 Plan"]
)
st.sidebar.markdown("---")
st.sidebar.caption("Built with ❤️ by our team")

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
    st.title("📋 Enter Your Financial Details")

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, step=1)
        dependents = st.number_input("Dependents", min_value=0, max_value=10, step=1)
    with col2:
        income = st.number_input("Monthly Income ($)", min_value=0, step=100)
        expenses = st.number_input("Monthly Expenses ($)", min_value=0, step=100)
    with col3:
        savings = st.number_input("Total Savings ($)", min_value=0, step=50)
        debt = st.number_input("Monthly Loan Payment ($)", min_value=0, step=50)

    interest_rate = st.slider("Loan Interest Rate (%)", 0.0, 20.0, 5.0, 0.1)
    loan_term = st.slider("Loan Term (months)", 6, 120, 24, 6)

    submitted = st.button("💡 Analyze My Financial Health")

    if submitted:
        st.markdown("### 🔄 Analyzing your data... please wait")

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

                st.success(f"✅ Your Financial Status: **{result.get('prediction', 'Unknown')}**")
                st.metric("Financial Score", f"{result.get('health_score', 0)} / 100")
                st.caption(f"🤖 Confidence: {round(result.get('confidence', 0)*100, 1)}% (Model: {result.get('source', 'N/A')})")


                # Save session data
                st.session_state["last_result"] = result
                st.session_state["last_input"] = payload
            else:
                st.error("⚠️ Could not connect to the prediction API.")
        except Exception as e:
            st.error(f"🚨 Error: {e}")

# ----------------------------------------
# 📊 INSIGHTS PAGE
# ----------------------------------------
elif page == "📊 Insights":

    # 🎨 Custom Page Styling (Light + Mauve tones)
    st.markdown("""
        <style>
        /* 🌤️ Page background */
        [data-testid="stAppViewContainer"] {
            background-color: #ffffff !important;
        }

        /* 💜 Sidebar */
        [data-testid="stSidebar"] {
            background-color: #f5f3ff !important;
        }

        /* ✨ KPI Cards */
        div[data-testid="metric-container"] {
            background: linear-gradient(145deg, #f5f3ff, #ecebff);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(97, 84, 164, 0.15);
            border: 1px solid rgba(97, 84, 164, 0.1);
            transition: all 0.25s ease;
        }

        div[data-testid="metric-container"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(97, 84, 164, 0.25);
        }

        /* 🟣 Metric Cards Inner Styling */
        [data-testid="stMetricValue"] {
            color: #1e1b4b !important;
            font-weight: 700 !important;
            font-size: 24px !important;
        }
        [data-testid="stMetricLabel"] {
            color: #6154a4 !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }

        /* 🔲 Card Wrapper */
        div[data-testid="stHorizontalBlock"] > div {
            background-color: #ffffff !important;
            border: 2px solid #6154a4 !important;
            border-radius: 12px !important;
            padding: 20px !important;
            box-shadow: 0 4px 10px rgba(97, 84, 164, 0.15) !important;
            transition: all 0.3s ease-in-out;
        }

        div[data-testid="stHorizontalBlock"] > div:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 18px rgba(97, 84, 164, 0.25) !important;
        }

        div[data-testid="stHorizontalBlock"] {
            gap: 2rem !important;
        }

        /* 💜 Text and Fonts */
        html, body, [class*="css"] {
            font-family: "Poppins", sans-serif !important;
        }
        h1, h4, p, span {
            color: #4b3f72 !important;
        }

        /* 🎨 Gradient for Section Titles ONLY (keeps emojis colored normally) */
        h2, h3 {
            font-weight: 700 !important;
            background: linear-gradient(90deg, #6154a4, #a89bd9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }
        /* Keep emojis normal color beside gradient titles */
        h2::first-letter, h3::first-letter {
            -webkit-text-fill-color: initial !important;
        }

        /* 📦 Section Box */
        .section-box {
            background: #faf9ff;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 4px 10px rgba(97, 84, 164, 0.1);
            margin-bottom: 25px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 🌟 Header
    st.markdown("""
        <h1 style='display:flex;align-items:center;gap:10px;color:#4b3f72;'>
            <svg xmlns="http://www.w3.org/2000/svg" fill="#6154a4" height="32" width="32" viewBox="0 0 24 24">
                <path d="M3 17h2v-7H3v7zm4 0h2V7H7v10zm4 0h2v-4h-2v4zm4 0h2V4h-2v13zm4 0h2v-9h-2v9z"/>
            </svg>
            <b>Financial Insights Dashboard</b>
        </h1>
    """, unsafe_allow_html=True)
    st.markdown("Gain a clear and visually balanced overview of your financial health 💜")
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
                    "Income": "#6154a4", "Expenses": "#8b7fd4",
                    "Debt": "#a49ee0", "Savings": "#c3bff2"
                },
                title="Your Financial Composition"
            )
            fig1.update_layout(
                title_font=dict(size=18, color="#4b3f72", family="Poppins"),
                font=dict(size=13, family="Poppins", color="#4b3f72"),
                yaxis_title="Amount ($)",
                height=400,
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
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
                color_continuous_scale=["#c3bff2", "#8b7fd4", "#6154a4"],
                title="📊 Financial Ratios Overview"
            )
            fig2.update_layout(
                title_font=dict(size=18, color="#4b3f72", family="Poppins"),
                font=dict(size=13, family="Poppins", color="#4b3f72"),
                yaxis_title="Value",
                height=400,
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
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
# 💡 CLUSTER PAGE
# ----------------------------------------
elif page == "💡 Cluster":
    st.title("💡 Your Financial Cluster")

    if "last_input" not in st.session_state:
        st.warning("Please analyze your data first from the 'Financial Input' page.")
    else:
        try:
            response = requests.post(f"{API_URL}/cluster", json=st.session_state["last_input"])
            if response.status_code == 200:
                cluster_info = response.json()
                st.success("✅ Cluster analysis retrieved successfully!")

                # 🎯 Basic Info
                st.markdown(f"### 🏷️ **Cluster Name:** {cluster_info.get('cluster_name', 'N/A')}")
                st.markdown(f"**Description:** {cluster_info.get('description', 'No description available')}")
                st.markdown(f"**Health Status:** {cluster_info.get('health_status', 'N/A')}")

                st.markdown("---")

                # 📊 Comparison Section
                comp = cluster_info.get("comparison", {})
                st.subheader(f"📊 Comparison with Group: {comp.get('group_name', 'N/A')}")

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
                st.table(df_comp)

                st.markdown("---")

                # 💡 Characteristics Section
                st.subheader("💡 Cluster Characteristics")
                ch = cluster_info.get("characteristics", {})

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Cash Flow", ch.get("cash_flow", "N/A"))
                    st.metric("Emergency Fund", ch.get("emergency_fund", "N/A"))
                with col2:
                    st.metric("Expense Ratio", ch.get("expense_ratio", "N/A"))
                    st.metric("Debt Level", ch.get("debt_level", "N/A"))

            else:
                st.error("⚠️ Could not fetch cluster data.")
        except Exception as e:
            st.error(f"🚨 Error fetching cluster info: {e}")
# ----------------------------------------
# 🧠 PLAN PAGE - COMPREHENSIVE VERSION
# ----------------------------------------
elif page == "🧠 Plan":
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
                        st.success("✅ Personalized Plan Generated Successfully!")

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

                        st.markdown(f"**🎯 Top Priority:** {summary.get('top_priority', 'N/A')}")

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
                                hole=.3
                            )])
                            fig.update_layout(
                                title="Recommended Asset Allocation",
                                height=300
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
                                st.write(f"• {category}")
                            
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
                        st.caption(f"🕒 Plan generated at: {plan_data.get('generated_at', 'N/A')}")
                        st.caption("✨ Generated by Ezhalni Financial Health AI")

                    else:
                        st.warning("📋 No plan data returned from API.")
                else:
                    st.error(f"⚠️ Could not generate plan (HTTP {response.status_code})")

            except Exception as e:
                st.error(f"🚨 Error fetching plan: {e}")
                st.caption("Please try again or check your internet connection.")