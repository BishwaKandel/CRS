"""
Chatbot Pipeline - Sagarmatha Engineering College
Integrates trained Intent Classifier and NER models for complete conversation handling
"""

import os
import sys
import json
import joblib
import spacy
from typing import Dict, List, Tuple, Any, Optional

# Add current directory to path for importing local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from intent.predict_intent import IntentPredictor


class NERExtractor:
    """Named Entity Recognition using trained spaCy model"""
    
    def __init__(self, model_path='ner'):
        """Load the trained NER model"""
        try:
            self.nlp = spacy.load(model_path)
            print(f"✅ NER model loaded from {model_path}")
        except Exception as e:
            print(f"❌ Error loading NER model: {e}")
            raise
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from text using trained NER model"""
        doc = self.nlp(text)
        entities = {}
        
        for ent in doc.ents:
            entity_type = ent.label_
            entity_text = ent.text
            
            if entity_type not in entities:
                entities[entity_type] = []
            entities[entity_type].append(entity_text)
        
        return entities


class IntentHandler:
    """Handles different intents and generates appropriate responses"""
    
    def __init__(self):
        """Initialize intent response mappings"""
        self.response_templates = {
            "Admission_process": {
                "base": "Here's information about our admission process:",
                "details": [
                    "• Online application through our portal",
                    "• Submit required documents (10+2 certificates, etc.)",
                    "• Merit-based selection",
                    "• Interview for some programs",
                    "• Final admission after fee payment"
                ]
            },
            "College_basic_info": {
                "base": "Sagarmatha Engineering College Information:",
                "details": [
                    "• Established engineering college in Nepal",
                    "• Offers undergraduate and graduate programs",
                    "• Affiliated with Pokhara University",
                    "• Focus on practical and theoretical education",
                    "• Modern facilities and experienced faculty"
                ]
            },
            "College_contact": {
                "base": "Contact Information:",
                "details": [
                    "• Phone: +977-1-XXXXXXX",
                    "• Email: info@sec.edu.np",
                    "• Website: www.sec.edu.np",
                    "• Office Hours: 9 AM - 5 PM (Sun-Fri)"
                ]
            },
            "College_location": {
                "base": "College Location:",
                "details": [
                    "• Located in Kathmandu, Nepal",
                    "• Easily accessible by public transport",
                    "• Modern campus with all facilities",
                    "• Safe and conducive learning environment"
                ]
            },
            "Course_list": {
                "base": "Available Courses:",
                "details": [
                    "• Computer Engineering",
                    "• Civil Engineering", 
                    "• Electronics & Communication Engineering",
                    "• Electrical Engineering",
                    "• Mechanical Engineering"
                ]
            },
            "Course_fee": {
                "base": "Fee Structure Information:",
                "details": [
                    "• Fees vary by program",
                    "• Scholarship opportunities available",
                    "• Installment payment options",
                    "• Contact admission office for detailed fee structure"
                ]
            },
            "Hostel_availability": {
                "base": "Hostel Accommodation:",
                "details": [
                    "• On-campus hostel facilities available",
                    "• Separate hostels for boys and girls",
                    "• Furnished rooms with basic amenities",
                    "• Mess facilities available",
                    "• Limited seats - early application recommended"
                ]
            },
            "Scholarship_info": {
                "base": "Scholarship Information:",
                "details": [
                    "• Merit-based scholarships",
                    "• Need-based financial aid",
                    "• Government scholarships available",
                    "• Sports and cultural scholarships",
                    "• Contact admission office for application process"
                ]
            },
            "Placement_info": {
                "base": "Placement & Career Support:",
                "details": [
                    "• Dedicated placement cell",
                    "• Industry partnerships",
                    "• Career counseling and guidance",
                    "• Internship opportunities",
                    "• Regular job fairs and campus recruitment"
                ]
            }
        }
    
    def handle_intent(self, intent: str, entities: Dict[str, List[str]], 
                     original_text: str, confidence: float) -> str:
        """Generate response based on intent and entities"""
        
        # Get base response for the intent
        if intent in self.response_templates:
            response_data = self.response_templates[intent]
            response = f"{response_data['base']}\n"
            
            # Add detailed information
            for detail in response_data['details']:
                response += f"{detail}\n"
            
            # Add entity-specific information if available
            if entities:
                response += f"\n📝 I noticed you mentioned:\n"
                for entity_type, entity_values in entities.items():
                    for value in entity_values:
                        response += f"• {entity_type}: {value}\n"
        else:
            # Generic response for unknown intents
            response = f"I understand you're asking about '{intent}'. "
            response += "Let me help you with general information. "
            response += "Could you please be more specific about what you'd like to know?"
        
        # Add confidence information
        if confidence < 0.7:
            response += f"\n⚠️ I'm not entirely sure about this query (confidence: {confidence:.2f}). "
            response += "Could you please rephrase or provide more details?"
        
        return response
    
    def get_fallback_response(self, original_text: str) -> str:
        """Generate fallback response when intent confidence is very low"""
        return (
            "I'm not sure I understand your question completely. "
            "Here are some topics I can help you with:\n\n"
            "• Admission process and requirements\n"
            "• Course information and fees\n"
            "• College location and contact details\n"
            "• Hostel and accommodation\n"
            "• Scholarships and financial aid\n"
            "• Placement and career opportunities\n\n"
            "Please feel free to ask about any of these topics!"
        )


class ChatbotPipeline:
    """Main chatbot pipeline that orchestrates all components"""
    
    def __init__(self, intent_model_dir='intent', ner_model_dir='ner'):
        """Initialize the complete chatbot pipeline"""
        print("🤖 Initializing Chatbot Pipeline...")
        print("=" * 50)
        
        # Initialize components
        try:
            # Change to intent directory for loading models
            original_dir = os.getcwd()
            intent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), intent_model_dir)
            os.chdir(intent_dir)
            
            self.intent_predictor = IntentPredictor()
            
            # Change back to original directory
            os.chdir(original_dir)
            
            # Initialize NER extractor
            ner_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ner_model_dir)
            self.ner_extractor = NERExtractor(ner_path)
            
            # Initialize intent handler
            self.intent_handler = IntentHandler()
            
            print("✅ All components initialized successfully!")
            
        except Exception as e:
            print(f"❌ Error initializing pipeline: {e}")
            raise
    
    def process_message(self, user_input: str) -> Dict[str, Any]:
        """Process user message through the complete pipeline"""
        try:
            # Step 1: Predict Intent
            predicted_intent, confidence, top_predictions = self.intent_predictor.predict_intent(user_input)
            
            # Step 2: Extract Entities
            entities = self.ner_extractor.extract_entities(user_input)
            
            # Step 3: Generate Response
            if confidence >= 0.3:  # Minimum confidence threshold
                response = self.intent_handler.handle_intent(
                    predicted_intent, entities, user_input, confidence
                )
            else:
                response = self.intent_handler.get_fallback_response(user_input)
            
            # Return complete pipeline result
            return {
                "user_input": user_input,
                "predicted_intent": predicted_intent,
                "confidence": confidence,
                "top_predictions": top_predictions,
                "entities": entities,
                "response": response,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "user_input": user_input,
                "error": str(e),
                "response": "Sorry, I encountered an error processing your request. Please try again.",
                "status": "error"
            }
    
    def chat_interactive(self):
        """Interactive chat mode"""
        print("\n🎯 SAGARMATHA ENGINEERING COLLEGE CHATBOT")
        print("=" * 50)
        print("Hello! I'm here to help you with information about our college.")
        print("Ask me about admissions, courses, fees, location, hostels, and more!")
        print("Type 'quit', 'exit', or 'bye' to end the conversation.")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("🤖 Bot: Thank you for your interest in Sagarmatha Engineering College! Goodbye! 👋")
                    break
                
                if not user_input:
                    print("🤖 Bot: Please ask me something about the college!")
                    continue
                
                # Process the message
                result = self.process_message(user_input)
                
                # Display results
                if result["status"] == "success":
                    print(f"\n🤖 Bot: {result['response']}")
                    
                    # Show debug information (optional)
                    print(f"\n🔍 Debug Info:")
                    print(f"   Intent: {result['predicted_intent']} (confidence: {result['confidence']:.3f})")
                    if result['entities']:
                        print(f"   Entities: {result['entities']}")
                    else:
                        print(f"   Entities: None detected")
                else:
                    print(f"\n🤖 Bot: {result['response']}")
                
            except KeyboardInterrupt:
                print("\n🤖 Bot: Thank you for visiting! Goodbye! 👋")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    def demo_pipeline(self):
        """Demonstrate the pipeline with sample queries"""
        print("\n🧪 PIPELINE DEMONSTRATION")
        print("=" * 30)
        
        sample_queries = [
            "What courses do you offer?",
            "How much does Computer Engineering cost?",
            "Where is Sagarmatha Engineering College located?",
            "Do you have hostel facilities?",
            "Tell me about the admission process",
            "What scholarships are available?",
            "Can you tell me about placement opportunities?",
            "I want to know about Civil Engineering course",
            "How can I contact the college?",
        ]
        
        for i, query in enumerate(sample_queries, 1):
            print(f"\n📝 Query {i}: {query}")
            print("-" * 40)
            
            result = self.process_message(query)
            
            if result["status"] == "success":
                print(f"🎯 Intent: {result['predicted_intent']} ({result['confidence']:.3f})")
                print(f"🏷️ Entities: {result['entities'] if result['entities'] else 'None'}")
                print(f"🤖 Response:\n{result['response']}")
            else:
                print(f"❌ Error: {result['error']}")
            
            print("\n" + "="*50)


def main():
    """Main function to run the chatbot pipeline"""
    try:
        # Initialize the pipeline
        chatbot = ChatbotPipeline()
        
        # Show demo first
        chatbot.demo_pipeline()
        
        # Start interactive chat
        chatbot.chat_interactive()
        
    except Exception as e:
        print(f"❌ Failed to start chatbot: {e}")
        print("\nPlease ensure:")
        print("1. Intent model files are in the 'intent/' directory")
        print("2. NER model is in the 'ner/' directory")
        print("3. All required dependencies are installed")


if __name__ == "__main__":
    main()
