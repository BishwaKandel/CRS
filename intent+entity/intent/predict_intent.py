"""
Simple Intent Prediction Script
Use the trained model to predict intents for new text
"""

import joblib
import json

class IntentPredictor:
    """Simple intent prediction using trained model"""
    
    def __init__(self, model_path='best_intent_classifier_model.pkl', 
                 vectorizer_path='best_intent_classifier_vectorizer.pkl',
                 labels_path='label_classes.json'):
        """Load trained model components"""
        print("🤖 Loading trained intent classifier...")
        
        # Load model and vectorizer
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        
        # Load label classes
        with open(labels_path, 'r') as f:
            self.label_classes = json.load(f)
        
        print(f"✅ Model loaded with {len(self.label_classes)} intent classes")
    
    def predict_intent(self, text):
        """Predict intent for given text"""
        # Vectorize the text
        text_vector = self.vectorizer.transform([text])
        
        # Predict intent
        prediction = self.model.predict(text_vector)[0]
        confidence_scores = self.model.predict_proba(text_vector)[0]
        
        # Get intent name and confidence
        predicted_intent = self.label_classes[prediction]
        confidence = confidence_scores[prediction]
        
        # Get top 3 predictions
        top_indices = confidence_scores.argsort()[-3:][::-1]
        top_predictions = []
        for idx in top_indices:
            intent_name = self.label_classes[idx]
            score = confidence_scores[idx]
            top_predictions.append((intent_name, score))
        
        return predicted_intent, confidence, top_predictions
    
    def interactive_prediction(self):
        """Interactive mode for testing predictions"""
        print("\n🎯 INTERACTIVE INTENT PREDICTION")
        print("=" * 40)
        print("Type your questions and I'll predict the intent!")
        print("Type 'quit' to exit")
        print("-" * 40)
        
        while True:
            try:
                user_input = input("\n💬 Enter text: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Predict intent
                intent, confidence, top_3 = self.predict_intent(user_input)
                
                print(f"\n🎯 Predicted Intent: {intent}")
                print(f"🔢 Confidence: {confidence:.3f}")
                print("\n📊 Top 3 Predictions:")
                for i, (pred_intent, score) in enumerate(top_3, 1):
                    print(f"  {i}. {pred_intent}: {score:.3f}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main prediction script"""
    print("🎯 INTENT PREDICTION - SAGARMATHA ENGINEERING COLLEGE")
    print("=" * 60)
    
    try:
        # Initialize predictor
        predictor = IntentPredictor()
        
        # Test with some sample texts
        print("\n🧪 Sample Predictions:")
        print("-" * 25)
        
        sample_texts = [
            "What courses are available?",
            "How much does it cost?",
            "Where is the college?",
            "Can I get hostel accommodation?",
            "Tell me about admission process",
            "What is the contact number?",
            "Do you have scholarships?",
            "When can I visit the campus?"
        ]
        
        for text in sample_texts:
            intent, confidence, _ = predictor.predict_intent(text)
            print(f"'{text}' → {intent} ({confidence:.3f})")
        
        # Start interactive mode
        predictor.interactive_prediction()
        
    except FileNotFoundError:
        print("❌ Error: Model files not found. Please train the model first:")
        print("  1. Run: python prepare_intent_data.py")
        print("  2. Run: python simple_ml_trainer.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
