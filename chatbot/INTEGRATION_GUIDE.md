# College Recommendation System Integration Guide

## System Overview

The College Recommendation System integrates three key components to provide intelligent college recommendations based on natural language queries:

1. **Intent & Entity Recognition**: Analyzes user queries to identify the intent (what the user wants) and entities (specific criteria like location, course, etc.)
2. **SQL Builder**: Converts intents and entities into SQL queries to retrieve matching colleges from the database
3. **Recommendation Engine**: Ranks and compares colleges based on user preferences with customizable weighting factors

![System Architecture](system_architecture.png)

## How It Works

### 1. Processing a User Query

When a user enters a natural language query like "Show me affordable engineering colleges in Lalitpur with hostel facility", the system:

1. Extracts the intent (e.g., "find_affordable_college")
2. Identifies entities (e.g., "COURSE": ["engineering"], "LOCATION": ["Lalitpur"], "HOSTEL": ["facility"])
3. Maps these to a SQL query to retrieve matching colleges
4. Creates a student profile from extracted preferences
5. Determines comparison factors (location, fee, pass rate) based on the query
6. Ranks colleges using the recommendation engine
7. Returns personalized college recommendations

### 2. Components Interaction

```
User Query → Intent+Entity Pipeline → SQL Builder → Recommendation Engine → Ranked Results
```

## Example Queries

The system can handle various types of queries:

- "Which are the best engineering colleges in Kathmandu?"
- "Show me affordable private colleges with computer science"
- "Top rated civil engineering programs with internship opportunities"
- "Colleges with hostel facility near Lalitpur"
- "Compare electrical engineering programs by fee and pass rate"

## Integration Details

### Intent and Entity Mapping

Intents are mapped to different search strategies:

- `find_affordable_college` → Sort by lowest fees
- `find_top_rated_college` → Sort by highest ratings
- `compare_colleges` → Compare by specified factors

Entities are mapped to SQL query conditions:

- `COLLEGE` → Filter by college name
- `LOCATION` → Filter by college location
- `COURSE`/`DEPARTMENT` → Filter by course or department name
- `TYPE` → Filter by college type (public/private)
- `HOSTEL` → Filter for hostel availability
- `MAX_FEE` → Filter by maximum fee amount

### Recommendation Factors

The system can compare colleges based on three primary factors:

1. **Location** - Proximity to preferred locations
2. **Fee** - Affordability based on tuition costs
3. **Pass Rate** - Academic quality based on pass percentage

The system automatically selects relevant factors based on the query or uses all three with equal weights by default.

## Usage Example

```python
from chatbot_integrator import ChatbotIntegrator

# Initialize the integrator
integrator = ChatbotIntegrator()

# Process a user query
result = integrator.process_query("Show me affordable engineering colleges in Lalitpur with hostel facility")

# Access the recommendations
for rec in result['recommendations']:
    print(f"{rec['college_name']} - {rec['match_percentage']:.1f}% match")
    print(f"Fee: {rec['fee']} | Location: {rec['location']}")
```

## Database Schema

The system works with the following database structure:

- **College**: Basic college information (name, location, type, contact details)
- **Department**: Academic departments within colleges
- **Courses**: Course details including fees, ratings, and academic metrics

## Extending the System

To add new recommendation factors:

1. Add the factor to the `compare_colleges` method in `recommendation_engine.py`
2. Update the factor detection logic in `chatbot_integrator.py`

To add new entity types:

1. Train the NER model with new entity examples
2. Add entity handling in the `map_intent_to_sql` method
