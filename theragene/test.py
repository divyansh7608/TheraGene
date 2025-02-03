import os
from azure.core.credentials import AzureKeyCredential 
from azure.ai.language.questionanswering import QuestionAnsweringClient
from dotenv import load_dotenv

# Get Configuration Settings
load_dotenv()
ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
ai_key = os.getenv('AI_SERVICE_KEY')

#Create client using endpoint and key 
credential = AzureKeyCredential(ai_key) 
ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)

#Submit a question and display the answer 
user_question = '' 
try:
    while user_question.lower() != 'quit': 
            user_question = input('\nQuestion:\n') 
            response = ai_client.get_answers_from_text(
            question=user_question,
            ) 
            for candidate in response.answers:
                print(f"Answer: {candidate.answer}")
                print(f"Confidence: {candidate.confidence}")

except Exception as e:
    print(f"Error: {e}")
