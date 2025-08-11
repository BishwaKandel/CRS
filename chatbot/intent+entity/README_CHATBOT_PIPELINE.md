# Sagarmatha Engineering College Chatbot Pipeline

## Overview

This chatbot pipeline integrates your trained Intent Classifier and NER models to create a complete conversational AI system for handling college-related queries.

## System Architecture

```
User Input → Intent Classification → Entity Extraction → Intent Handling → Response Generation
```

### Components

1. **Intent Predictor** (uses your trained model)

   - Uses `best_intent_classifier_model.pkl`
   - Uses `best_intent_classifier_vectorizer.pkl`
   - Classifies user queries into 20+ intent categories

2. **NER Extractor** (two versions available)

   - **Full Version**: Uses your trained spaCy NER model (`ner/` directory)
   - **Simplified Version**: Uses pattern-matching for entity detection

3. **Intent Handler**

   - Maps intents to appropriate responses
   - Incorporates detected entities into responses
   - Handles confidence thresholds

4. **Main Pipeline**
   - Orchestrates all components
   - Provides interactive chat interface
   - Includes demo functionality

## Files Structure

```
intent+entity/
├── chatbot_pipeline.py           # Full pipeline with spaCy NER
├── simple_chatbot_pipeline.py    # Simplified pipeline with mock NER
├── test_pipeline.py              # Testing script
├── pipeline_requirements.txt     # Dependencies
├── intent/
│   ├── best_intent_classifier_model.pkl     # Your trained intent model
│   ├── best_intent_classifier_vectorizer.pkl
│   ├── label_classes.json                   # Intent labels
│   └── predict_intent.py                    # Intent prediction logic
└── ner/                                     # Your trained NER model
    ├── config.cfg
    ├── meta.json
    └── ...
```

## Supported Intents

The system can handle 20+ intent categories including:

- **Academic**: Course_list, Course_fee, Course_specific_info, Eligibility_criteria
- **Admission**: Admission_process, College_basic_info, Course_cutoff
- **Contact**: College_contact, College_location
- **Facilities**: Hostel_availability, Faculty_info, Department_info
- **Support**: Scholarship_info, Placement_info, Internship_opportunities
- **Comparison**: Compare_courses, Course_rating, Course_seats

## Entity Types (NER)

The NER system can detect:

- **College**: Sagarmatha, SEC, College names
- **Course**: Computer Engineering, Civil Engineering, etc.
- **Department**: Various department names
- **Facility**: Hostel, Library, Lab, etc.

## How to Use the Pipeline

### Prerequisites

Before using the pipeline, ensure you have:

- Python 3.7 or higher installed
- Your trained intent classifier models in the `intent/` directory:
  - `best_intent_classifier_model.pkl`
  - `best_intent_classifier_vectorizer.pkl`
  - `label_classes.json`
- Your trained NER model in the `ner/` directory (for full pipeline)

### Step-by-Step Usage Guide

#### Step 1: Quick Test (Verify Everything Works)

```bash
# Navigate to your project directory
cd "d:\college_project_major\intent+entity"

# Run the test script to verify all components
python test_pipeline.py
```

Expected output:

```
🔬 CHATBOT PIPELINE TESTING
========================================
🧪 Testing Basic Pipeline Components...
✅ Intent Prediction Test: Course_list (confidence: 0.579)
✅ Intent Handler Test: Available Courses...
✅ Mock NER working!
🎉 All tests passed! Pipeline is ready to use.
```

#### Step 2: Choose Your Pipeline Version

**Option A: Simple Pipeline (Recommended for beginners)**

```bash
# Run the simplified pipeline with mock NER
python simple_chatbot_pipeline.py

# Choose option when prompted:
# 1. See demo with sample queries
# 2. Start interactive chat
# 3. Both (demo first, then chat)
```

**Option B: Full Pipeline (Advanced users)**

```bash
# Install additional dependencies
pip install -r pipeline_requirements.txt
python -m spacy download en_core_web_sm

# Run full pipeline with trained NER
python chatbot_pipeline.py
```

**Option C: Test Components**

```bash
python test_pipeline.py
```

### Interactive Usage

#### Method 1: Command Line Interface

```bash
python simple_chatbot_pipeline.py
```

Sample interaction:

