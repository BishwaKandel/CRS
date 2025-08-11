"""
Real Trained Model Pipeline - Uses your actual trained intent classifier
This version loads your trained models with compatibility handling
"""

import os
import sys
import json
import re
from typing import Dict, List, Tuple, Any, Optional

# Add current directory to path for importing local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TrainedEntityExtractor:
    """Use your actual trained spaCy NER model"""
    
    def __init__(self, model_path='ner'):
        """Load your trained NER model"""
        print("🤖 Loading your trained NER model...")
        try:
            import spacy
            self.nlp = spacy.load(model_path)
            print(f"✅ Successfully loaded trained NER model from {model_path}")
            
            # Get available entity labels
            if self.nlp.get_pipe("ner"):
                labels = self.nlp.get_pipe("ner").labels
                print(f"📋 Available entity types: {list(labels)}")
            
            self.model_loaded = True
            
        except Exception as e:
            print(f"❌ Failed to load trained NER model: {e}")
            print("Using fallback pattern matching...")
            self.model_loaded = False
            self._init_fallback()
    
    def _init_fallback(self):
        """Initialize fallback patterns if NER model loading fails"""
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
            ]
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities using trained NER model or fallback"""
        
        if self.model_loaded:
            try:
                # Use actual trained NER model
                doc = self.nlp(text)
                entities = {}
                
                for ent in doc.ents:
                    entity_type = ent.label_
                    entity_text = ent.text
                    
                    if entity_type not in entities:
                        entities[entity_type] = []
                    
                    if entity_text not in entities[entity_type]:
                        entities[entity_type].append(entity_text)
                
                return entities
                
            except Exception as e:
                print(f"❌ Error using trained NER model: {e}")
                print("Falling back to pattern matching...")
                return self._fallback_extract(text)
        else:
            return self._fallback_extract(text)
    
    def _fallback_extract(self, text: str) -> Dict[str, List[str]]:
        """Fallback pattern-based entity extraction"""
        import re
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

class TrainedIntentPredictor:
    """Load and use your actual trained intent classifier"""
    
    def __init__(self):
        print("🤖 Loading your trained intent classifier...")
        
        # Try to load the actual trained models
        try:
            # Fix numpy compatibility issue
            os.environ['SKLEARN_ENABLE_VERSION_MISMATCH'] = '1'
            
            import joblib
            import warnings
            warnings.filterwarnings('ignore')
            
            # Load model components
            model_path = os.path.join('intent', 'best_intent_classifier_model.pkl')
            vectorizer_path = os.path.join('intent', 'best_intent_classifier_vectorizer.pkl')
            labels_path = os.path.join('intent', 'label_classes.json')
            
            # Check if files exist
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            if not os.path.exists(vectorizer_path):
                raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")
            if not os.path.exists(labels_path):
                raise FileNotFoundError(f"Labels file not found: {labels_path}")
            
            # Load with error handling
            print(f"Loading model from: {model_path}")
            self.model = joblib.load(model_path)
            
            print(f"Loading vectorizer from: {vectorizer_path}")
            self.vectorizer = joblib.load(vectorizer_path)
            
            print(f"Loading labels from: {labels_path}")
            with open(labels_path, 'r') as f:
                label_data = json.load(f)
                # Handle both list and dict formats
                if isinstance(label_data, dict):
                    self.label_classes = label_data
                elif isinstance(label_data, list):
                    self.label_classes = {i: label for i, label in enumerate(label_data)}
                else:
                    raise ValueError("Invalid label classes format")
            
            self.model_loaded = True
            print(f"✅ Successfully loaded trained model with {len(self.label_classes)} intent classes")
            print(f"Available intents: {list(self.label_classes.values())}")
            
        except Exception as e:
            print(f"❌ Failed to load trained model: {e}")
            print("Using fallback intent classification...")
            self.model_loaded = False
            self._init_fallback()
    
    def _init_fallback(self):
        """Initialize fallback intent patterns if model loading fails"""
        self.intent_patterns = {
            "College_basic_info": [r"tell me about", r"what is", r"about.*college", r"information.*college"],
            "Course_list": [r"what courses", r"courses.*offer", r"programs.*available"],
            "College_location": [r"where.*located", r"location.*college", r"address"],
            "Admission_process": [r"admission.*process", r"how.*apply", r"how.*join"],
            "Course_fee": [r"fee", r"cost", r"price", r"tuition", r"how much.*cost"],
            "Faculty_info": [r"faculty", r"teachers", r"professors", r"instructors"],
            "Hostel_availability": [r"hostel", r"accommodation", r"stay.*campus"],
            "Course_seats": [r"seats.*available", r"how many.*seats", r"capacity"],
            "Scholarship_info": [r"scholarship", r"financial.*aid", r"merit.*award"],
            "Placement_info": [r"placement", r"job.*opportunities", r"career.*prospects"],
        }
        self.label_classes = {i: intent for i, intent in enumerate(self.intent_patterns.keys())}
    
    def predict_intent(self, text: str) -> Tuple[str, float, List[Tuple[str, float]]]:
        """Predict intent using trained model or fallback"""
        
        if self.model_loaded:
            try:
                # Use actual trained model
                text_vector = self.vectorizer.transform([text])
                prediction = self.model.predict(text_vector)[0]
                confidence_scores = self.model.predict_proba(text_vector)[0]
                
                # Get intent name and confidence
                predicted_intent = self.label_classes[str(prediction)] if str(prediction) in self.label_classes else self.label_classes[prediction]
                confidence = confidence_scores[prediction]
                
                # Get top 3 predictions
                top_indices = confidence_scores.argsort()[-3:][::-1]
                top_predictions = []
                for idx in top_indices:
                    intent_key = str(idx) if str(idx) in self.label_classes else idx
                    intent_name = self.label_classes[intent_key]
                    score = confidence_scores[idx]
                    top_predictions.append((intent_name, score))
                
                return predicted_intent, confidence, top_predictions
                
            except Exception as e:
                print(f"❌ Error using trained model: {e}")
                print("Falling back to pattern matching...")
                return self._fallback_predict(text)
        else:
            return self._fallback_predict(text)
    
    def _fallback_predict(self, text: str) -> Tuple[str, float, List[Tuple[str, float]]]:
        """Fallback pattern-based prediction"""
        text_lower = text.lower()
        scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    score += 1
            if patterns:
                scores[intent] = score / len(patterns)
        
        if scores:
            best_intent = max(scores, key=scores.get)
            confidence = scores[best_intent]
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            top_predictions = [(intent, score) for intent, score in sorted_scores[:3]]
            return best_intent, confidence, top_predictions
        else:
            return "Unknown", 0.0, [("Unknown", 0.0)]

class RealTrainedPipeline:
    """Pipeline using your actual trained models"""
    
    def __init__(self):
        print("🤖 Initializing Real Trained Model Pipeline...")
        print("=" * 60)
        
        # Initialize entity extractor (using your trained NER model)
        self.entity_extractor = TrainedEntityExtractor()
        print("✅ Entity extractor initialized")
        
        # Initialize trained intent predictor
        self.intent_predictor = TrainedIntentPredictor()
        
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
        
        # Predict intent using trained model
        intent, confidence, top_predictions = self.intent_predictor.predict_intent(text)
        result["intent"] = intent
        result["confidence"] = confidence
        result["top_predictions"] = top_predictions
        
        # Generate response
        result["response"] = self.generate_response(intent, entities, text)
        
        return result
    
    def generate_response(self, intent: str, entities: Dict, text: str) -> str:
        """Generate response based on intent and entities"""
        # Use responses based on your training data patterns
        responses = {
            "College_basic_info": "Sagarmatha Engineering College (SEC) is a private engineering college located in Sanepa, Lalitpur, Nepal.",
            "Course_list": "SEC offers Computer Engineering, Civil Engineering, and Electronics & Communication Engineering programs.",
            "College_location": "Sagarmatha Engineering College is located in Sanepa, Lalitpur, Nepal. Contact: 015427274",
            "Admission_process": "Admission is based on IOE entrance examination results. Contact our admission office for the detailed process.",
            "Course_fee": "Course fees vary by program. Please contact the admission office for detailed fee structure.",
            "Faculty_info": "SEC has experienced faculty members across all engineering departments.",
            "Hostel_availability": "Currently, SEC does not have on-campus hostel facilities, but nearby accommodation options are available.",
            "Course_seats": "Each program has 48 seats. Total seats vary by program.",
            "Scholarship_info": "Merit-based scholarships up to 55% are available for eligible students.",
            "Placement_info": "SEC has a dedicated placement cell with good placement records in the industry.",
            "Course_specific_info": "Our engineering programs include practical lab sessions, project work, and industry exposure.",
            "Department_info": "SEC has Department of Computer and Electronics Engineering and Department of Civil Engineering.",
            "Eligibility_criteria": "Completion of 10+2 with Physics, Chemistry, Mathematics and passing IOE entrance exam.",
            "Course_duration": "All engineering programs are 4-year Bachelor's degree programs.",
            "Course_cutoff": "Cutoff ranks vary each year. Generally around 6000 rank for most programs.",
            "College_contact": "Contact SEC at 015427274 or email info@sagarmatha.edu.np",
            "Course_rating": "SEC maintains good academic standards with experienced faculty and modern facilities.",
            "Compare_courses": "All engineering programs at SEC are well-designed with industry-relevant curriculum.",
            "Internship_opportunities": "SEC provides internship opportunities and industry exposure for students.",
            "Department_head": "Each department has experienced department heads leading the academic programs."
        }
        
        response = responses.get(intent, "Thank you for your question about Sagarmatha Engineering College. How can I help you?")
        
        # Add entity context if available
        if entities:
            entity_context = []
            for entity_type, entity_list in entities.items():
                entity_context.append(f"{entity_type}: {', '.join(entity_list)}")
            if entity_context:
                response += f"\\n\\n🔍 Context: {'; '.join(entity_context)}"
        
        return response
    
    def demo(self):
        """Run demonstration with sample queries"""
        print("\\n🧪 PIPELINE DEMONSTRATION - REAL TRAINED MODELS")
        print("=" * 60)
        
        sample_queries = [
            "Tell me about Sagarmatha Engineering College",
            "What courses do you offer?", 
            "Where is SEC located?",
            "How much does Computer Engineering cost?",
            "Do you have hostel facilities?",
            "What is the admission process?",
            "Are scholarships available?",
            "How many seats are available?",
            "What are the eligibility criteria?",
            "How long is the engineering course?"
        ]
        
        for i, query in enumerate(sample_queries, 1):
            print(f"\\n📝 Query {i}: {query}")
            print("-" * 50)
            
            result = self.process_query(query)
            
            print(f"🎯 Intent: {result['intent']} (Confidence: {result['confidence']:.3f})")
            print(f"🏷️ Entities: {result['entities'] if result['entities'] else 'None detected'}")
            print(f"🤖 Response: {result['response']}")
            
            if result.get('top_predictions') and len(result['top_predictions']) > 1:
                print(f"📊 Top Predictions:")
                for intent, conf in result['top_predictions'][:3]:
                    print(f"   - {intent}: {conf:.3f}")
            
            print("\\n" + "="*60)
    
    def interactive_chat(self):
        """Interactive chat mode"""
        print("\\n💬 INTERACTIVE CHAT MODE - REAL TRAINED MODELS")
        print("Type 'quit', 'exit', or 'bye' to stop")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye', '']:
                    print("👋 Goodbye! Thank you for using Sagarmatha Engineering College Chatbot!")
                    break
                
                result = self.process_query(user_input)
                
                # Show analysis
                print(f"\\n📋 Analysis:")
                print(f"🎯 Intent: {result['intent']} (Confidence: {result['confidence']:.3f})")
                print(f"🏷️ Entities: {result['entities'] if result['entities'] else 'None detected'}")
                
                # Show response
                print(f"\\n🤖 Chatbot: {result['response']}")
                
                # Show alternatives
                if result.get('top_predictions') and len(result['top_predictions']) > 1:
                    print(f"\\n📊 Alternative Intents:")
                    for intent, conf in result['top_predictions'][1:3]:
                        if conf > 0:
                            print(f"   - {intent}: {conf:.3f}")
                
            except KeyboardInterrupt:
                print("\\n\\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\\n❌ Error: {e}")

def main():
    """Main function"""
    try:
        pipeline = RealTrainedPipeline()
        
        # Run demo
        pipeline.demo()
        
        # Start interactive chat
        pipeline.interactive_chat()
        
    except Exception as e:
        print(f"❌ Failed to start pipeline: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
