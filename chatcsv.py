import streamlit as st
import pandas as pd
import json

import os
import openai
from langchain.llms import AzureOpenAI
from langchain.embeddings import OpenAIEmbeddings

from langchain.agents import create_pandas_dataframe_agent
from langchain.agents import create_csv_agent
import pandas as pd
from dotenv import load_dotenv
from streamlit_chat import message
from tempfile import NamedTemporaryFile


#from agent import csv_agent , query_agent

load_dotenv()

API_KEY = os.getenv("apikey")
BASE_ENDPOINT = os.getenv("api_base")
COMPLETION_MODEL = os.getenv("completion_model")
CHAT_MODEL = os.getenv("chat_model")
EMBEDDING_MODEL = os.getenv("embedding_model")
API_VERSION = os.getenv("api_version")

#init Azure OpenAI
openai.api_type = "azure"
openai.api_version = API_VERSION
openai.api_base = BASE_ENDPOINT
openai.api_key = API_KEY

#saveDir = "./data"


# if csv_file is not None:
#     csv_file_details = {"FileName":csv_file.name,"FileType":csv_file.type}
#     st.write(csv_file_details)
#     with open(os.path.join("saveDir", csv_file.name), "wb") as f:
#         f.write(csv_file.getbuffer())
#     st.success("Saved File")

# def joinpath(rootdir, targetdir):
#     return os.path.join(os.sep, rootdir + os.sep, targetdir)

# saveDir = (".", "data")

def save_uploadedfile(uploadedfile):
     with open(os.path.join("saveDir",uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success("Saved File:{} to saveDir".format(uploadedfile.name))

st.sidebar.title("Chat with CSV")
csv_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if csv_file is not None:
   file_details = {"FileName":csv_file.name,"FileType":csv_file.type}
#    df  = pd.read_csv(csv_file)
#    st.dataframe(df)
   save_uploadedfile(csv_file)

st.sidebar.title("References")
st.sidebar.markdown(
    """
    * [Langchain](https://python.langchain.com/en/latest/modules/agents/toolkits/examples/csv.html)
    * [Streamlit chat](https://discuss.streamlit.io/t/new-component-streamlit-chat-a-new-way-to-create-chatbots/20412)
    """
)

if API_KEY:
    #os.environ["OPENAI_API_KEY"] = api_key
    st.title("Chat with CSV")

    if csv_file:
        llm = AzureOpenAI(deployment_name=COMPLETION_MODEL ,openai_api_key= API_KEY , openai_api_version = API_VERSION)
        agent = create_csv_agent(llm, "./saveDir/"+csv_file.name, verbose=False)
        # Initialize the chat history in the session_state if it doesn't exist
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_input = st.text_input("Enter your question:", key="input_field")

        if user_input:
            answer = agent.run(user_input)
            # Add the question and answer to the chat_history
            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("agent", answer))

        # Display the chat_history in a chat-like format using streamlit-chat
        for i, (sender, message_text) in enumerate(st.session_state.chat_history):
            if sender == "user":
                message(message_text, is_user=True, key=f"{i}_user")
            else:
                message(message_text, key=f"{i}")

    else:
        st.write("Upload a csv")
else:
    st.sidebar.error("Error encountered check logs.")