```
🎓 SAGARMATHA ENGINEERING COLLEGE CHATBOT
=======================================================
Hello! I'm your virtual assistant for Sagarmatha Engineering College! 🤖

💬 You: What courses do you offer?
🤖 Bot: Available Courses:
• Computer Engineering (4 years)
• Civil Engineering (4 years)
• Electronics & Communication Engineering (4 years)
...

💬 You: How much does Computer Engineering cost?
🤖 Bot: Fee Structure Information:
• Fees vary by program (approx. NPR 2-4 lakhs per year)
• Scholarship opportunities available
...
```

#### Method 2: Programmatic Usage

```python
# Import the pipeline
from simple_chatbot_pipeline import SimpleChatbotPipeline

# Initialize chatbot
chatbot = SimpleChatbotPipeline()

# Process single query
result = chatbot.process_message("What courses are available?")
print(f"Intent: {result['predicted_intent']}")
print(f"Response: {result['response']}")

# Process multiple queries
queries = ["Where is the college?", "How much are the fees?"]
for query in queries:
    result = chatbot.process_message(query)
    print(f"Q: {query}")
    print(f"A: {result['response'][:100]}...")
```

### Demo Mode

To see the system capabilities:

```bash
python simple_chatbot_pipeline.py
# Choose option 1 or 3 to see demo
```

Demo shows:

- Sample queries and responses
- Intent detection accuracy
- Entity extraction results
- Confidence scores
- Technical details

### Batch Processing

For processing multiple queries programmatically:

```python
# See example_usage.py for complete examples
python example_usage.py
```

### Usage Examples by Category

#### Academic Queries

```
"What courses are available?"
"How long is the Computer Engineering program?"
"What are the eligibility criteria?"
"Tell me about the Civil Engineering curriculum"
```

#### Admission Queries

```
"How can I apply for admission?"
"What documents do I need?"
"When is the admission deadline?"
"What is the selection process?"
```

#### Financial Queries

```
"How much are the fees?"
"Are scholarships available?"
"Can I pay fees in installments?"
"What financial aid options exist?"
```

#### Facility Queries

```
"Do you have hostel facilities?"
"Where is the college located?"
"What lab facilities are available?"
"How can I contact the college?"
```

### Troubleshooting Usage Issues

#### Common Problems and Solutions

**1. Import Errors**

```bash
# Error: ModuleNotFoundError: No module named 'intent.predict_intent'
# Solution: Ensure you're in the correct directory
cd "d:\college_project_major\intent+entity"
python simple_chatbot_pipeline.py
```

**2. Model Loading Errors**

```bash
# Error: FileNotFoundError: Model files not found
# Solution: Check model files exist in intent/ directory
ls intent/best_intent_classifier_model.pkl
ls intent/label_classes.json
```

**3. Low Confidence Responses**

```
# If getting too many fallback responses:
# 1. Check your query spelling and grammar
# 2. Use more specific college-related terms
# 3. Try example queries from demo mode
```

**4. spaCy Errors (Full Pipeline)**

```bash
# Error: Can't find model 'en_core_web_sm'
# Solution: Install spaCy language model
python -m spacy download en_core_web_sm

# Alternative: Use simple pipeline instead
python simple_chatbot_pipeline.py
```

### Performance Tips

1. **For Development**: Use simple pipeline for faster iteration
2. **For Production**: Use full pipeline with trained NER for better accuracy
3. **Batch Processing**: Process multiple queries in single session for efficiency
4. **Confidence Monitoring**: Track confidence scores to improve intent training
5. **Entity Validation**: Verify entity extraction accuracy for domain-specific terms

### Integration Examples

#### Web Application Integration

```python
from flask import Flask, request, jsonify
from simple_chatbot_pipeline import SimpleChatbotPipeline

app = Flask(__name__)
chatbot = SimpleChatbotPipeline()

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    result = chatbot.process_message(user_message)
    return jsonify({
        'response': result['response'],
        'intent': result['predicted_intent'],
        'confidence': result['confidence']
    })
```

#### API Endpoint Usage

```python
# For REST API integration
def handle_chat_request(user_input):
    chatbot = SimpleChatbotPipeline()
    result = chatbot.process_message(user_input)

    return {
        'success': result['status'] == 'success',
        'response': result['response'],
        'metadata': {
            'intent': result['predicted_intent'],
            'confidence': result['confidence'],
            'entities': result['entities']
        }
    }
```

## Features

### 1. Interactive Chat Mode

- Natural conversation interface
- Real-time intent and entity detection
- Contextual responses based on detected entities
- Confidence scoring and fallback handling

