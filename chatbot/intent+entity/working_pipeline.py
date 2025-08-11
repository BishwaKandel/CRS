"""
Working Pipeline - Intent and Entity Processing
This version handles the numpy compatibility issue and shows actual intent predictions
"""

import os
import sys
import re
import json
from typing import Dict, List, Tuple

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

class MockIntentClassifier:
    """Mock intent classifier that simulates the trained model behavior"""
    
    def __init__(self):
        # Define intent patterns based on your training data
        self.intent_patterns = {
            "College_basic_info": [
                r"tell me about", r"what is", r"about.*college", r"information.*college",
                r"college.*profile", r"college.*details", r"sagarmatha.*college"
            ],
            "Course_list": [
                r"what courses", r"courses.*offer", r"programs.*available", 
                r"study.*options", r"subjects.*offer", r"branches.*available"
            ],
            "College_location": [
                r"where.*located", r"location.*college", r"address", 
                r"where.*sec", r"geographical.*location"
            ],
            "Admission_process": [
                r"admission.*process", r"how.*apply", r"how.*join", 
                r"enrollment", r"how.*get.*admission"
            ],
            "Course_fee": [
                r"fee", r"cost", r"price", r"tuition", r"expenses", 
                r"how much.*cost", r"fees.*structure"
            ],
            "Faculty_info": [
                r"faculty", r"teachers", r"professors", r"instructors",
                r"teaching.*staff", r"academic.*staff"
            ],
            "Hostel_availability": [
                r"hostel", r"accommodation", r"stay.*campus", r"living.*facilities",
                r"residential", r"dormitory"
            ],
            "Course_seats": [
                r"seats.*available", r"how many.*seats", r"capacity", 
                r"enrollment.*limit", r"intake.*numbers"
            ],
            "Scholarship_info": [
                r"scholarship", r"financial.*aid", r"merit.*award", 
                r"financial.*assistance", r"financial.*support"
            ],
            "Placement_info": [
                r"placement", r"job.*opportunities", r"career.*prospects", 
                r"employment", r"job.*placement"
            ],
            "Course_specific_info": [
                r"computer.*engineering.*course", r"civil.*engineering.*course",
                r"mechanical.*engineering.*course", r"electrical.*engineering.*course",
                r"tell me about.*engineering"
            ],
            "Department_info": [
                r"departments", r"academic.*divisions", r"faculties",
                r"which.*departments"
            ],
            "Eligibility_criteria": [
                r"eligibility", r"requirements", r"qualifications",
                r"who can apply", r"criteria"
            ],
            "Course_duration": [
                r"duration", r"how long", r"years.*course", r"semesters",
                r"time.*complete"
            ],
            "Course_cutoff": [
                r"cutoff", r"minimum.*marks", r"required.*rank", 
                r"entrance.*marks", r"qualifying.*marks"
            ]
        }
        
        # Load actual label classes if available
        try:
            with open('intent/label_classes.json', 'r') as f:
                self.label_classes = json.load(f)
        except:
            # Fallback label classes
            self.label_classes = list(self.intent_patterns.keys())
    
    def predict_intent(self, text: str) -> Tuple[str, float, List[Tuple[str, float]]]:
        """Predict intent using pattern matching"""
        text_lower = text.lower()
        scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    score += 1
            # Normalize score
            if patterns:
                scores[intent] = score / len(patterns)
        
        if scores:
            # Get the best match
            best_intent = max(scores, key=scores.get)
            confidence = scores[best_intent]
            
            # Get top 3 predictions
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            top_predictions = [(intent, score) for intent, score in sorted_scores[:3]]
            
            return best_intent, confidence, top_predictions
        else:
            return "Unknown", 0.0, [("Unknown", 0.0)]

