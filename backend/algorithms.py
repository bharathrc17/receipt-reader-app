import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def sort_data(df, st):
    if df.empty:
        st.warning("No data available to sort.")
        return df

    sort_columns = [col for col in ["Vendor", "Amount", "Date"] if col in df.columns]
    if not sort_columns:
        st.warning("No sortable columns found.")
        return df

    by = st.selectbox("Sort by", sort_columns)
    order = st.radio("Order", ["Ascending", "Descending"])
    return df.sort_values(by=by, ascending=(order == "Ascending"))

def show_charts(df, st):
    if df.empty or "Amount" not in df.columns:
        st.warning("Not enough data to generate charts.")
        return
    st.subheader("Statistics")
    st.write(f"**Total Spent:** ₹{df['Amount'].sum():,.2f}")
    st.write(f"**Mean:** ₹{df['Amount'].mean():,.2f}")
    st.write(f"**Median:** ₹{df['Amount'].median():,.2f}")
    st.write(f"**Mode:** ₹{df['Amount'].mode()[0]:,.2f}" if not df['Amount'].mode().empty else "**Mode:** N/A")

    # Vendor bar chart
    if "Vendor" in df.columns:
        st.subheader("Spend per Vendor")
        vendor_summary = df.groupby("Vendor")["Amount"].sum().sort_values(ascending=False)
        st.bar_chart(vendor_summary)

    # Monthly line chart
    if "Date" in df.columns:
        st.subheader("Monthly Spend Trend")
        try:
            df["Parsed Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df["Month"] = df["Parsed Date"].dt.to_period("M").astype(str)
            monthly = df.groupby("Month")["Amount"].sum()
            if len(monthly) > 1:
                st.line_chart(monthly)
            else:
                st.info("Not enough data for trend (only one month present).")
        except Exception as e:
            st.warning(f"Date format issue — skipping trend chart. {e}")
