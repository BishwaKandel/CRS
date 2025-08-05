"""
Simplified Chatbot Pipeline - Works without spaCy dependency for testing
Uses mock NER function and your existing trained intent classifier
"""

import os
import sys
import json
from typing import Dict, List, Tuple, Any, Optional

# Add current directory to path for importing local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from intent.predict_intent import IntentPredictor


class MockNERExtractor:
    """Mock Named Entity Recognition for testing without spaCy"""
    
    def __init__(self):
        """Initialize mock NER with predefined patterns"""
        self.entity_patterns = {
            "Course": [
                "computer engineering", "civil engineering", "mechanical engineering",
                "electrical engineering", "electronics communication", "electronics",
                "computer", "civil", "mechanical", "electrical", "ece", "cse"
            ],
            "College": [
                "sagarmatha engineering college", "sagarmatha", "sec", "college"
            ],
            "Department": [
                "computer department", "civil department", "mechanical department",
                "electrical department", "electronics department"
            ],
            "Facility": [
                "hostel", "library", "laboratory", "canteen", "playground",
                "auditorium", "computer lab", "workshop"
            ]
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities using pattern matching"""
        entities = {}
        text_lower = text.lower()
        
        for entity_type, patterns in self.entity_patterns.items():
            found_entities = []
            for pattern in patterns:
                if pattern in text_lower:
                    # Capitalize properly for display
                    formatted_entity = pattern.title()
                    if formatted_entity not in found_entities:
                        found_entities.append(formatted_entity)
            
            if found_entities:
                entities[entity_type] = found_entities
        
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
                    "• Merit-based selection process",
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
                    "• Computer Engineering (4 years)",
                    "• Civil Engineering (4 years)", 
                    "• Electronics & Communication Engineering (4 years)",
                    "• Electrical Engineering (4 years)",
                    "• Mechanical Engineering (4 years)"
                ]
            },
            "Course_specific_info": {
                "base": "Course-Specific Information:",
                "details": [
                    "• Curriculum designed with industry requirements",
                    "• Practical lab sessions and projects",
                    "• Industrial visits and internships",
                    "• Expert faculty from industry and academia",
                    "• Modern equipment and software"
                ]
            },
            "Course_fee": {
                "base": "Fee Structure Information:",
                "details": [
                    "• Fees vary by program (approx. NPR 2-4 lakhs per year)",
                    "• Scholarship opportunities available",
                    "• Installment payment options",
                    "• Contact admission office for detailed fee structure",
                    "• Additional fees for lab and library"
                ]
            },
            "Hostel_availability": {
                "base": "Hostel Accommodation:",
                "details": [
                    "• On-campus hostel facilities available",
                    "• Separate hostels for boys and girls",
                    "• Furnished rooms with basic amenities",
                    "• Mess facilities with nutritious meals",
                    "• Limited seats - early application recommended"
                ]
            },
            "Scholarship_info": {
                "base": "Scholarship Information:",
                "details": [
                    "• Merit-based scholarships (up to 100% tuition)",
                    "• Need-based financial aid",
                    "• Government scholarships for eligible students",
                    "• Sports and cultural achievement scholarships",
                    "• Contact admission office for application process"
                ]
            },
            "Placement_info": {
                "base": "Placement & Career Support:",
                "details": [
                    "• Dedicated placement cell with industry connections",
                    "• 80%+ placement rate for eligible students",
                    "• Career counseling and soft skills training",
                    "• Internship opportunities with top companies",
                    "• Regular job fairs and campus recruitment drives"
                ]
            },
            "Eligibility_criteria": {
                "base": "Eligibility Criteria:",
                "details": [
                    "• 10+2 or equivalent with Physics, Chemistry, Math",
                    "• Minimum aggregate of 50% in 10+2",
                    "• Valid IOE entrance exam score",
                    "• Age limit: Maximum 25 years",
                    "• English proficiency required"
                ]
            },
            "Faculty_info": {
                "base": "Faculty Information:",
                "details": [
                    "• Highly qualified faculty with PhD and Masters",
                    "• Industry experience and academic expertise",
                    "• Regular training and development programs",
                    "• Research-oriented teaching approach",
                    "• Student-friendly and supportive environment"
                ]
            }
        }
    
    def handle_intent(self, intent: str, entities: Dict[str, List[str]], 
                     original_text: str, confidence: float) -> str:
        """Generate response based on intent and entities"""
        
        response = ""
        
        # Get base response for the intent
        if intent in self.response_templates:
            response_data = self.response_templates[intent]
            response = f"{response_data['base']}\n\n"
            
            # Add detailed information
            for detail in response_data['details']:
                response += f"{detail}\n"
            
            # Add entity-specific customization
            if entities:
                response += f"\n📝 Based on your query, I noticed you mentioned:\n"
                for entity_type, entity_values in entities.items():
                    for value in entity_values:
                        response += f"• {entity_type}: {value}\n"
                
                # Add specific information for detected entities
                if "Course" in entities:
                    response += f"\n💡 For specific course information, feel free to ask about:\n"
                    response += f"• Course curriculum and subjects\n"
                    response += f"• Career opportunities\n"
                    response += f"• Faculty and facilities\n"
        else:
            # Generic response for unknown intents
            response = f"I understand you're asking about '{intent}'. "
            response += "Let me provide you with general information.\n\n"
            response += "I can help you with information about:\n"
            response += "• Admissions and eligibility\n"
            response += "• Courses and fees\n"
            response += "• College facilities and location\n"
            response += "• Scholarships and placements\n\n"
            response += "Please feel free to ask more specific questions!"
        
        # Add confidence notice if needed
        if confidence < 0.7:
            response += f"\n\n⚠️ Note: I'm not entirely certain about this query (confidence: {confidence:.2f}). "
            response += "If this doesn't answer your question, please try rephrasing it."
        
        return response
    
    def get_fallback_response(self, original_text: str) -> str:
        """Generate fallback response when intent confidence is very low"""
        return (
            "I'm not sure I understand your question completely. Let me help you! 🤔\n\n"
            "Here are some topics I can assist you with:\n\n"
            "📚 **Academic Information:**\n"
            "• Available courses and programs\n"
            "• Admission process and eligibility\n"
            "• Course fees and duration\n\n"
            "🏫 **College Information:**\n"
            "• Campus location and facilities\n"
            "• Contact details and office hours\n"
            "• Hostel and accommodation\n\n"
            "💰 **Financial & Support:**\n"
            "• Scholarships and financial aid\n"
            "• Placement assistance and career support\n\n"
            "Please ask me about any of these topics, and I'll be happy to help! 😊"
        )


class SimpleChatbotPipeline:
    """Simplified chatbot pipeline using existing intent classifier and mock NER"""
    
    def __init__(self, intent_model_dir='intent'):
        """Initialize the chatbot pipeline"""
        print("🤖 Initializing Sagarmatha Engineering College Chatbot...")
        print("=" * 55)
        
        try:
            # Initialize intent predictor
            original_dir = os.getcwd()
            intent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), intent_model_dir)
            os.chdir(intent_dir)
            
            self.intent_predictor = IntentPredictor()
            
            # Change back to original directory
            os.chdir(original_dir)
            
            # Initialize mock NER extractor
            self.ner_extractor = MockNERExtractor()
            
            # Initialize intent handler
            self.intent_handler = IntentHandler()
            
            print("✅ All components initialized successfully!")
            print("📝 Using mock NER for entity extraction")
            
        except Exception as e:
            print(f"❌ Error initializing pipeline: {e}")
            raise
    
    def process_message(self, user_input: str) -> Dict[str, Any]:
        """Process user message through the complete pipeline"""
        try:
            # Step 1: Predict Intent
            predicted_intent, confidence, top_predictions = self.intent_predictor.predict_intent(user_input)
            
            # Step 2: Extract Entities (using mock NER)
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
        print("\n🎓 SAGARMATHA ENGINEERING COLLEGE CHATBOT")
        print("=" * 55)
        print("Hello! I'm your virtual assistant for Sagarmatha Engineering College! 🤖")
        print("I can help you with information about:")
        print("• Admissions & Courses • Fees & Scholarships • Location & Facilities")
        print("• Hostel & Accommodation • Placements & Career Support")
        print("\nType 'quit', 'exit', or 'bye' to end our conversation.")
        print("=" * 55)
        
        conversation_count = 0
        
        while True:
            try:
                user_input = input(f"\n💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("🤖 Bot: Thank you for your interest in Sagarmatha Engineering College!")
                    print("       Feel free to visit our campus or contact us anytime. Goodbye! 👋")
                    break
                
                if not user_input:
                    print("🤖 Bot: Please ask me something about the college! I'm here to help! 😊")
                    continue
                
                conversation_count += 1
                
                # Process the message
                print("🔄 Processing your query...")
                result = self.process_message(user_input)
                
                # Display response
                if result["status"] == "success":
                    print(f"\n🤖 Bot: {result['response']}")
                    
                    # Show technical details (can be hidden in production)
                    if conversation_count <= 3:  # Show for first few queries
                        print(f"\n{'─' * 40}")
                        print(f"🔍 Technical Details:")
                        print(f"   Detected Intent: {result['predicted_intent']}")
                        print(f"   Confidence Score: {result['confidence']:.3f}")
                        if result['entities']:
                            print(f"   Extracted Entities: {result['entities']}")
                        else:
                            print(f"   Extracted Entities: None")
                        print(f"{'─' * 40}")
                else:
                    print(f"\n🤖 Bot: {result['response']}")
                
            except KeyboardInterrupt:
                print("\n🤖 Bot: Thank you for your time! Have a great day! 👋")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("🤖 Bot: Sorry, something went wrong. Please try asking again!")
    
    def demo_pipeline(self):
        """Demonstrate the pipeline with sample queries"""
        print("\n🧪 PIPELINE DEMONSTRATION")
        print("=" * 35)
        print("Let me show you how the chatbot works with some sample queries:\n")
        
        sample_queries = [
            "What courses does Sagarmatha Engineering College offer?",
            "How much does Computer Engineering cost?",
            "Where is the college located?",
            "Do you have hostel facilities available?",
            "Tell me about the admission process for Civil Engineering",
            "What scholarships are available for students?",
            "Can you provide information about placement opportunities?",
            "What are the eligibility criteria for admission?",
            "Tell me about the faculty at SEC"
        ]
        
        for i, query in enumerate(sample_queries, 1):
            print(f"📝 Sample Query {i}: {query}")
            print("─" * 50)
            
            result = self.process_message(query)
            
            if result["status"] == "success":
                print(f"🎯 Detected Intent: {result['predicted_intent']}")
                print(f"📊 Confidence: {result['confidence']:.3f}")
                print(f"🏷️ Entities: {result['entities'] if result['entities'] else 'None detected'}")
                print(f"\n🤖 Response:\n{result['response'][:200]}...")
                if len(result['response']) > 200:
                    print("   (Response truncated for demo)")
            else:
                print(f"❌ Error: {result['error']}")
            
            print("\n" + "="*60 + "\n")
        
        print("Demo completed! 🎉")


def main():
    """Main function to run the chatbot pipeline"""
    try:
        # Initialize the simplified pipeline
        chatbot = SimpleChatbotPipeline()
        
        # Ask user what they want to do
        print("\nWhat would you like to do?")
        print("1. See demo with sample queries")
        print("2. Start interactive chat")
        print("3. Both (demo first, then chat)")
        
        choice = input("\nEnter your choice (1/2/3): ").strip()
        
        if choice == "1":
            chatbot.demo_pipeline()
        elif choice == "2":
            chatbot.chat_interactive()
        elif choice == "3":
            chatbot.demo_pipeline()
            input("\nPress Enter to start interactive chat...")
            chatbot.chat_interactive()
        else:
            print("Starting interactive chat by default...")
            chatbot.chat_interactive()
        
    except Exception as e:
        print(f"❌ Failed to start chatbot: {e}")
        print("\nPlease ensure:")
        print("1. Intent model files are in the 'intent/' directory")
        print("2. All required files are present:")
        print("   - best_intent_classifier_model.pkl")
        print("   - best_intent_classifier_vectorizer.pkl")
        print("   - label_classes.json")


if __name__ == "__main__":
    main()
