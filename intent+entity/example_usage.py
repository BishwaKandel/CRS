"""
Example Usage - Chatbot Pipeline Integration
Shows how to use the chatbot pipeline programmatically
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_chatbot_pipeline import SimpleChatbotPipeline

def example_single_query():
    """Example: Process a single query"""
    print("🔍 Example 1: Single Query Processing")
    print("="*40)
    
    # Initialize chatbot
    chatbot = SimpleChatbotPipeline()
    
    # Process a single query
    query = "What are the admission requirements for Computer Engineering?"
    result = chatbot.process_message(query)
    
    print(f"Query: {query}")
    print(f"Intent: {result['predicted_intent']}")
    print(f"Confidence: {result['confidence']:.3f}")
    print(f"Entities: {result['entities']}")
    print(f"Response: {result['response'][:200]}...")

def example_batch_processing():
    """Example: Process multiple queries"""
    print("\n🔍 Example 2: Batch Query Processing")
    print("="*40)
    
    # Initialize chatbot
    chatbot = SimpleChatbotPipeline()
    
    queries = [
        "What courses are available?",
        "How much does it cost to study here?",
        "Where is the college located?",
        "Do you provide hostel accommodation?",
        "Tell me about scholarships"
    ]
    
    results = []
    for query in queries:
        result = chatbot.process_message(query)
        results.append(result)
        
        print(f"Q: {query}")
        print(f"A: {result['predicted_intent']} ({result['confidence']:.2f})")
        if result['entities']:
            print(f"   Entities: {result['entities']}")
        print()

def example_custom_handler():
    """Example: Custom intent handling"""
    print("\n🔍 Example 3: Custom Response Generation")
    print("="*40)
    
    # Initialize chatbot
    chatbot = SimpleChatbotPipeline()
    
    # Process query
    query = "I want to apply for Computer Engineering"
    result = chatbot.process_message(query)
    
    # Custom handling based on intent and entities
    if result['predicted_intent'] == 'Course_specific_info':
        if result['entities'] and 'Course' in result['entities']:
            course = result['entities']['Course'][0]
            custom_response = f"""
🎯 Great! You're interested in {course}!

Here's what you need to know for admission:
✅ Eligibility: 10+2 with PCM (Physics, Chemistry, Math)
✅ Entrance: IOE Entrance Exam
✅ Duration: 4 years
✅ Career: Software Engineer, System Analyst, IT Consultant

Would you like specific information about:
1. Admission deadlines
2. Fee structure  
3. Curriculum details
4. Career opportunities
"""
            print(f"Original Response Preview: {result['response'][:100]}...")
            print(f"\nCustom Enhanced Response:{custom_response}")

def example_confidence_based_handling():
    """Example: Handle different confidence levels"""
    print("\n🔍 Example 4: Confidence-Based Handling")
    print("="*40)
    
    chatbot = SimpleChatbotPipeline()
    
    test_queries = [
        "What courses do you offer?",  # High confidence expected
        "Tell me something about college",  # Medium confidence expected
        "abcd xyz random text"  # Low confidence expected
    ]
    
    for query in test_queries:
        result = chatbot.process_message(query)
        confidence = result['confidence']
        
        print(f"Query: {query}")
        print(f"Confidence: {confidence:.3f}")
        
        if confidence > 0.8:
            print("✅ High confidence - Direct response")
        elif confidence > 0.5:
            print("⚠️ Medium confidence - Response with clarification")
        else:
            print("❌ Low confidence - Fallback response")
        
        print(f"Response type: {'Success' if result['status'] == 'success' else 'Error'}")
        print()

def example_entity_extraction_demo():
    """Example: Focus on entity extraction"""
    print("\n🔍 Example 5: Entity Extraction Demo")
    print("="*40)
    
    chatbot = SimpleChatbotPipeline()
    
    entity_test_queries = [
        "I want to study Computer Engineering at Sagarmatha Engineering College",
        "Tell me about Civil Engineering department",
        "What hostel facilities are available at SEC?",
        "How is the Mechanical Engineering course?"
    ]
    
    for query in entity_test_queries:
        result = chatbot.process_message(query)
        
        print(f"Query: {query}")
        print(f"Entities found:")
        
        if result['entities']:
            for entity_type, entity_values in result['entities'].items():
                print(f"  {entity_type}: {', '.join(entity_values)}")
        else:
            print("  No entities detected")
        print()

def main():
    """Run all examples"""
    print("🚀 CHATBOT PIPELINE - USAGE EXAMPLES")
    print("="*50)
    
    try:
        # Run examples
        example_single_query()
        example_batch_processing()
        example_custom_handler()
        example_confidence_based_handling()
        example_entity_extraction_demo()
        
        print("\n🎉 All examples completed successfully!")
        print("\nTo use the chatbot interactively, run:")
        print("python simple_chatbot_pipeline.py")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")

if __name__ == "__main__":
    main()
