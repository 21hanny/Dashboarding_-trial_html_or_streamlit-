import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

# Page config
st.set_page_config(
    page_title="Investment Portfolio Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling inspired by the screenshot
st.markdown("""
    <style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global styles */
    .main {
        background-color: #f8fafb;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafb 100%);
        border-right: 1px solid #e5e9f0;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        padding-top: 2rem;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1f36;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        color: #6b7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Custom metric card */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        border: 1px solid #e5e9f0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1f36;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-change {
        font-size: 0.875rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .positive {
        color: #10b981;
    }
    
    .negative {
        color: #ef4444;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a1f36;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #3b82f6;
    }
    
    /* Card styling */
    .custom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        border: 1px solid #e5e9f0;
        margin-bottom: 1.5rem;
    }
    
    .card-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #1a1f36;
        margin-bottom: 1rem;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 1px solid #e5e9f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px 8px 0 0;
        padding: 0.75rem 1.5rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: #3b82f6;
        border-bottom: 2px solid #3b82f6;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);
        transform: translateY(-2px);
    }
    
    /* Table styling */
    .dataframe {
        font-size: 0.875rem;
    }
    
    .dataframe th {
        background-color: #f8fafb;
        color: #3b82f6;
        font-weight: 600;
        padding: 1rem;
        border-bottom: 2px solid #3b82f6;
    }
    
    .dataframe td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #e5e9f0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Stock tag styling */
    .stock-tag {
        display: inline-block;
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 1px solid #3b82f6;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 0.25rem;
        font-size: 0.875rem;
        color: #3b82f6;
        font-weight: 500;
    }
    
    /* Performance badge */
    .perf-badge {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    .perf-high {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
    }
    
    .perf-medium {
        background: rgba(249, 115, 22, 0.1);
        color: #f97316;
    }
    
    .perf-low {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
    }
    
    /* Header styling */
    .dashboard-header {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(59, 130, 246, 0.2);
    }
    
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .dashboard-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.125rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 💼 Investure")
    st.markdown("---")
    
    menu_options = {
        "📊 Dashboard": "dashboard",
        "💼 Stocks": "stocks",
        "🏦 Bonds": "bonds",
        "💎 Crypto": "crypto",
        "📈 ETFs": "etfs",
        "📖 Accounting": "accounting",
        "📊 Analytics": "analytics",
        "⚙️ Settings": "settings"
    }
    
    selected_page = st.radio("Navigation", list(menu_options.keys()), label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("#### 👤 Profile")
    st.markdown("**Sourabh Saini**")
    st.markdown("Professional Investor")
    
    st.markdown("---")
    if st.button("📧 Contact Adviser", use_container_width=True):
        st.info("Contact: sourabhsainihvd@gmail.com")

# Main Dashboard
st.markdown("""
    <div class="dashboard-header">
        <div class="dashboard-title">📊 Sourabh Saini's Investment Portfolio</div>
        <div class="dashboard-subtitle">Comprehensive Analysis | Multi-Sector Thematic | Performance Tracking</div>
    </div>
""", unsafe_allow_html=True)

# Top Metrics
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        label="My Portfolio XIRR",
        value="+145.74%",
        delta="Annualized Returns",
        delta_color="off"
    )

with col2:
    st.metric(
        label="vs NIFTY 50",
        value="+5.15x",
        delta="Outperformed by 117.44%",
        delta_color="off"
    )

with col3:
    st.metric(
        label="vs NIFTY Midcap 150",
        value="+3.25x",
        delta="Outperformed by 100.95%",
        delta_color="off"
    )

with col4:
    st.metric(
        label="Total Holdings",
        value="28+",
        delta="Across 10 Sectors",
        delta_color="off"
    )

with col5:
    st.metric(
        label="Equity Allocation",
        value="75-80%",
        delta="Thematic Small/Mid-Cap",
        delta_color="off"
    )

with col6:
    st.metric(
        label="Precious Metals",
        value="6-7%",
        delta="Gold (4%) + Silver (2-3%)",
        delta_color="off"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Total Invested Value Chart
st.markdown("### 📈 Portfolio Value Over Time")

# Sample data for the chart
dates = pd.date_range(start='2024-03-01', end='2024-06-01', freq='D')
values = 8000 + np.cumsum(np.random.randn(len(dates)) * 50) + np.linspace(0, 2350, len(dates))

fig_portfolio = go.Figure()
fig_portfolio.add_trace(go.Scatter(
    x=dates,
    y=values,
    mode='lines',
    name='Portfolio Value',
    line=dict(color='#10b981', width=2.5),
    fill='tozeroy',
    fillcolor='rgba(16, 185, 129, 0.1)'
))

fig_portfolio.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=40, b=20),
    paper_bgcolor='white',
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=True,
        gridcolor='#f0f0f0',
        title='Date'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#f0f0f0',
        title='Value ($)',
        tickprefix='$'
    ),
    hovermode='x unified',
    font=dict(family='Inter', size=12)
)

st.plotly_chart(fig_portfolio, use_container_width=True)

# Asset Summary Cards
st.markdown("### 💰 Asset Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="custom-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div class="metric-label">Stocks</div>
                    <div class="metric-value">$2,587.60</div>
                    <div class="metric-change positive">↑ +14.98% / month</div>
                </div>
                <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;">
                    📊
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="custom-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div class="metric-label">Bonds</div>
                    <div class="metric-value">$2,070.09</div>
                    <div class="metric-change positive">↑ +4.21% / month</div>
                </div>
                <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;">
                    🏦
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="custom-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div class="metric-label">Crypto</div>
                    <div class="metric-value">$1,552.56</div>
                    <div class="metric-change negative">↓ -10.90% / month</div>
                </div>
                <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;">
                    💎
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="custom-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div class="metric-label">ETFs</div>
                    <div class="metric-value">$4,140.17</div>
                    <div class="metric-change positive">↑ +10.55% / month</div>
                </div>
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;">
                    📈
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Three columns for detailed views
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🏆 Top Gainers")
    top_gainers = pd.DataFrame({
        'Company': ['Tesla Inc.', 'Shopify Inc.', 'Apple Inc.'],
        'Ticker': ['TSLA', 'SHOP', 'AAPL'],
        'Value': ['$870.76', '$462.82', '$107.72'],
        'Change': ['+17.12%', '+10.34%', '+4.23%']
    })
    
    for idx, row in top_gainers.iterrows():
        color = '#ef4444' if idx == 0 else '#1a1f36' if idx == 1 else '#000000'
        st.markdown(f"""
            <div class="custom-card" style="padding: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="background: {color}; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700;">
                            {row['Ticker'][0]}
                        </div>
                        <div>
                            <div style="font-weight: 600; color: #1a1f36;">{row['Company']}</div>
                            <div style="font-size: 0.875rem; color: #6b7280;">{row['Ticker']}</div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-weight: 700; color: #1a1f36;">{row['Value']}</div>
                        <div style="font-size: 0.875rem; color: #10b981; font-weight: 600;">{row['Change']}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📊 Diversification")
    
    # Donut chart
    fig_diversification = go.Figure(data=[go.Pie(
        labels=['ETFs', 'Stocks', 'Bonds', 'Crypto'],
        values=[40, 25, 20, 15],
        hole=.6,
        marker=dict(colors=['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6']),
        textposition='inside',
        textinfo='percent',
        hoverinfo='label+percent+value'
    )])
    
    fig_diversification.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        annotations=[dict(
            text='$4,140.17',
            x=0.5,
            y=0.5,
            font_size=20,
            font=dict(family='Inter', weight=700),
            showarrow=False
        )]
    )
    
    st.plotly_chart(fig_diversification, use_container_width=True)

with col3:
    st.markdown("### 💵 Dividend")
    
    # Sample dividend data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    values_2022 = [30, 45, 35, 50, 40, 55]
    values_2023 = [40, 50, 45, 60, 52, 70]
    
    fig_dividend = go.Figure()
    fig_dividend.add_trace(go.Bar(
        x=months,
        y=values_2022,
        name='2022',
        marker_color='#cbd5e1',
        width=0.4
    ))
    fig_dividend.add_trace(go.Bar(
        x=months,
        y=values_2023,
        name='2023',
        marker_color='#10b981',
        width=0.4
    ))
    
    fig_dividend.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='white',
        plot_bgcolor='white',
        barmode='group',
        bargap=0.3,
        xaxis=dict(
            showgrid=False,
            title=''
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#f0f0f0',
            title='',
            tickprefix='$'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        font=dict(family='Inter', size=11)
    )
    
    st.plotly_chart(fig_dividend, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Benchmark Comparison Section
st.markdown("### 🏆 My Portfolio Performance vs Benchmarks")

benchmark_col1, benchmark_col2, benchmark_col3, benchmark_col4 = st.columns(4)

with benchmark_col1:
    st.markdown("""
        <div class="custom-card" style="background: linear-gradient(135deg, #dc2626 0%, #7f1d1d 100%); border: 3px solid #fca5a5;">
            <div style="text-align: center; color: white;">
                <div style="font-size: 3em; margin-bottom: 10px;">📊</div>
                <div style="font-size: 0.75em; color: #fca5a5; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; margin-bottom: 8px;">NIFTY 50</div>
                <div style="font-size: 1.1em; margin-bottom: 10px;">Beaten By</div>
                <div style="font-size: 3em; font-weight: bold; color: #fef08a; margin-bottom: 8px;">+117.44%</div>
                <div style="font-size: 0.9em; font-weight: 600;">5.15x Multiple | +28.30% Index</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with benchmark_col2:
    st.markdown("""
        <div class="custom-card" style="background: linear-gradient(135deg, #0891b2 0%, #164e63 100%); border: 3px solid #67e8f9;">
            <div style="text-align: center; color: white;">
                <div style="font-size: 3em; margin-bottom: 10px;">📈</div>
                <div style="font-size: 0.75em; color: #67e8f9; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; margin-bottom: 8px;">NIFTY 500</div>
                <div style="font-size: 1.1em; margin-bottom: 10px;">Beaten By</div>
                <div style="font-size: 3em; font-weight: bold; color: #fef08a; margin-bottom: 8px;">+112.97%</div>
                <div style="font-size: 0.9em; font-weight: 600;">4.45x Multiple | +32.77% Index</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with benchmark_col3:
    st.markdown("""
        <div class="custom-card" style="background: linear-gradient(135deg, #ea580c 0%, #7c2d12 100%); border: 3px solid #fb923c;">
            <div style="text-align: center; color: white;">
                <div style="font-size: 3em; margin-bottom: 10px;">🎯</div>
                <div style="font-size: 0.75em; color: #fb923c; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; margin-bottom: 8px;">NIFTY MIDCAP 150</div>
                <div style="font-size: 1.1em; margin-bottom: 10px;">Beaten By</div>
                <div style="font-size: 3em; font-weight: bold; color: #fef08a; margin-bottom: 8px;">+100.95%</div>
                <div style="font-size: 0.9em; font-weight: 600;">3.25x Multiple | +44.79% Index</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with benchmark_col4:
    st.markdown("""
        <div class="custom-card" style="background: linear-gradient(135deg, #059669 0%, #064e3b 100%); border: 3px solid #6ee7b7;">
            <div style="text-align: center; color: white;">
                <div style="font-size: 3em; margin-bottom: 10px;">⭐</div>
                <div style="font-size: 0.75em; color: #6ee7b7; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; margin-bottom: 8px;">NIFTY SMALLCAP 250</div>
                <div style="font-size: 1.1em; margin-bottom: 10px;">Beaten By</div>
                <div style="font-size: 3em; font-weight: bold; color: #fef08a; margin-bottom: 8px;">+94.66%</div>
                <div style="font-size: 0.9em; font-weight: 600;">2.85x Multiple | +51.08% Index</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Realized Investment Wins
st.markdown("### 🎖️ Realized Investment Wins")

wins_col1, wins_col2, wins_col3 = st.columns(3)

realized_wins = [
    {"name": "Data Patterns", "return": "+60%", "sector": "Defense Electronics", "color": "#f59e0b"},
    {"name": "Apollo Micro Systems", "return": "+100%+", "sector": "Electronics", "color": "#ef4444"},
    {"name": "Zen Technologies", "return": "+30%", "sector": "Tech", "color": "#06b6d4"},
    {"name": "Suzlon Energy", "return": "+32%", "sector": "Renewables", "color": "#10b981"},
    {"name": "JSW Holdings", "return": "+106%", "sector": "Sector Inflection", "color": "#8b5cf6"},
    {"name": "Trent (Tata)", "return": "+32%", "sector": "Retail", "color": "#0066cc"}
]

for idx, win in enumerate(realized_wins):
    col_idx = idx % 3
    with [wins_col1, wins_col2, wins_col3][col_idx]:
        st.markdown(f"""
            <div class="custom-card" style="background: linear-gradient(135deg, #1f2937 0%, #111827 100%); border: 2px solid {win['color']};">
                <div style="text-align: center; color: white;">
                    <div style="color: {win['color']}; font-weight: 700; margin-bottom: 12px; font-size: 0.95em; letter-spacing: 0.5px; text-transform: uppercase;">
                        {win['name']}
                    </div>
                    <div style="color: #fef3c7; font-size: 2.5em; font-weight: 800; margin-bottom: 8px;">
                        {win['return']}
                    </div>
                    <div style="color: #d1d5db; font-size: 0.9em; font-weight: 500; margin-bottom: 12px;">
                        {win['sector']} | Exited
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Sector Allocation
st.markdown("### 🏢 Sector Allocation & Holdings")

tab1, tab2, tab3 = st.tabs(["📊 Visual Breakdown", "📋 Detailed View", "🏷️ All Stocks"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### My Sector Allocation")
        
        sector_data = {
            'Sector': ['Banking/Finance', 'Energy', 'Defense/Tech', 'Infrastructure', 
                      'Pharma', 'Retail', 'Automotive', 'Real Estate', 'Electronics', 'Chemicals'],
            'Allocation': [25, 20, 20, 15, 8, 7, 10, 5, 5, 5]
        }
        
        colors = ['#3498db', '#f39c12', '#e74c3c', '#9b59b6', '#16a085', 
                 '#8e44ad', '#1abc9c', '#34495e', '#e67e22', '#c0392b']
        
        fig_sector = go.Figure(data=[go.Pie(
            labels=sector_data['Sector'],
            values=sector_data['Allocation'],
            hole=.4,
            marker=dict(colors=colors),
            textposition='outside',
            textinfo='label+percent'
        )])
        
        fig_sector.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='white',
            font=dict(family='Inter', size=12)
        )
        
        st.plotly_chart(fig_sector, use_container_width=True)
    
    with col2:
        st.markdown("#### Legend & Distribution")
        
        legend_items = [
            ("Banking/Finance", "25% | PSU Turnaround + Fintech", "#3498db"),
            ("Energy", "20% | Green Transition", "#f39c12"),
            ("Defense/Tech", "20% | Modernization", "#e74c3c"),
            ("Infrastructure", "15% | Capex Cycle", "#9b59b6"),
            ("Pharma", "8% | Healthcare Growth", "#16a085"),
            ("Retail", "7% | Consumption Boom", "#8e44ad"),
            ("Automotive", "10% | EV Transition", "#1abc9c"),
            ("Real Estate", "5% | Distressed Recovery", "#34495e"),
            ("Electronics", "5% | PLI Scheme", "#e67e22"),
            ("Chemicals", "5% | Specialty Chemicals", "#c0392b")
        ]
        
        for name, desc, color in legend_items:
            st.markdown(f"""
                <div style="display: flex; align-items: center; margin-bottom: 12px; padding: 10px; background: white; border-radius: 8px; border: 1px solid #e5e9f0;">
                    <div style="width: 20px; height: 20px; background: {color}; border-radius: 4px; margin-right: 12px;"></div>
                    <div>
                        <div style="font-weight: 600; color: #1a1f36;">{name}</div>
                        <div style="font-size: 0.875rem; color: #6b7280;">{desc}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("#### Sector Details")
    
    sector_details = pd.DataFrame({
        'Sector': ['Banking/Finance', 'Energy', 'Defense/Tech', 'Infrastructure', 'Pharmaceutical', 
                  'Retail', 'Automotive', 'Real Estate', 'Electronics', 'Chemicals'],
        'Allocation': ['25%', '20%', '20%', '15%', '8%', '7%', '10%', '5%', '5%', '5%'],
        'Key Holdings': [
            'NSDL, Yes Bank, BoI, BoM',
            'Suzlon, IEX, Jaiprakash, RattanIndia',
            'Data Patterns, DCX Systems, KPIT, Vimta',
            'Tata Steel, NMDC Steel, Tilaknagar',
            'Sun Pharma, Divi\'s Lab, Mankind',
            'Trent (32% exit), Raymonds, Alok, Trident, ITC',
            'Tata Motors',
            'Parsvnath Developers',
            'MIRC Electronics',
            'Aether Industry'
        ],
        'Investment Thesis': [
            'PSU turnaround + fintech infrastructure',
            'Traditional + green energy transition',
            'Defense modernization + tech innovation',
            'Capex cycle + materials demand',
            'Healthcare growth + export potential',
            'Consumption boom + premiumization',
            'EV transition + electrification',
            'Distressed asset recovery',
            'PLI scheme benefits',
            'Specialty chemicals demand'
        ]
    })
    
    st.dataframe(sector_details, use_container_width=True, hide_index=True)

with tab3:
    st.markdown("#### All Stock Holdings")
    
    sectors_stocks = {
        '🏦 Banking & Finance (25%)': ['NSDL', 'Yes Bank', 'BoI', 'BoM'],
        '⚡ Energy & Renewables (20%)': ['Suzlon', 'IEX', 'Jaiprakash', 'RattanIndia'],
        '🛡️ Defense & Tech (20%)': ['Data Patterns', 'DCX Systems', 'KPIT', 'Vimta Labs'],
        '🏗️ Infrastructure & Materials (15%)': ['Tata Steel', 'NMDC Steel', 'Tilaknagar'],
        '💊 Pharmaceuticals (8%)': ['Sun Pharma', 'Divi\'s Lab', 'Mankind'],
        '🛍️ Retail & Fashion (7%)': ['Trent ✓', 'Raymonds', 'Alok Industries', 'Trident', 'ITC'],
        '🚗 Automotive (10%)': ['Tata Motors'],
        '🏢 Real Estate (5%)': ['Parsvnath'],
        '📱 Electronics (5%)': ['MIRC'],
        '🧪 Chemicals (5%)': ['Aether Industry']
    }
    
    cols = st.columns(2)
    for idx, (sector, stocks) in enumerate(sectors_stocks.items()):
        with cols[idx % 2]:
            st.markdown(f"**{sector}**")
            stock_html = " ".join([f'<span class="stock-tag">{stock}</span>' for stock in stocks])
            st.markdown(f'<div style="margin-bottom: 20px;">{stock_html}</div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Contact Section
st.markdown("""
    <div class="custom-card" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); border: 2px solid #0066cc; text-align: center; padding: 2rem;">
        <h2 style="color: #ffffff; font-size: 2em; margin-bottom: 20px; font-weight: 800;">🚀 Interested in My Investment Approach?</h2>
        <p style="color: rgba(255,255,255,0.95); font-size: 1.05em; margin-bottom: 30px; line-height: 1.8;">
            I'm actively exploring opportunities in <strong style="color: #fbbf24;">portfolio management, investment research, and VC/hedge fund analyst roles</strong>.
            <br><br>My systematic thematic investing approach has delivered 145%+ XIRR with consistent outperformance. Let's connect to discuss opportunities.
        </p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("📧 Get in Touch", use_container_width=True):
        st.success("Email: sourabhsainihvd@gmail.com")
    if st.button("💼 LinkedIn Profile", use_container_width=True):
        st.success("https://www.linkedin.com/in/sourabh-saini-tum/")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.875rem; padding: 20px;">
        <p>📊 Portfolio Dashboard | Last Updated: December 2025 | Data-Driven Investment Analysis</p>
        <p>🎓 This dashboard analyzes a sophisticated multi-sector thematic portfolio with 145.74% XIRR | Designed for informed decision-making and risk management</p>
    </div>
""", unsafe_allow_html=True)
