"""
Debug Intent Confidence - Compare confidence scores and analyze distribution
"""

import os
import sys
import json
import joblib
import numpy as np

# Add path for intent module
sys.path.append(os.path.join(os.path.dirname(__file__), 'intent'))

class DebugIntentPredictor:
    """Debug version to analyze confidence scores"""
    
    def __init__(self):
        print("🔍 DEBUG: Loading intent classifier for confidence analysis...")
        
        # Load model components
        model_path = os.path.join('intent', 'best_intent_classifier_model.pkl')
        vectorizer_path = os.path.join('intent', 'best_intent_classifier_vectorizer.pkl')
        labels_path = os.path.join('intent', 'label_classes.json')
        
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        
        with open(labels_path, 'r') as f:
            label_data = json.load(f)
            if isinstance(label_data, dict):
                self.label_classes = label_data
            elif isinstance(label_data, list):
                self.label_classes = {i: label for i, label in enumerate(label_data)}
        
        print(f"✅ Model loaded with {len(self.label_classes)} classes")
    
    def debug_predict(self, text: str):
        """Detailed prediction analysis"""
        print(f"\n🔍 DEBUGGING PREDICTION FOR: '{text}'")
        print("=" * 60)
        
        # Vectorize
        text_vector = self.vectorizer.transform([text])
        print(f"📊 Text vector shape: {text_vector.shape}")
        print(f"📊 Text vector sparsity: {(text_vector.data.size / text_vector.shape[1]):.4f}")
        
        # Get all probabilities
        all_probabilities = self.model.predict_proba(text_vector)[0]
        prediction = self.model.predict(text_vector)[0]
        
        print(f"\\n🎯 RAW PREDICTION ANALYSIS:")
        print(f"Predicted class index: {prediction}")
        print(f"Predicted intent: {self.label_classes[prediction]}")
        print(f"Confidence: {all_probabilities[prediction]:.6f}")
        
        # Show distribution analysis
        print(f"\\n📈 PROBABILITY DISTRIBUTION:")
        print(f"Max probability: {np.max(all_probabilities):.6f}")
        print(f"Min probability: {np.min(all_probabilities):.6f}")
        print(f"Mean probability: {np.mean(all_probabilities):.6f}")
        print(f"Std deviation: {np.std(all_probabilities):.6f}")
        
        # Show top 10 predictions
        print(f"\\n🏆 TOP 10 PREDICTIONS:")
        top_indices = all_probabilities.argsort()[-10:][::-1]
        for i, idx in enumerate(top_indices):
            intent_name = self.label_classes[idx]
            score = all_probabilities[idx]
            percentage = score * 100
            print(f"  {i+1:2d}. {intent_name:25s}: {score:.6f} ({percentage:.2f}%)")
        
        # Check if this is actually good confidence for 24 classes
        print(f"\\n💡 ANALYSIS:")
        theoretical_random = 1.0 / len(self.label_classes)
        confidence_ratio = all_probabilities[prediction] / theoretical_random
        print(f"Random chance probability: {theoretical_random:.6f} ({theoretical_random*100:.2f}%)")
        print(f"Actual confidence: {all_probabilities[prediction]:.6f} ({all_probabilities[prediction]*100:.2f}%)")
        print(f"Confidence ratio vs random: {confidence_ratio:.2f}x")
        
        if confidence_ratio > 2:
            print("✅ This is actually GOOD confidence for 24 classes!")
        elif confidence_ratio > 1.5:
            print("⚠️ Moderate confidence - reasonable for multi-class")
        else:
            print("❌ Low confidence - model is uncertain")
        
        return self.label_classes[prediction], all_probabilities[prediction]

def main():
    predictor = DebugIntentPredictor()
    
    test_queries = [
        "Tell me about Sagarmatha Engineering College",
        "Where is sagarmatha engineering college located",
        "What courses do you offer",
        "How much does Computer Engineering cost",
        "Do you have hostel facilities",
        "What is the admission process"
    ]
    
    for query in test_queries:
        intent, confidence = predictor.debug_predict(query)
        print("\\n" + "="*80 + "\\n")

if __name__ == "__main__":
    main()