class WorkingPipeline:
    """Working pipeline that shows both intent and entity processing"""
    
    def __init__(self):
        print("🤖 Initializing Working Chatbot Pipeline...")
        print("=" * 50)
        
        # Initialize entity extractor
        self.entity_extractor = SimpleEntityExtractor()
        print("✅ Entity extractor initialized")
        
        # Initialize mock intent classifier
        self.intent_classifier = MockIntentClassifier()
        print("✅ Intent classifier initialized (mock version)")
        
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
        
        # Predict intent
        intent, confidence, top_predictions = self.intent_classifier.predict_intent(text)
        result["intent"] = intent
        result["confidence"] = confidence
        result["top_predictions"] = top_predictions
        
        # Generate response
        result["response"] = self.generate_response(intent, entities, text)
        
        return result
    
    def generate_response(self, intent: str, entities: Dict, text: str) -> str:
        """Generate response based on intent and entities"""
        responses = {
            "College_basic_info": "Sagarmatha Engineering College (SEC) is a private engineering college located in Sanepa, Lalitpur, Nepal. It's affiliated with Tribhuvan University and offers various engineering programs.",
            "Course_list": "SEC offers the following engineering programs:\n• Computer Engineering\n• Civil Engineering\n• Electronics and Communication Engineering\n• All programs are 4-year Bachelor's degrees.",
            "College_location": "Sagarmatha Engineering College is located in:\n📍 Sanepa, Lalitpur, Nepal\n📞 Contact: 015427274\n📧 Email: info@sagarmatha.edu.np",
            "Admission_process": "Admission Process:\n• Based on IOE (Institute of Engineering) entrance examination\n• Apply through IOE entrance portal\n• Merit-based selection\n• Contact admission office for detailed guidance",
            "Course_fee": "Course fees vary by program:\n• Computer Engineering: ~11,00,000 NPR\n• Civil Engineering: ~13,00,000 NPR\n• Electronics Engineering: ~7,00,000 NPR\n• Scholarship opportunities available for eligible students",
            "Faculty_info": "SEC has experienced and qualified faculty members:\n• PhD and Master's degree holders\n• Industry experience\n• Regular training and development\n• Low faculty-to-student ratio for personalized attention",
            "Hostel_availability": "Hostel Facilities:\n🏠 Currently no on-campus hostel\n🏘️ Nearby accommodation options available\n📞 Contact college for assistance in finding suitable accommodation",
            "Course_seats": "Seat Information:\n• Computer Engineering: 48 seats\n• Civil Engineering: 48 seats\n• Electronics Engineering: 48 seats\n• Limited seats - apply early for better chances",
            "Scholarship_info": "Scholarship Opportunities:\n🏆 Merit-based scholarships (up to 55% fee waiver)\n💰 Need-based financial assistance\n🎯 Academic excellence awards\n🏅 Special scholarships for outstanding students",
            "Placement_info": "Placement Support:\n💼 Dedicated placement cell\n🤝 Industry partnerships\n📈 Good placement record\n🎯 Career counseling and guidance\n📊 Regular job fairs and campus recruitment",
            "Course_specific_info": "Our engineering programs are designed with:\n📚 Updated curriculum\n🔬 Practical lab sessions\n🏭 Industry exposure\n📖 Project-based learning\n👨‍🎓 Experienced faculty guidance",
            "Department_info": "Academic Departments:\n• Department of Computer and Electronics Engineering\n• Department of Civil Engineering\n• Each department has dedicated faculty and facilities",
            "Eligibility_criteria": "Eligibility Requirements:\n✅ Completed 10+2 or equivalent with Physics, Chemistry, and Mathematics\n✅ Minimum percentage requirements as per IOE guidelines\n✅ Pass IOE entrance examination\n✅ Meet age requirements",
            "Course_duration": "Course Duration:\n⏰ All engineering programs: 4 years (8 semesters)\n📅 Each semester: ~6 months\n🎓 Total: 140+ credit hours\n📝 Includes project work and practical training",
            "Course_cutoff": "Cutoff Information:\n📊 Computer Engineering: ~6000 rank\n📊 Civil Engineering: ~6000 rank\n📊 Electronics Engineering: ~6000 rank\n⚠️ Cutoffs vary each year based on competition",
            "Unknown": "I understand you're asking about Sagarmatha Engineering College. Could you please be more specific about what information you need?"
        }
        
        base_response = responses.get(intent, responses["Unknown"])
        
        # Add entity-specific context if relevant
        if entities and intent != "Unknown":
            entity_context = []
            for entity_type, entity_list in entities.items():
                entity_context.append(f"{entity_type}: {', '.join(entity_list)}")
            if entity_context:
                base_response += f"\n\n🔍 Detected context: {'; '.join(entity_context)}"
        
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
            "What are the eligibility criteria?",
            "How long is the engineering course?"
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
                print(f"🎯 Intent: {result['intent']} (Confidence: {result['confidence']:.3f})")
                print(f"🏷️ Entities: {result['entities'] if result['entities'] else 'None detected'}")
                
                # Show response
                print(f"\n🤖 Chatbot: {result['response']}")
                
                # Show top predictions if available
                if result.get('top_predictions') and len(result['top_predictions']) > 1:
                    print(f"\n📊 Alternative Intents:")
                    for intent, conf in result['top_predictions'][1:3]:  # Skip first one as it's already shown
                        if conf > 0:
                            print(f"   - {intent}: {conf:.3f}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    """Main function"""
    try:
        pipeline = WorkingPipeline()
        
        # Run demo
        pipeline.demo()
        
        # Start interactive chat
        pipeline.interactive_chat()
        
    except Exception as e:
        print(f"❌ Failed to start pipeline: {e}")

if __name__ == "__main__":
    main()
