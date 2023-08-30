import streamlit as st
import pandas as pd
import os
from fuzzywuzzy import process

def fuzzy_match_names(known_names, input_name):
    best_match = process.extractOne(input_name, known_names, scorer=process.fuzz.ratio)
    return best_match[0] if best_match[1] >= 80 else "No match found"

def main():
    st.title("Fuzzy Name Matcher")

    # Upload multiple CSV files
    uploaded_files = st.file_uploader("Upload CSV Files", type="csv", accept_multiple_files=True, key="upload")

    if uploaded_files:
        column_names = []  # List to store column names in all uploaded CSV files
        
        # Iterate through uploaded CSV files and extract column names
        for csv_file in uploaded_files:
            df = pd.read_csv(csv_file)
            column_names.extend(df.columns.tolist())
        
        # Auto-detect columns that might contain names (based on common naming patterns)
        possible_name_columns = [col for col in column_names if "name" in col.lower()]
        
        if not possible_name_columns:
            st.warning("No potential name columns found in the uploaded files.")
            return
        
        name_column = st.selectbox("Select the column containing names:", possible_name_columns)
        
        known_names = []  # List to store known names
        # Iterate through uploaded CSV files and extract names from the selected column
        for csv_file in uploaded_files:
            df = pd.read_csv(csv_file)
            known_names.extend(df[name_column].tolist())
        
        input_name = st.text_input("Enter the name to match:", key="input_name")
        
        if st.button("Match Name"):
            matched_name = fuzzy_match_names(known_names, input_name)
            st.success(f"Best match: {matched_name}")
            
            # Create a DataFrame with the original names and the matched names
            result_df = pd.DataFrame({
                "Original Names": known_names,
                "Fuzzy Matched Names": [fuzzy_match_names(known_names, name) for name in known_names]
            })
            
            st.write("Matched Names:")
            st.dataframe(result_df)

if __name__ == "__main__":
    main()


