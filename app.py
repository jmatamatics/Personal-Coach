import streamlit as st
from aiagent import AIAgent

from streamlit.web.server.websocket_headers import _get_websocket_headers

# Get session id
headers = _get_websocket_headers()
session_id = headers.get("Sec-Websocket-Key")

@st.cache_resource
def get_agent(session_id):
    # Instantiate AIAgent if no cached agent is found.  
    # This happens exactly one time each time a new session is started
    agent = AIAgent(model='gpt-3.5-turbo')
    print('creating the ai agent')
    agent.reponse = 'We wont tell what to see. Only where to look.'
    return agent

def format_history(history):
    # Make the history more readable
    report = ''
    for message in history[1:]:
        if message['role'] == 'user':
            report += (f"\n\nYOU: {message['content'].replace(agent.prefix, '')}")
        else:
            report += (f"\n\nPHILOSOPHER: {message['content']}")
    return report
 
def query_agent():
    # Sent user query to agent
    if prompt:
        try:      
            current_response.write("All Is Wtihin is considering your query and will send a representative soon.")
            agent.query(prompt, 
                        temperature=temperature
                                )
        except Exception as e:
            agent.response = "I'm sorry, all philosophers are busy helping other wisdom seekers.  Please try again later."
            print(e)
    else:
        print('no prompt')

# Page Header
st.title('Chat with your Personal Coach')

# User prompt input
prompt = st.text_input(label="Ask a question and our Spiritual AI will respond",
                       max_chars=1000,
                       value='',
                       help="Repsonses will source the material the resopnse was based on.",
                       key='user_query',
                       placeholder="Enter your burning question here")

# Instantiate agent (only if it has not been created yet, otherwise use cached agent)
agent = get_agent(session_id)

# Submit user input to query agent.
st.button('Submit your question to All Is Within',
          on_click=query_agent
          )

# Slider bar to adjust temperature on the sidebar
temperature = st.sidebar.slider('Creativity', min_value=0.0, max_value=1.0, step=0.1, value=0.1)

# button to clear the message history and start a new conversation on the sidebar
st.sidebar.button('New conversation', on_click=agent.clear_history,
                   use_container_width=False)

# display the conversation so far on the sidebar
st.sidebar.markdown(f'The conversation so far: {format_history(agent.history)}')

# Display most recent response
current_response = st.markdown(agent.response)
