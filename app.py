import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Super Store Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("Data/final_data.csv")

df = load_data()

# ---------------- Sidebar ---------------- #

st.sidebar.title("📊 Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📈 Analytics",
        "🖼️ Power BI Dashboard",
        "📋 Dataset",
        "👨‍💻 About"
    ]
)

st.sidebar.markdown("---")

regions = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

categories = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

segments = st.sidebar.multiselect(
    "Segment",
    df["Segment"].unique(),
    default=df["Segment"].unique()
)

filtered = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Segment"].isin(segments))
]

# ---------------- Home ---------------- #

if page=="🏠 Home":

    st.title("📊 Super Store Sales Analysis Dashboard")

    st.caption("Interactive Business Intelligence Dashboard | Python • Streamlit • Plotly • Power BI")

    st.markdown("---")

    total_sales = filtered["Sales"].sum()
    total_profit = filtered["Profit"].sum()
    total_orders = filtered["Order ID"].nunique()
    avg_sales = filtered["Sales"].mean()

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("💰 Total Sales",f"${total_sales:,.0f}")

    c2.metric("📈 Total Profit",f"${total_profit:,.0f}")

    c3.metric("📦 Orders",total_orders)

    c4.metric("🛒 Average Sale",f"${avg_sales:,.2f}")

    st.markdown("---")

    left,right=st.columns(2)




        # ================= SALES TREND =================

    monthly_sales = (
        filtered.groupby("Order month", as_index=False)["Sales"]
        .sum()
        .sort_values("Order month")
    )

    fig1 = px.line(
        monthly_sales,
        x="Order month",
        y="Sales",
        markers=True,
        title="📈 Monthly Sales Trend"
    )

    fig1.update_layout(height=450)

    left.plotly_chart(fig1, use_container_width=True)

    # ================= CATEGORY SALES =================

    category_sales = (
        filtered.groupby("Category", as_index=False)["Sales"]
        .sum()
    )

    fig2 = px.pie(
        category_sales,
        values="Sales",
        names="Category",
        hole=0.45,
        title="💰 Sales by Category"
    )

    right.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ================= SECOND ROW =================

    left2, right2 = st.columns(2)

    region_profit = (
        filtered.groupby("Region", as_index=False)["Profit"]
        .sum()
    )

    fig3 = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        color="Region",
        title="🌍 Profit by Region"
    )

    left2.plotly_chart(fig3, use_container_width=True)

    segment_sales = (
        filtered.groupby("Segment", as_index=False)["Sales"]
        .sum()
    )

    fig4 = px.bar(
        segment_sales,
        x="Segment",
        y="Sales",
        color="Segment",
        title="👥 Sales by Customer Segment"
    )

    right2.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # ================= TOP PRODUCTS =================

    top_products = (
        filtered.groupby("Product Name", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(10)
    )

    fig5 = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        title="🏆 Top 10 Products by Sales"
    )

    fig5.update_layout(height=500)

    st.plotly_chart(fig5, use_container_width=True)



    # ============================================================
# ANALYTICS PAGE
# ============================================================

elif page=="📈 Analytics":

    st.title("📈 Advanced Business Analytics")

    c1,c2=st.columns(2)

    yearly=filtered.groupby("Order year",as_index=False)[["Sales","Profit"]].sum()

    fig=px.bar(
        yearly,
        x="Order year",
        y="Sales",
        color="Profit",
        title="Yearly Sales & Profit"
    )

    c1.plotly_chart(fig,use_container_width=True)

    sub=filtered.groupby("Sub-Category",as_index=False)["Profit"].sum()

    fig=px.bar(
        sub.sort_values("Profit"),
        x="Profit",
        y="Sub-Category",
        orientation="h",
        title="Profit by Sub-Category"
    )

    c2.plotly_chart(fig,use_container_width=True)

    st.markdown("---")

    corr=filtered[["Sales","Profit","Quantity","Discount"]].corr()

    fig=px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="Blues",
        title="Correlation Matrix"
    )

    st.plotly_chart(fig,use_container_width=True)

# ============================================================
# POWER BI PAGE
# ============================================================

elif page=="🖼️ Power BI Dashboard":

    st.title("🖼️ Power BI Dashboard Preview")

    st.info("These dashboards were created in Microsoft Power BI.")

    c1,c2=st.columns(2)

    with c1:
        st.image(
            "Dashboard/overall_sales.png",
            caption="Overall Sales Dashboard",
            use_container_width=True
        )

    with c2:
        st.image(
            "Dashboard/segment_dashboard.png",
            caption="Segment Dashboard",
            use_container_width=True
        )

    c3,c4=st.columns(2)

    with c3:
        st.image(
            "Dashboard/sales_dashboard.png",
            caption="Sales Dashboard",
            use_container_width=True
        )

    with c4:
        st.image(
            "Dashboard/Profit_dashboard.png",
            caption="Profit Dashboard",
            use_container_width=True
        )



        # ============================================================
# DATASET PAGE
# ============================================================

elif page=="📋 Dataset":

    st.title("📋 Dataset Explorer")

    st.write("Preview of the filtered dataset.")

    st.dataframe(filtered, use_container_width=True)

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Filtered Dataset",
        data=csv,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )

# ============================================================
# ABOUT PAGE
# ============================================================

elif page=="👨‍💻 About":

    st.title("👨‍💻 About the Developer")

    st.markdown("## Apoorva Gupta")

    st.write("""
Aspiring **Data Analyst / Business Analyst** passionate about transforming raw data into meaningful business insights through analytics and interactive dashboards.

### Skills
- Python
- SQL
- Power BI
- Excel
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- Plotly

### Project
**Super Store Sales Analysis & Interactive Dashboard**

This project demonstrates end-to-end data analysis including:
- Data Cleaning
- Exploratory Data Analysis (EDA)
- Business Insights
- Interactive Dashboard Development
- Power BI Visualization
""")

    c1, c2 = st.columns(2)

    with c1:
        st.link_button(
            "💻 GitHub",
            "https://github.com/apoorvagupta9068"
        )

    with c2:
        st.link_button(
            "🔗 LinkedIn",
            "https://www.linkedin.com/in/apoorva-g-9ba552253/"
        )

    st.markdown("---")

    st.success("Thank you for visiting this project! ⭐")

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
"""
<div style='text-align:center; color:gray; font-size:15px;'>

Developed by <b>Apoorva Gupta</b>

<br><br>

📊 Python • Streamlit • Plotly • Power BI

</div>
""",
unsafe_allow_html=True
)