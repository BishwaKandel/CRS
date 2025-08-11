"""
Simple Pipeline Runner - Run Intent and Entity Processing
Works with basic pattern matching for entities and trained intent classifier
"""

import os
import sys
import re
from typing import Dict, List, Tuple

# Add path for intent module
sys.path.append(os.path.join(os.path.dirname(__file__), 'intent'))

class SimpleEntityExtractor:
    """Simple entity extraction using pattern matching"""
    
    def __init__(self):
        self.patterns = {
            "COURSE": [
                r"computer\s+engineering", r"civil\s+engineering", 
                r"mechanical\s+engineering", r"electrical\s+engineering",
                r"electronics\s+engineering", r"computer", r"civil", 
                r"mechanical", r"electrical", r"electronics"
            ],
            "COLLEGE": [
                r"sagarmatha\s+engineering\s+college", r"sagarmatha", 
                r"sec", r"college"
            ],
            "LOCATION": [
                r"sanepa", r"lalitpur", r"kathmandu", r"nepal"
            ],
            "FACILITY": [
                r"hostel", r"library", r"laboratory", r"lab", 
                r"canteen", r"playground", r"auditorium"
            ],
            "DEPARTMENT": [
                r"department\s+of\s+computer", r"department\s+of\s+civil",
                r"department\s+of\s+mechanical", r"department\s+of\s+electrical"
            ]
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities using regex patterns"""
        entities = {}
        text_lower = text.lower()
        
        for entity_type, patterns in self.patterns.items():
            found = []
            for pattern in patterns:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    if match not in found:
                        found.append(match.title())
            
            if found:
                entities[entity_type] = found
        
        return entities

class SimplePipeline:
    """Simple pipeline combining intent and entity extraction"""
    
    def __init__(self):
        print("🤖 Initializing Simple Chatbot Pipeline...")
        print("=" * 50)
        
        # Initialize entity extractor
        self.entity_extractor = SimpleEntityExtractor()
        print("✅ Entity extractor initialized")
        
        # Try to initialize intent predictor
        try:
            from predict_intent import IntentPredictor
            # Use correct paths for model files
            model_path = os.path.join('intent', 'best_intent_classifier_model.pkl')
            vectorizer_path = os.path.join('intent', 'best_intent_classifier_vectorizer.pkl')
            labels_path = os.path.join('intent', 'label_classes.json')
            
            self.intent_predictor = IntentPredictor(model_path, vectorizer_path, labels_path)
            self.intent_available = True
            print("✅ Intent predictor loaded")
        except Exception as e:
            print(f"⚠️ Intent predictor not available: {e}")
            self.intent_available = False
        
        print("🚀 Pipeline ready!")
    
    def process_query(self, text: str) -> Dict:
        """Process a query through the pipeline"""
        result = {
            "original_text": text,
            "entities": {},
            "intent": None,
            "confidence": 0.0,
            "response": ""
        }
        
        # Extract entities
        entities = self.entity_extractor.extract_entities(text)
        result["entities"] = entities
        
        # Predict intent if available
        if self.intent_available:
            try:
                intent, confidence, top_predictions = self.intent_predictor.predict_intent(text)
                result["intent"] = intent
                result["confidence"] = confidence
                result["top_predictions"] = top_predictions
            except Exception as e:
                print(f"❌ Intent prediction failed: {e}")
        
        # Generate simple response
        result["response"] = self.generate_response(result["intent"], entities, text)
        
        return result
    
    def generate_response(self, intent: str, entities: Dict, text: str) -> str:
        """Generate a simple response based on intent and entities"""
        if not intent:
            # Generate response based on entities when intent is not available
            if entities:
                if "COURSE" in entities:
                    courses = entities["COURSE"]
                    return f"I see you're asking about {', '.join(courses)}. SEC offers various engineering programs including Computer, Civil, Mechanical, Electrical, and Electronics Engineering."
                elif "COLLEGE" in entities:
                    return "Sagarmatha Engineering College (SEC) is a private engineering college located in Sanepa, Lalitpur, Nepal."
                elif "FACILITY" in entities:
                    facilities = entities["FACILITY"]
                    if "hostel" in [f.lower() for f in facilities]:
                        return "Yes, SEC provides hostel facilities for students with basic amenities."
                    elif "lab" in [f.lower() for f in facilities]:
                        return "SEC has well-equipped laboratories for all engineering programs."
                    else:
                        return f"You're asking about {', '.join(facilities)}. SEC has various facilities to support student learning."
                elif "LOCATION" in entities:
                    return "SEC is located in Sanepa, Lalitpur, Nepal. It's easily accessible from major parts of Kathmandu valley."
            
            # Analyze text for keywords when entities aren't detected
            text_lower = text.lower()
            if any(word in text_lower for word in ["course", "program", "study", "offer"]):
                return "SEC offers engineering programs in Computer, Civil, Mechanical, Electrical, and Electronics Engineering."
            elif any(word in text_lower for word in ["location", "where", "address"]):
                return "Sagarmatha Engineering College is located in Sanepa, Lalitpur, Nepal."
            elif any(word in text_lower for word in ["fee", "cost", "price", "tuition"]):
                return "Course fees vary by program. Please contact our admission office at 015427274 for detailed fee structure."
            elif any(word in text_lower for word in ["admission", "apply", "join", "enroll"]):
                return "Admission is based on IOE entrance examination results. Contact our admission office for the detailed process."
            elif any(word in text_lower for word in ["hostel", "accommodation"]):
                return "Yes, hostel facilities are available for students at SEC."
            elif any(word in text_lower for word in ["scholarship", "financial aid"]):
                return "Merit-based and need-based scholarships are available for eligible students."
            
            return "I understand you're asking about Sagarmatha Engineering College. How can I help you?"

        responses = {
            "College_basic_info": "Sagarmatha Engineering College is a private engineering college located in Sanepa, Lalitpur.",
            "Course_list": "We offer Computer Engineering, Civil Engineering, Mechanical Engineering, Electrical Engineering, and Electronics Engineering.",
            "College_location": "SEC is located in Sanepa, Lalitpur, Nepal.",
            "Admission_process": "Admission is based on IOE entrance examination results. Contact our admission office for detailed process.",
            "Course_fee": "Course fees vary by program. Please contact the admission office for detailed fee structure.",
            "Faculty_info": "Our college has experienced faculty members across all engineering departments.",
            "Hostel_availability": "Yes, hostel facilities are available for students.",
            "Course_seats": "Total seats vary by program. Please check with admission office for current availability.",
            "Scholarship_info": "Merit-based and need-based scholarships are available for eligible students.",
            "Placement_info": "We have a dedicated placement cell with good placement records.",
        }
        
        base_response = responses.get(intent, "Thank you for your question about Sagarmatha Engineering College.")
        
        # Add entity-specific information
        if entities:
            entity_info = []
            for entity_type, entity_list in entities.items():
                entity_info.append(f"{entity_type}: {', '.join(entity_list)}")
            if entity_info:
                base_response += f"\n\nDetected topics: {'; '.join(entity_info)}"
        
        return base_response
    
    def demo(self):
        """Run demonstration with sample queries"""
        print("\n🧪 PIPELINE DEMONSTRATION")
        print("=" * 50)
        
        sample_queries = [
            "Tell me about Sagarmatha Engineering College",
            "What courses do you offer?",
            "Where is SEC located?",
            "How much does Computer Engineering cost?",
            "Do you have hostel facilities?",
            "What is the admission process?",
            "Tell me about Civil Engineering department",
            "Are scholarships available?",
        ]
        
        for i, query in enumerate(sample_queries, 1):
            print(f"\n📝 Query {i}: {query}")
            print("-" * 40)
            
            result = self.process_query(query)
            
            print(f"🎯 Intent: {result['intent']} (Confidence: {result['confidence']:.3f})")
            print(f"🏷️ Entities: {result['entities'] if result['entities'] else 'None detected'}")
            print(f"🤖 Response: {result['response']}")
            
            if result.get('top_predictions'):
                print(f"📊 Top Predictions:")
                for intent, conf in result['top_predictions'][:3]:
                    print(f"   - {intent}: {conf:.3f}")
            
            print("\n" + "="*50)
    
    def interactive_chat(self):
        """Interactive chat mode"""
        print("\n💬 INTERACTIVE CHAT MODE")
        print("Type 'quit', 'exit', or 'bye' to stop")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye', '']:
                    print("👋 Goodbye! Thank you for using Sagarmatha Engineering College Chatbot!")
                    break
                
                result = self.process_query(user_input)
                
                # Show analysis first
                print(f"\n📋 Analysis:")
                print(f"🎯 Intent: {result['intent'] if result['intent'] else 'Not detected'} (Confidence: {result['confidence']:.3f})")
                print(f"🏷️ Entities: {result['entities'] if result['entities'] else 'None detected'}")
                
                # Show response
                print(f"\n🤖 Chatbot: {result['response']}")
                
                # Show top predictions if available
                if result.get('top_predictions'):
                    print(f"\n📊 Top Intent Predictions:")
                    for intent, conf in result['top_predictions'][:3]:
                        print(f"   - {intent}: {conf:.3f}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    """Main function"""
    try:
        pipeline = SimplePipeline()
        
        # Run demo
        pipeline.demo()
        
        # Start interactive chat
        pipeline.interactive_chat()
        
    except Exception as e:
        print(f"❌ Failed to start pipeline: {e}")

if __name__ == "__main__":
    main()
