import streamlit as st
import pandas as pd
from backend import ocr_parser, db, algorithms


st.set_page_config(page_title="Receipt Reader", layout="centered")
st.title("Receipt Reader App")

uploaded_file = st.file_uploader("Upload a receipt (.jpg/.png/.pdf)", type=["jpg", "png", "pdf"])


if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Receipt", use_container_width=True)

    from PIL import Image
    import numpy as np

    image = Image.open(uploaded_file).convert("RGB")
    text = ocr_parser.extract_text(np.array(image))


    st.subheader("OCR Output")
    st.text(text)

    vendor = ocr_parser.extract_vendor(text)
    amount = ocr_parser.extract_amount(text)
    date = ocr_parser.extract_date(text)

    st.subheader("Parsed Fields")
    st.write(f"**Vendor:** {vendor}")
    st.write(f"**Date:** {date}")
    st.write(f"**Amount:** ₹{amount}")

    if st.button("Save to Database"):
        db.insert_receipt(vendor, date, amount)
        st.success("Saved successfully!")

# Show saved data
df = db.get_all_receipts()

st.subheader("Saved Receipts")
if not df.empty:
    st.dataframe(df)

    st.subheader("Filter & Search")
    vendor = st.text_input("Vendor contains:")
    min_amt = st.number_input("Minimum Amount", value=0.0)
    max_amt = st.number_input("Maximum Amount", value=100000.0)
    date_search = st.text_input("Date contains:")

    if st.button("Apply Filters"):
        if vendor:
            df = df[df["Vendor"].str.contains(vendor, case=False, na=False)]
        df = df[(df["Amount"] >= min_amt) & (df["Amount"] <= max_amt)]
        if date_search:
            df = df[df["Date"].str.contains(date_search, na=False)]

    st.subheader("Sort")
    df = algorithms.sort_data(df, st)
    st.dataframe(df)

    st.subheader("Stats & Trends")
    algorithms.show_charts(df, st)

    st.subheader("Export")
    st.download_button("Download CSV", df.to_csv(index=False), "receipts.csv")
    st.download_button("Download JSON", df.to_json(orient='records', indent=2), "receipts.json")
else:
    st.info("No receipts found.")