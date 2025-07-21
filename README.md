# OCR Bill Tracker

A full-stack **Streamlit** application that extracts information like **vendor**, **date**, and **amount** from uploaded **image receipts** using **EasyOCR**, then stores and visualizes them for insights.

---

## Features

- Upload receipt images (`.jpg`, `.png`)
- Extract data using EasyOCR (English only)
- Analyze total spend, filter by vendor/date/amount
- Visual charts for vendor spend and trends
- Save and retrieve data from SQLite database
- Export receipts to CSV or JSON

---

## Tech Stack

- **Frontend**: Streamlit  
- **OCR**: EasyOCR (English)  
- **Data Handling**: Pandas  
- **Visualization**: Matplotlib, Seaborn  
- **Database**: SQLite (via pandas)

---

## Watch App Demo

https://github.com/user-attachments/assets/4748d742-8264-4fcf-964b-33719560cfff
## Notes

- The app includes a feature to download receipt data as a CSV file.
- This functionality is **not shown in the demo video**, but is available in the UI.

