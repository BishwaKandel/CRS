"""
Test Chatbot Pipeline - Simple verification script
"""

import os
import sys

def test_pipeline_basic():
    """Basic test without importing spacy (for testing core logic)"""
    print("🧪 Testing Basic Pipeline Components...")
    
    # Test 1: Check if intent predictor works
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from intent.predict_intent import IntentPredictor
        
        # Change to intent directory
        original_dir = os.getcwd()
        intent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'intent')
        os.chdir(intent_dir)
        
        predictor = IntentPredictor()
        
        # Test prediction
        test_text = "What courses are available?"
        intent, confidence, top_3 = predictor.predict_intent(test_text)
        
        print(f"✅ Intent Prediction Test:")
        print(f"   Text: {test_text}")
        print(f"   Intent: {intent}")
        print(f"   Confidence: {confidence:.3f}")
        
        os.chdir(original_dir)
        
    except Exception as e:
        print(f"❌ Intent Prediction Test Failed: {e}")
        return False
    
    # Test 2: Check if intent handler works
    try:
        # Import and test intent handler from main pipeline
        import importlib.util
        spec = importlib.util.spec_from_file_location("chatbot_pipeline", "chatbot_pipeline.py")
        chatbot_module = importlib.util.module_from_spec(spec)
        
        # Mock the spacy import for testing
        sys.modules['spacy'] = type(sys)('spacy')
        sys.modules['spacy'].load = lambda x: None
        
        spec.loader.exec_module(chatbot_module)
        
        handler = chatbot_module.IntentHandler()
        
        # Test intent handling
        test_intent = "Course_list"
        test_entities = {"Course": ["Computer Engineering"]}
        
        response = handler.handle_intent(test_intent, test_entities, "What courses do you have?", 0.95)
        
        print(f"\n✅ Intent Handler Test:")
        print(f"   Intent: {test_intent}")
        print(f"   Entities: {test_entities}")
        print(f"   Response Preview: {response[:100]}...")
        
    except Exception as e:
        print(f"❌ Intent Handler Test Failed: {e}")
        return False
    
    print(f"\n🎉 Basic pipeline components are working!")
    return True

def test_mock_ner():
    """Test a mock NER function for demonstration"""
    print("\n🧪 Testing Mock NER (for demo purposes)...")
    
    def mock_extract_entities(text):
        """Mock NER function that detects common college-related entities"""
        entities = {}
        
        # Mock entity detection based on keywords
        text_lower = text.lower()
        
        # Course detection
        courses = ["computer engineering", "civil engineering", "mechanical engineering", 
                  "electrical engineering", "electronics", "computer", "civil", "mechanical"]
        for course in courses:
            if course in text_lower:
                if "Course" not in entities:
                    entities["Course"] = []
                entities["Course"].append(course.title())
        
        # College name detection
        college_names = ["sagarmatha", "sec", "sagarmatha engineering college"]
        for college in college_names:
            if college in text_lower:
                if "College" not in entities:
                    entities["College"] = []
                entities["College"].append(college.title())
        
        return entities
    
    # Test cases
    test_cases = [
        "What courses does Sagarmatha Engineering College offer?",
        "I want to know about Computer Engineering fees",
        "Tell me about Civil Engineering at SEC",
        "How much does Mechanical Engineering cost?"
    ]
    
    for text in test_cases:
        entities = mock_extract_entities(text)
        print(f"   Text: {text}")
        print(f"   Entities: {entities}")
        print()
    
    print("✅ Mock NER working!")
    return True

def main():
    """Run all tests"""
    print("🔬 CHATBOT PIPELINE TESTING")
    print("=" * 40)
    
    success = True
    
    # Test basic components
    if not test_pipeline_basic():
        success = False
    
    # Test mock NER
    if not test_mock_ner():
        success = False
    
    if success:
        print("\n🎉 All tests passed! Pipeline is ready to use.")
        print("\nTo run the full pipeline:")
        print("1. Install requirements: pip install -r pipeline_requirements.txt")
        print("2. Download spacy model: python -m spacy download en_core_web_sm")
        print("3. Run: python chatbot_pipeline.py")
    else:
        print("\n❌ Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main()
