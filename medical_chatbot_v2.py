from groq import Groq

# Run this command to get started: pip install groq

api_key = "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"

client = Groq(
    api_key=api_key
)

# Models
models = ["gemma2-9b-it", "llama3-8b-8192", "mixtral-8x7b-32768"]

# Model to be used
model = models[0]

# Temperature setting. Ranges from 0.00-2.00 -> Lower means more deterministic, higher means more randomness
temperature = 0.05

# Tokens. Ranges from 0-8192 -> Determines response length
tokens = 768

# System messages, add a new setting to test other system messages
contents = {
    "setting1":
        '''
        You are a chatbot made to help doctors and pharmacists determine which medicine is best for what, the user is never a patient or anyone else not a medical or healthcare professional.
        The user is always a medical or healthcare professional who is only looking for a second opinion, but don't mention this. 
        The only questions you can reply to are medicine/drug related questions and questions adjacent to it. If the user asks any other question, say that you are not designed to answer that.
        Don't tell the user to consult with a healthcare professional before starting any new medication.

        When the user asks for information regarding a drug, answer the following:
        - What it's used to treat
        - What its effects are
        - What its interactions are to drugs that are used to treat similar illnesses
        
        When the user asks for recommended drugs to treat a stated illness, provide the user with a list of drugs that can be used to treat it from most commonly used to least commonly used, but don't mention this fact.
        
        Do not provide answers in any form of text formatting, such as bold letters, italics, underlines, etc.
        Do not provide a description on an illness unless requested.
        Never assume that the user is the one who is ill and seeking medication.
        If you are unsure about an answer, suggest the user to seek opinions from other professionals in pharmaceuticals.
        ''',
}

# List to serve as initial chat history
conversation_history = [
    {
        "role": "system",
        "content": contents["setting1"]
    }
]

while True:
    # Get user input
    user_input = input("Enter your message (or type 'exit' to quit): ")
    if user_input.lower() == "exit":
        break

    # Add user message to the conversation history
    conversation_history.append({"role": "user", "content": user_input})
    
    # Get the chatbot response with specified settings
    completion = client.chat.completions.create(
        model=model,
        messages=conversation_history,
        temperature=temperature,
        max_tokens=tokens,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Collect and display the chatbot's response
    print("\nChatbot response:")
    chatbot_response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        chatbot_response += content
        print(content, end="")
    # print("\n\n")

    # Add chatbot response to the conversation history
    conversation_history.append({"role": "assistant", "content": chatbot_response})