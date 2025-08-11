"""
Clean Intent Classification Data Preparation
Focus: Only intent classification, no entity extraction
"""

import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
from collections import Counter

class IntentDataPreparation:
    """Prepare clean intent classification data"""
    
    def __init__(self):
        self.label_encoder = LabelEncoder()
    
    def load_intent_data(self, file_path='enhanced_training_data.json'):
        """Load intent data from JSON file with enhanced dataset"""
        print(f"📂 Loading enhanced intent data from {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract examples and intents
        texts = []
        intents = []
        
        for intent_data in data['intents']:
            intent_name = intent_data['intent']
            examples = intent_data['examples']
            
            for example in examples:
                texts.append(example.strip())
                intents.append(intent_name)
        
        print(f"✅ Loaded {len(texts)} examples across {len(set(intents))} intents")
        
        return texts, intents
    
    def prepare_datasets(self, texts, intents):
        """Split data into train/test sets (no validation for small dataset)"""
        print("\n🔄 Preparing train/test splits...")
        print("ℹ️ Using simple train/test split due to small dataset size")
        
        # Encode labels
        intent_encoded = self.label_encoder.fit_transform(intents)
        label_classes = self.label_encoder.classes_.tolist()
        
        # Use more data for training with small dataset
        # Take 1-2 samples per class for testing, rest for training
        X_train, X_test, y_train, y_test = train_test_split(
            texts, intent_encoded, 
            test_size=0.20,  # 20% for test (about 1 sample per class)
            random_state=42, 
            stratify=intent_encoded
        )
        
        # Create validation set from training data
        X_train, X_val, y_train, y_val = train_test_split(
            X_train, y_train,
            test_size=0.15,  # 15% of training data for validation
            random_state=42
        )
        
        print(f"✅ Data split complete:")
        print(f"  Training: {len(X_train)} samples")
        print(f"  Validation: {len(X_val)} samples")
        print(f"  Test: {len(X_test)} samples")
        print(f"  Classes: {len(label_classes)} intents")
        
        return (X_train, X_val, X_test, y_train, y_val, y_test, label_classes)
    
    def create_dataframes(self, X_train, X_val, X_test, y_train, y_val, y_test, label_classes):
        """Create pandas DataFrames for easy handling"""
        print("\n📊 Creating DataFrames...")
        
        # Create DataFrames
        train_df = pd.DataFrame({
            'text': X_train,
            'intent': [label_classes[i] for i in y_train],
            'label_encoded': y_train
        })
        
        val_df = pd.DataFrame({
            'text': X_val,
            'intent': [label_classes[i] for i in y_val],
            'label_encoded': y_val
        })
        
        test_df = pd.DataFrame({
            'text': X_test,
            'intent': [label_classes[i] for i in y_test],
            'label_encoded': y_test
        })
        
        return train_df, val_df, test_df
    
    def compute_class_weights(self, y_train, label_classes):
        """Compute class weights for handling imbalanced data"""
        print("\n⚖️ Computing class weights...")
        
        # Count class distribution
        class_counts = Counter(y_train)
        print("Class distribution:")
        for i, class_name in enumerate(label_classes):
            count = class_counts.get(i, 0)
            print(f"  {class_name}: {count} samples")
        
        # Compute class weights
        class_weights = compute_class_weight(
            'balanced',
            classes=np.unique(y_train),
            y=y_train
        )
        
        class_weight_dict = {i: weight for i, weight in enumerate(class_weights)}
        
        return class_weight_dict
    
    def save_processed_data(self, train_df, val_df, test_df, label_classes, class_weights):
        """Save all processed data to files"""
        print("\n💾 Saving processed data...")
        
        # Save CSV files
        train_df.to_csv('train_data.csv', index=False)
        val_df.to_csv('val_data.csv', index=False)
        test_df.to_csv('test_data.csv', index=False)
        
        # Save metadata
        with open('label_classes.json', 'w') as f:
            json.dump(label_classes, f, indent=2)
        
        with open('class_weights.json', 'w') as f:
            json.dump(class_weights, f, indent=2)
        
        # Save statistics
        stats = {
            'total_samples': len(train_df) + len(val_df) + len(test_df),
            'train_samples': len(train_df),
            'val_samples': len(val_df),
            'test_samples': len(test_df),
            'num_classes': len(label_classes),
            'intents': label_classes
        }
        
        with open('data_stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
        
        print("✅ Saved files:")
        print("  - train_data.csv")
        print("  - val_data.csv") 
        print("  - test_data.csv")
        print("  - label_classes.json")
        print("  - class_weights.json")
        print("  - data_stats.json")
    
    def display_sample_data(self, train_df):
        """Display sample data for verification"""
        print("\n📋 Sample training data:")
        print("-" * 50)
        
        sample_data = train_df.groupby('intent').head(2)
        for _, row in sample_data.iterrows():
            print(f"Intent: {row['intent']}")
            print(f"Text: {row['text']}")
            print()

def main():
    """Main data preparation pipeline"""
    print("🚀 INTENT CLASSIFICATION - DATA PREPARATION")
    print("=" * 50)
    print("Focus: Clean intent classification (no entities)")
    print()
    
    # Initialize data preparation
    prep = IntentDataPreparation()
    
    try:
        # Load intent data
        texts, intents = prep.load_intent_data('enhanced_training_data.json')
        
        # Prepare datasets
        X_train, X_val, X_test, y_train, y_val, y_test, label_classes = prep.prepare_datasets(
            texts, intents
        )
        
        # Create DataFrames
        train_df, val_df, test_df = prep.create_dataframes(
            X_train, X_val, X_test, y_train, y_val, y_test, label_classes
        )
        
        # Compute class weights
        class_weights = prep.compute_class_weights(y_train, label_classes)
        
        # Save processed data
        prep.save_processed_data(train_df, val_df, test_df, label_classes, class_weights)
        
        # Display sample data
        prep.display_sample_data(train_df)
        
        print("🎉 DATA PREPARATION COMPLETE!")
        print("Ready to train with simple_ml_trainer.py")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
