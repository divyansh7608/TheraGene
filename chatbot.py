import openai
openai.api_key="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"

def chat_with_gpt(prompt):
    response= openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role":"user","content": prompt}]
    )

    return response.choices[0].message.content.strip()

if __name__=="__main__":
    while True:
        user_input=input("You: ")
        if user_input.lower() in ["quit","exit","bye"]:
            break

        response=chat_with_gpt(user_input)
        print("Chatbot: ", response) 