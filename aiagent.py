import openai
import streamlit

openai.api_key = streamlit.secrets['OPENAI_API_KEY']
    
class AIAgent():
    def __init__(self, model="gpt-3.5-turbo"):
        """Initialize the AI Agent.  Set the system message, initial prompt prefix, and initial response"""
        self.model=model
        self.system_message = """For each query, consider writings of the writers Neville Goddard, 
        Peter A. Levine, Bessel A van der Kolk, Siddartha, Sadhguru Jaggi Vasudev, and Robert E. Grant that have addressed that question.
        Finally, combine referenced sources to form a response.  
        For example:
        Query: What is the meaning of life?
        Response: Life is meaningless from an objective viewpoint, but that we can create our own meaning for our lives. 
        Ultimately, life is what you make of it and it means what it means to you."""
        self.prefix = ''
        self.history = [{'role': 'system', 'content':self.system_message}]
        self.response = ''
        
    def add_message(self, text, role):
        """Add a message to the conversation history"""
        message = {'role':role, 'content':text}
        self.history.append(message)
        
    def query(self, prompt, temperature=.1):
        # Add user prompt to history
        self.add_message(self.prefix + prompt, 'user')

        # Query the model through the API 
        result = openai.ChatCompletion.create(
            model=self.model,
            messages=self.history,
            temperature=temperature, # this is the degree of randomness of the model's output
        )

        self.response = result.choices[0].message["content"]
        # Add reply to message history
        self.add_message(self.response, 'assistant')
        
        # set prompt prefix to ensure same philosopher answers each time.
        self.prefix = 'Please continue to respond as the previous philosopher: '
           
    def clear_history(self):
        """Reset the history to its initial state.  Also reset the prefix and current response"""
        self.history = [{'role':'system', 'content':self.system_message}]
        self.prefix = ''
        self.response = ''