import streamlit as st
import pandas as pd
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.tools.pandas import PandasTools

# Set up Streamlit app
st.title("SQL Data Assistant 🤖")
st.caption("Upload your dataset, ask a question, and get SQL queries with results!")

# Sidebar for user inputs
st.sidebar.header("SQL Input Panel")
openai_api_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password")
uploaded_file = st.sidebar.file_uploader("📂 Upload your file (CSV or Excel)", type=['csv', 'xlsx'])
user_question = st.sidebar.text_input("❓ Enter your question", placeholder="e.g., What is the highest salary?")

# Main Page Content
if openai_api_key:
    # Initialize the Assistant with OpenAI and PandasTools
    assistant = Assistant(
        llm=OpenAIChat(model="gpt-4o", api_key=openai_api_key),
        tools=[PandasTools()],
        show_tool_calls=True,
    )

    if uploaded_file:
        # Load the uploaded file into a DataFrame
        with st.spinner("Loading your data..."):
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file)
                else:
                    st.error("Unsupported file type!")
                    st.stop()
                
                st.subheader("Uploaded Data")
                st.write(df)

                # Summarize or sample the DataFrame to reduce size
                df_summary = df.describe(include='all').transpose()  # Summary statistics
                df_sample = df.head(100)  # Take a small sample of rows
                
                # Convert the summary/sample to a string for processing
                summary_as_string = df_summary.to_csv(index=True)
                sample_as_string = df_sample.to_csv(index=False)

                # Process the user's question
                if user_question:
                    st.subheader(f"Your Question: {user_question}")
                    with st.spinner("Processing your question..."):
                        query = f"""
                        Here is a sample of the dataset:
                        ```
                        {sample_as_string}
                        ```
                        And here is a summary of the dataset:
                        ```
                        {summary_as_string}
                        ```
                        Please answer the following question: {user_question}. 
                        Provide the SQL query and result as output.
                        """
                        response = assistant.run(query, stream=False)
                        
                        # Debugging: Display the full response
                        st.subheader("Response Object")
                        st.write(response)

                        # Adjust to access the correct parts of the response
                        if hasattr(response, 'tool_output') and hasattr(response, 'content'):
                            st.subheader("Generated SQL Query")
                            st.code(response.tool_output, language="sql")  # Display the SQL query

                            st.subheader("Query Result")
                            st.write(response.content)  # Display the query result
                        else:
                            st.error("Unexpected response format. Check the response structure.")
                else:
                    st.warning("Please enter a question in the sidebar.")
            except Exception as e:
                st.error(f"An error occurred while processing your data: {e}")
    else:
        st.warning("Please upload a file to continue.")
else:
    st.info("Enter your OpenAI API key in the sidebar to begin.")
