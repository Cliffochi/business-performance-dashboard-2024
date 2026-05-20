import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Business Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #F8FAFC; }
  [data-testid="stSidebar"] { background: #1A2E4A; }
  [data-testid="stSidebar"] * { color: #E2E8F0 !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stMultiSelect label { color: #93C5FD !important; font-weight: 600; }
  .metric-card {
    background: #1A2E4A; border-radius: 12px; padding: 20px 24px;
    color: white; border-top: 4px solid #2563EB;
  }
  .metric-label { font-size: 11px; font-weight: 700; color: #93C5FD;
                  letter-spacing: .08em; text-transform: uppercase; margin-bottom: 6px; }
  .metric-value { font-size: 28px; font-weight: 800; color: #fff; line-height: 1.1; }
  .metric-sub   { font-size: 12px; color: #64748B; margin-top: 4px; }
  .insight-card {
    background: white; border-radius: 10px; padding: 18px 22px;
    border-left: 5px solid #2563EB; margin-bottom: 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,.06);
  }
  .insight-title { font-size: 14px; font-weight: 700; color: #1A2E4A; margin-bottom: 6px; }
  .insight-body  { font-size: 13px; color: #475569; margin-bottom: 8px; line-height: 1.6; }
  .insight-action{
    font-size: 12px; font-weight: 600; color: #166534;
    background: #DCFCE7; padding: 8px 12px; border-radius: 6px;
  }
  .section-header {
    font-size: 13px; font-weight: 700; color: #1A2E4A;
    text-transform: uppercase; letter-spacing: .07em;
    border-bottom: 2px solid #DBEAFE; padding-bottom: 6px; margin-bottom: 14px;
  }
  .stTabs [data-baseweb="tab"] { font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel(
        "Business_Data_Sample_Dashboard_main.xlsx",
        sheet_name="Raw Data"
    )
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df_raw = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Dashboard Filters")
    st.markdown("---")

    quarters = ["All"] + sorted(df_raw["Quarter"].unique().tolist())
    sel_quarter = st.selectbox("Quarter", quarters)

    regions = ["All"] + sorted(df_raw["Region"].unique().tolist())
    sel_region = st.selectbox("Region", regions)

    categories = ["All"] + sorted(df_raw["Category"].unique().tolist())
    sel_category = st.selectbox("Category", categories)

    channels = ["All"] + sorted(df_raw["Channel"].unique().tolist())
    sel_channel = st.selectbox("Channel", channels)

    st.markdown("---")
    st.markdown("**Prepared by:** Cliff Ochieng'")
    st.markdown("**Period:** Full Year 2024")
    st.markdown("**Data:** 500 transactions")

# ── Apply filters ─────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_quarter   != "All": df = df[df["Quarter"]  == sel_quarter]
if sel_region    != "All": df = df[df["Region"]   == sel_region]
if sel_category  != "All": df = df[df["Category"] == sel_category]
if sel_channel   != "All": df = df[df["Channel"]  == sel_channel]

# ── KPIs ──────────────────────────────────────────────────────────────────────
total_rev    = df["Revenue"].sum()
total_profit = df["Gross Profit"].sum()
total_units  = df["Units"].sum()
avg_order    = df["Revenue"].mean() if len(df) else 0
margin_pct   = (total_profit / total_rev * 100) if total_rev else 0

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:#1A2E4A;padding:20px 28px;border-radius:12px;margin-bottom:24px'>
  <span style='font-size:22px;font-weight:800;color:white'>
    📊 BUSINESS PERFORMANCE DASHBOARD
  </span>
  <span style='font-size:13px;color:#64748B;margin-left:16px'>Full Year 2024  •  Sample Report</span>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
cards = [
    (k1, "TOTAL REVENUE",    f"${total_rev:,.0f}",    "Full Year 2024"),
    (k2, "GROSS PROFIT",     f"${total_profit:,.0f}", f"{margin_pct:.1f}% margin"),
    (k3, "UNITS SOLD",       f"{total_units:,}",      "Across all categories"),
    (k4, "AVG ORDER VALUE",  f"${avg_order:,.0f}",    "Per transaction"),
]
for col, label, value, sub in cards:
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📈 Charts", "📋 Data Table", "💡 Key Insights"])

COLORS = ["#2563EB","#1A2E4A","#F59E0B","#16A34A","#DC2626",
          "#7C3AED","#0891B2","#EA580C"]

with tab1:
    row1_l, row1_r = st.columns(2)

    # Chart 1 – Revenue by Region (bar)
    with row1_l:
        st.markdown('<div class="section-header">Revenue by Region</div>', unsafe_allow_html=True)
        reg = df.groupby("Region")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=True)
        fig1 = px.bar(reg, x="Revenue", y="Region", orientation="h",
                      color="Revenue", color_continuous_scale=["#DBEAFE","#2563EB"],
                      text=reg["Revenue"].apply(lambda x: f"${x:,.0f}"))
        fig1.update_traces(textposition="outside", textfont_size=11)
        fig1.update_layout(
            height=300, margin=dict(l=10, r=30, t=10, b=10),
            coloraxis_showscale=False, paper_bgcolor="white",
            plot_bgcolor="white", xaxis_title=None, yaxis_title=None,
            font=dict(family="Arial"), xaxis=dict(showgrid=True, gridcolor="#F1F5F9")
        )
        st.plotly_chart(fig1, use_container_width=True)

    # Chart 2 – Revenue by Category (pie)
    with row1_r:
        st.markdown('<div class="section-header">Revenue by Category</div>', unsafe_allow_html=True)
        cat = df.groupby("Category")["Revenue"].sum().reset_index()
        fig2 = px.pie(cat, values="Revenue", names="Category",
                      color_discrete_sequence=COLORS, hole=0.45)
        fig2.update_traces(textposition="outside", textinfo="label+percent",
                           textfont_size=11)
        fig2.update_layout(
            height=300, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="white", showlegend=False,
            font=dict(family="Arial")
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Chart 3 – Monthly Revenue Trend (line)
    st.markdown('<div class="section-header">Monthly Revenue Trend</div>', unsafe_allow_html=True)
    monthly = df.groupby(df["Date"].dt.to_period("M"))["Revenue"].sum().reset_index()
    monthly["Date"] = monthly["Date"].astype(str)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=monthly["Date"], y=monthly["Revenue"],
        mode="lines+markers", line=dict(color="#2563EB", width=3),
        marker=dict(size=7, color="#1A2E4A"),
        fill="tozeroy", fillcolor="rgba(37,99,235,0.08)",
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>"
    ))
    fig3.update_layout(
        height=280, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(showgrid=False, tickangle=-30),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9",
                   tickformat="$,.0f"),
        font=dict(family="Arial")
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Chart 4 – Revenue by Channel
    row2_l, row2_r = st.columns(2)
    with row2_l:
        st.markdown('<div class="section-header">Revenue by Channel</div>', unsafe_allow_html=True)
        ch = df.groupby("Channel")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False)
        fig4 = px.bar(ch, x="Channel", y="Revenue",
                      color="Channel", color_discrete_sequence=COLORS,
                      text=ch["Revenue"].apply(lambda x: f"${x:,.0f}"))
        fig4.update_traces(textposition="outside", textfont_size=11)
        fig4.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="white", plot_bgcolor="white",
            showlegend=False, xaxis_title=None, yaxis_title=None,
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
            font=dict(family="Arial")
        )
        st.plotly_chart(fig4, use_container_width=True)

    with row2_r:
        st.markdown('<div class="section-header">Gross Profit by Category</div>', unsafe_allow_html=True)
        gp = df.groupby("Category").agg(
            Revenue=("Revenue","sum"), Profit=("Gross Profit","sum")
        ).reset_index()
        gp["Margin"] = gp["Profit"] / gp["Revenue"] * 100
        fig5 = px.bar(gp, x="Category", y="Margin",
                      color="Margin", color_continuous_scale=["#DBEAFE","#1A2E4A"],
                      text=gp["Margin"].apply(lambda x: f"{x:.1f}%"))
        fig5.update_traces(textposition="outside", textfont_size=11)
        fig5.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="white", plot_bgcolor="white",
            coloraxis_showscale=False, xaxis_title=None,
            yaxis=dict(title="Margin %", showgrid=True, gridcolor="#F1F5F9"),
            font=dict(family="Arial")
        )
        st.plotly_chart(fig5, use_container_width=True)

with tab2:
    st.markdown('<div class="section-header">Transaction Data</div>', unsafe_allow_html=True)
    search = st.text_input("🔍 Search by region, category, rep or channel", "")
    display_df = df.copy()
    if search:
        mask = display_df.apply(
            lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1
        )
        display_df = display_df[mask]

    display_df["Date"] = display_df["Date"].dt.strftime("%d-%b-%Y")
    display_df["Revenue"]      = display_df["Revenue"].apply(lambda x: f"${x:,.2f}")
    display_df["Gross Profit"] = display_df["Gross Profit"].apply(lambda x: f"${x:,.2f}")
    display_df["Unit Price"]   = display_df["Unit Price"].apply(lambda x: f"${x:,.2f}")
    display_df["Cost"]         = display_df["Cost"].apply(lambda x: f"${x:,.2f}")
    st.dataframe(display_df, use_container_width=True, height=480)
    st.caption(f"Showing {len(display_df):,} of {len(df):,} transactions")

with tab3:
    top_region  = df.groupby("Region")["Revenue"].sum().idxmax() if len(df) else "N/A"
    top_region_pct = (df.groupby("Region")["Revenue"].sum().max() / total_rev * 100) if total_rev else 0
    top_cat     = df.groupby("Category")["Revenue"].sum().idxmax() if len(df) else "N/A"
    top_cat_pct = (df.groupby("Category")["Revenue"].sum().max() / total_rev * 100) if total_rev else 0
    bot_region  = df.groupby("Region")["Revenue"].sum().idxmin() if len(df) else "N/A"
    top_ch      = df.groupby("Channel")["Revenue"].sum().idxmax() if len(df) else "N/A"
    top_ch_pct  = (df.groupby("Channel")["Revenue"].sum().max() / total_rev * 100) if total_rev else 0
    best_q      = df.groupby("Quarter")["Revenue"].sum().idxmax() if len(df) else "N/A"
    worst_q     = df.groupby("Quarter")["Revenue"].sum().idxmin() if len(df) else "N/A"

    insights = [
        (
            f"1. {top_region} Drives {top_region_pct:.0f}% of Total Revenue",
            f"{top_region} is the single largest revenue contributor at {top_region_pct:.1f}% of the total. "
            f"If resources are spread equally across all regions, the business is underinvesting where it matters most.",
            f"ACTION: Prioritise {top_region} for stock allocation, sales rep coverage, and promotional spend. "
            f"A 10% increase in {top_region} alone outweighs a 25% increase in {bot_region}."
        ),
        (
            f"2. {top_cat} Leads in Revenue — But Watch the Margin",
            f"{top_cat} leads at {top_cat_pct:.1f}% of total sales. "
            f"The overall gross margin sits at {margin_pct:.1f}%. "
            f"High-revenue categories don't always mean high-profit categories.",
            f"ACTION: Calculate margin per category individually. "
            f"If {top_cat} margin is below {margin_pct:.1f}%, a lower-volume category may be more profitable per unit sold."
        ),
        (
            f"3. {best_q} Is the Peak Quarter — Capitalise on It",
            f"Revenue peaks in {best_q} and dips in {worst_q}. "
            f"Seasonal patterns are predictable — and most businesses ignore them until it's too late.",
            f"ACTION: Stock up and staff up ahead of {best_q}. "
            f"Run retention campaigns in {worst_q} to lift the trough. "
            f"Even a 5% uplift in the low quarter meaningfully changes annual performance."
        ),
        (
            f"4. {top_ch} Is the Dominant Sales Channel at {top_ch_pct:.0f}%",
            f"Over-reliance on one channel creates fragility. "
            f"If the {top_ch} channel underperforms, the whole business feels it.",
            f"ACTION: Set a target to grow the second-largest channel by 15% over 6 months. "
            f"Diversified channels provide stability and open new customer segments."
        ),
        (
            f"5. Avg Order Value of ${avg_order:,.0f} Signals a Pricing Opportunity",
            f"At ${avg_order:,.0f} per transaction, there is room to increase order value "
            f"through bundling, minimum order thresholds, or upselling adjacent products.",
            f"ACTION: Introduce a 'buy more, save more' structure or a free-delivery threshold "
            f"just above ${avg_order*1.2:,.0f}. A 10% lift in order value adds "
            f"${total_rev*0.10:,.0f} without acquiring a single new customer."
        ),
    ]

    colors = ["#2563EB","#1A2E4A","#0F4C81","#1E3A5F","#164E63"]
    for (title, body, action), color in zip(insights, colors):
        st.markdown(f"""
        <div class="insight-card" style="border-left-color:{color}">
          <div class="insight-title">{title}</div>
          <div class="insight-body">{body}</div>
          <div class="insight-action">💡 {action}</div>
        </div>""", unsafe_allow_html=True)
