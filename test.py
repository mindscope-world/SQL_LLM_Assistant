import streamlit as st
import pandas as pd
import sqlite3
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.tools.pandas import PandasTools
import sys
import locale

# Set UTF-8 as the default encoding
if sys.getdefaultencoding() != 'utf-8':
    sys.setdefaultencoding('utf-8')

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


# Set up Streamlit app
st.title("SQL Data Assistant 🤖")
st.caption("Upload your dataset, ask a question, and get SQL queries with results!")

# Sidebar for user inputs
st.sidebar.header("SQL Input Panel")
openai_api_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password")
uploaded_file = st.sidebar.file_uploader("📂 Upload your file (CSV or Excel)", type=['csv', 'xlsx'])
user_question = st.sidebar.text_input("Enter your question", placeholder="e.g., What is the highest data_value?")

# Main Page Content
if openai_api_key:
    # Initialize the Assistant with OpenAI and PandasTools
    assistant = Assistant(
        llm=OpenAIChat(model="gpt-4o", api_key=openai_api_key),
        tools=[PandasTools()],
        show_tool_calls=True,
    )

    if uploaded_file:
        with st.spinner("Loading your data..."):
            try:
                # Load the uploaded file into a DataFrame
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file)
                else:
                    st.error("Unsupported file type!")
                    st.stop()
                
                st.subheader("Uploaded Data")
                st.write(df)

                # Normalize column names
                df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace(".", "_")
                st.subheader("Normalized Column Names")
                st.write(df.columns.tolist())

                # Process the user's question
                if user_question:
                    st.subheader(f"Your Question: {user_question}")

                    # Create an in-memory SQLite database
                    conn = sqlite3.connect(":memory:")
                    df.to_sql("uploaded_data", conn, if_exists="replace", index=False)

                    # Generate the SQL query dynamically
                    query_prompt = f"""
                    Here is the schema of a table created from the dataset:
                    {df.head(0).to_csv(index=False)}  # Only column names
                    Please write an SQL query to answer this question: "{user_question}".
                    """
                    with st.spinner("Generating SQL query..."):
                        sql_response = assistant.run(query_prompt, stream=False)

                    # Treat the response as a string
                    st.subheader("Assistant Response")
                    st.write(sql_response)

                    # Extract SQL query (assuming response starts with the query)
                    sql_lines = sql_response.split("\n")
                    sql_query = "\n".join(
                        line for line in sql_lines if line.strip().lower().startswith("select")
                    )

                    if not sql_query:
                        st.error("Could not extract SQL query from the response.")
                    else:
                        st.subheader("Generated SQL Query")
                        st.code(sql_query, language="sql")

                        try:
                            # Execute the SQL query and display the result
                            result_df = pd.read_sql_query(sql_query, conn)
                            st.subheader("Query Result")
                            st.write(result_df)
                        except Exception as e:
                            st.error(f"Error executing SQL query: {e}")
                        finally:
                            conn.close()
                else:
                    st.warning("Please enter a question in the sidebar.")
            except Exception as e:
                st.error(f"An error occurred while processing your data: {e}")
    else:
        st.warning("Please upload a file to continue.")
else:
    st.info("Enter your OpenAI API key in the sidebar to begin.")