### 2. Demo Mode

- Showcases system capabilities with sample queries
- Displays technical details (intent, confidence, entities)
- Helps understand system behavior

### 3. Robust Error Handling

- Graceful degradation for low-confidence predictions
- Fallback responses for unknown intents
- Error recovery and user guidance

### 4. Entity-Aware Responses

- Responses are customized based on detected entities
- Mentions specific courses, facilities, or college names
- Provides targeted information

## Example Conversations

### Query: "What courses does Sagarmatha Engineering College offer?"

- **Intent**: Course_list (confidence: 0.446)
- **Entities**: College: ["Sagarmatha Engineering College", "Sagarmatha", "College"]
- **Response**: Lists available courses with entity acknowledgment

### Query: "How much does Computer Engineering cost?"

- **Intent**: Course_fee (confidence: 0.575)
- **Entities**: Course: ["Computer Engineering", "Computer"]
- **Response**: Fee information with course-specific details

### Query: "Do you have hostel facilities?"

- **Intent**: Hostel_availability (confidence: 0.972)
- **Entities**: Facility: ["Hostel"]
- **Response**: Detailed hostel information

## Performance Characteristics

- **High Accuracy**: Intent classification confidence typically 0.4-0.9+
- **Entity Recognition**: Pattern-based detection for college-specific terms
- **Response Quality**: Structured, informative responses with entity context
- **Fallback Handling**: Graceful handling of unclear queries

## Customization Options

### Adding New Intents

1. Update `response_templates` in `IntentHandler` class
2. Retrain your intent classifier with new data
3. Update `label_classes.json`

### Enhancing Entity Recognition

1. **For Mock NER**: Update `entity_patterns` in `MockNERExtractor`
2. **For spaCy NER**: Retrain your spaCy model with new entity types

### Modifying Responses

- Edit `response_templates` dictionary in `IntentHandler`
- Adjust confidence thresholds in `process_message`
- Customize fallback responses

## Technical Requirements

### Minimum (Simple Pipeline)

- Python 3.7+
- scikit-learn
- joblib
- Your trained intent models

### Full Features

- Python 3.7+
- scikit-learn, joblib
- spaCy 3.8+
- Your trained intent + NER models

## Integration Notes

- **Existing Models**: Seamlessly uses your pre-trained models
- **No Retraining**: Works with current model files
- **Modular Design**: Components can be used independently
- **Extensible**: Easy to add new features or modify behavior

## Future Enhancements

1. **Context Memory**: Remember conversation history
2. **Multi-turn Conversations**: Handle follow-up questions
3. **Rich Responses**: Add multimedia, links, or formatted text
4. **Analytics**: Track popular queries and user satisfaction
5. **Integration**: Connect with college databases for real-time info

## Troubleshooting

### Common Issues

1. **Model Loading Errors**: Ensure model files are in correct directories
2. **Version Warnings**: scikit-learn version mismatch (usually harmless)
3. **spaCy Errors**: Install language model or use simple pipeline

### Performance Tips

1. Use simple pipeline for development/testing
2. Cache model loading for production use
3. Implement query preprocessing for better intent detection
4. Monitor confidence scores and adjust thresholds

---

## Quick Reference - Commands

### Essential Commands

```bash
# Test everything works
python test_pipeline.py

# Start interactive chatbot (recommended)
python simple_chatbot_pipeline.py

# See programming examples
python example_usage.py

# Advanced: Full pipeline with spaCy
pip install -r pipeline_requirements.txt
python -m spacy download en_core_web_sm
python chatbot_pipeline.py
```

### Quick Programmatic Usage

```python
from simple_chatbot_pipeline import SimpleChatbotPipeline

# Initialize and use
chatbot = SimpleChatbotPipeline()
result = chatbot.process_message("What courses are available?")
print(result['response'])
```

### File Structure Check

```
intent+entity/
├── simple_chatbot_pipeline.py    ← Main file to run
├── test_pipeline.py              ← Test first
├── example_usage.py              ← See examples
├── intent/
│   ├── best_intent_classifier_model.pkl     ← Required
│   ├── best_intent_classifier_vectorizer.pkl ← Required
│   └── label_classes.json                   ← Required
└── ner/                          ← Optional (for full pipeline)
```

This chatbot pipeline successfully demonstrates how to integrate trained ML models (Intent Classification + NER) into a complete conversational AI system, providing an interactive and intelligent assistant for college information queries.
