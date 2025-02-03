import json

class MedicalChatbot:
    def __init__(self):
        self.patient_info = {}
        self.conversation_state = 'start'
        self.questions = [
            'What is your name?',
            'What is your age?',
            'Do you have any existing medical conditions?',
            'Are you currently taking any medications?',
            'What symptoms are you experiencing?'
        ]
        self.current_question_index = 0

    def process_message(self, user_message):
        # Simple state machine for gathering patient information
        if self.conversation_state == 'start':
            return self.questions[0]
        
        # Store patient information based on current state
        if self.current_question_index < len(self.questions):
            self.patient_info[self.questions[self.current_question_index]] = user_message
            self.current_question_index += 1
            
            # If more questions, return next question
            if self.current_question_index < len(self.questions):
                return self.questions[self.current_question_index]
            
            # If all questions answered, process and summarize
            return self.generate_summary()
        
        return "Thank you for completing the medical intake."

    def generate_summary(self):
        summary = "Patient Information Summary:\n"
        for question, answer in self.patient_info.items():
            summary += f"{question} {answer}\n"
        return summary