import streamlit as st
import os
import requests

server_url = os.environ["project_1_url"]

# App information and setup
project_title = "Test Project 1"
project_desc = """
To create an AI agent that can take a question input from the user, then searches Google
and pulls web page content, summarises, and returns a coherent and comprehensive
answer, with references provided where appropriate.
This should be built into a simple webapp (with a login function if possible), and you should
also create an API for the service (perhaps using FastAPI) where the input can be passed
and it returns the answer, references etc
"""
st.set_page_config(page_title=project_title)

def search_then_gpt(message, openai_key):
    try:
        response = requests.post(f'{server_url}/web-summary', 
                                    data={'message': message,
                                          'openai_key': openai_key},
                                    timeout=600)
    except requests.exceptions.SSLError as e:
        st.error(f"SSL Error: {e}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

    if response.status_code == 200:
        json_data = response.json()
        if "response" in json_data:
            st.markdown(json_data['response'])
        elif "error" in json_data:
            st.error(f"Server error: {json_data['error']}")
    else:
        st.error('Request failed')

def main():
    st.title(project_title)
    st.write(project_desc)

    try:
        response = requests.get(f'{server_url}/ping')
        if response.status_code == 200:
            if response.content:
                json_data = response.json()
                if json_data['text'] == "pong":
                    st.success("• Connected to the server.")
                else:
                    st.warning(f"• Server is running but returned unexpected response.")
            else:
                st.warning(f"• Server returned an empty response.")
        else:
            st.warning(f"• Server returned a {response.status_code} status code.")

    except requests.exceptions.ConnectionError:
        st.error("• Could not connect to the server.")

#########################################
    openai_key = st.text_input('OpenAI API key')

    with st.form('input_form'):
        message = st.text_area("What do you want to search?", "How to make lemonade?")
        submit = st.form_submit_button("Send!")
        # if not openai_key.startswith('sk-'):
        #     st.warning('Please enter your OpenAI API key!')
        # elif openai_key.startswith('sk-') and submit:
        if submit:
            with st.spinner("Fetching search results.."):
                search_then_gpt(message, openai_key)

if __name__ == "__main__":
    main()