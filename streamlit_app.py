import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file, header=[0, 1])
    # Simplify the headers by combining them into one level
    df.columns = [f'{i} - {j}' if j != 'Unnamed: 1_level_1' else f'{i}' for i, j in df.columns]
    return df

def main():
    st.title("Survey Data Explorer")

    uploaded_file = st.sidebar.file_uploader("Upload your CSV data", type=["csv"])
    
    if uploaded_file is not None:
        data = load_data(uploaded_file)
        
        # Display the questions (ignoring the respondent ID column)
        st.sidebar.header("Variables")
        questions = list(data.columns)[1:] # Exclude the 'Response ID' column
        selected_question = st.sidebar.selectbox("Select a question (variable)", questions)

        # Determine if the selected question is multi-select
        is_multi_select = 'YES' in data[selected_question].unique() or 'NO' in data[selected_question].unique()

        # Visualization options
        viz_type = st.sidebar.selectbox("Visualization type", ["Table", "Bar chart", "Pie chart"])

        # Prepare the data for visualization
        if is_multi_select:
            # For multi-select questions, aggregate all related columns
            related_columns = [col for col in data.columns if col.startswith(selected_question.split(' - ')[0])]
            multi_data = data[related_columns].apply(pd.Series.value_counts).fillna(0).T['YES']
            display_data = multi_data
        else:
            # For single-select questions, count the frequency of each answer
            display_data = data[selected_question].value_counts()

        # Display the data
        if viz_type == "Table":
            st.write(display_data)
        else:
            fig, ax = plt.subplots()
            if viz_type == "Bar chart":
                display_data.plot(kind='bar', ax=ax)
            elif viz_type == "Pie chart":
                display_data.plot(kind='pie', ax=ax, autopct='%1.1f%%')
            st.pyplot(fig)

if __name__ == "__main__":
    main()
