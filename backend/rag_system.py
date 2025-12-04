"""
RAG System for Insurance Knowledge Base
Uses Chroma DB (local) + Gemini Embeddings (FREE)
"""

import os
from typing import List
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini embeddings (FREE!)
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Initialize Chroma vector store (local, FREE!)
vectorstore = Chroma(
    persist_directory="./insurance_knowledge_db",
    embedding_function=embeddings,
    collection_name="insurance_docs"
)

# Insurance knowledge base
INSURANCE_KNOWLEDGE = [
    {
        "content": """Auto Insurance Coverage Types:
        
1. Liability Coverage: Pays for damages you cause to others
   - Bodily Injury: Medical expenses for injured parties
   - Property Damage: Repairs to other vehicles/property
   - Minimum limits vary by state (e.g., 50/100/50)

2. Collision Coverage: Pays for damage to YOUR vehicle in accidents
   - Covers accidents with other vehicles or objects
   - Subject to deductible ($250, $500, $1000, etc.)
   
3. Comprehensive Coverage: Pays for non-collision damage
   - Theft, vandalism, weather, fire, animal strikes
   - Also subject to deductible
   
4. Uninsured/Underinsured Motorist: Protects you if hit by uninsured driver
   - Covers medical bills and vehicle damage
   - Highly recommended in all states""",
        "metadata": {"type": "auto", "topic": "coverage_types"}
    },
    {
        "content": """Factors Affecting Auto Insurance Rates:

1. Driver Age: Younger drivers (under 25) pay more due to higher risk
2. Driving Record: Accidents and violations increase premiums significantly
3. Vehicle Age & Type: Newer, expensive cars cost more to insure
4. Location: Urban areas typically have higher rates than rural
5. Credit Score: Better credit often means lower premiums
6. Coverage Limits: Higher limits = higher premiums
7. Deductible: Higher deductible = lower premium
8. Annual Mileage: More miles driven = higher risk
9. Safety Features: Anti-theft, airbags can reduce costs""",
        "metadata": {"type": "auto", "topic": "rate_factors"}
    },
    {
        "content": """Home Insurance Coverage Explained:

1. Dwelling Coverage: Rebuilds/repairs your home structure
   - Covers walls, roof, built-in appliances
   - Should equal replacement cost, not market value
   
2. Personal Property: Covers belongings inside home
   - Furniture, electronics, clothing, etc.
   - Typically 50-70% of dwelling coverage
   - Consider replacement cost vs actual cash value
   
3. Liability Protection: Protects if someone injured on property
   - Medical bills, legal fees
   - Minimum $300,000 recommended
   
4. Additional Living Expenses (ALE): Pays for temporary housing
   - If home uninhabitable due to covered event
   - Hotels, meals, etc.
   
5. Other Structures: Covers detached garage, shed, fence""",
        "metadata": {"type": "home", "topic": "coverage_types"}
    },
    {
        "content": """Home Insurance Discounts:

1. Security System: 5-20% discount for monitored alarm
2. Fire/Smoke Alarms: 5-10% discount
3. Multi-Policy: Bundle home + auto for 15-25% savings
4. New Home: Homes under 10 years old get discounts
5. Claims-Free: No claims for 3-5 years = discount
6. Roof Age: New roof (under 10 years) = lower premium
7. Impact-Resistant Roof: Special shingles = discount
8. Gated Community: Reduced theft risk = discount
9. Non-Smoker: Lower fire risk = discount""",
        "metadata": {"type": "home", "topic": "discounts"}
    },
    {
        "content": """Common Insurance Myths Debunked:

MYTH: Red cars cost more to insure
FACT: Color doesn't affect rates - make, model, and age do

MYTH: Comprehensive coverage covers everything
FACT: It only covers non-collision damage (theft, weather, etc.)

MYTH: Your credit score doesn't matter
FACT: Most insurers use credit-based insurance scores

MYTH: Minimum coverage is enough
FACT: State minimums often too low - consider higher limits

MYTH: Older cars don't need full coverage
FACT: Depends on value - if paid off and low value, maybe drop collision/comprehensive

MYTH: Home insurance covers floods
FACT: Flood insurance is separate - not covered by standard policy""",
        "metadata": {"type": "general", "topic": "myths"}
    },
    {
        "content": """When to File an Insurance Claim:

DO FILE for:
- Major accidents with significant damage
- Injuries to yourself or others
- Damage from natural disasters
- Theft or vandalism
- Liability claims from third parties

DON'T FILE for:
- Minor damage under your deductible
- Small claims that barely exceed deductible
- Preventable maintenance issues

WHY: Multiple claims can increase your rates significantly. If damage costs only slightly more than deductible, consider paying out of pocket to avoid rate increases.""",
        "metadata": {"type": "general", "topic": "claims"}
    }
]

def initialize_knowledge_base():
    """Initialize the vector store with insurance knowledge"""
    # Check if already initialized
    try:
        existing_docs = vectorstore.get()
        if existing_docs and len(existing_docs.get('ids', [])) > 0:
            print(f"✅ Knowledge base already initialized with {len(existing_docs['ids'])} documents")
            return vectorstore
    except:
        pass
    
    # Create documents
    documents = [
        Document(
            page_content=item["content"],
            metadata=item["metadata"]
        )
        for item in INSURANCE_KNOWLEDGE
    ]
    
    # Add to vector store
    vectorstore.add_documents(documents)
    print(f"✅ Initialized knowledge base with {len(documents)} documents")
    
    return vectorstore

def search_knowledge(query: str, k: int = 3, filter_type: str = None) -> List[Document]:
    """
    Search the knowledge base for relevant information
    
    Args:
        query: Search query
        k: Number of results to return
        filter_type: Optional filter by type ('auto', 'home', 'general')
    
    Returns:
        List of relevant documents
    """
    filter_dict = {"type": filter_type} if filter_type else None
    
    results = vectorstore.similarity_search(
        query,
        k=k,
        filter=filter_dict
    )
    
    return results

def get_relevant_context(query: str, insurance_type: str = None) -> str:
    """
    Get relevant context for a query as a formatted string
    
    Args:
        query: User's question
        insurance_type: 'auto' or 'home' to filter results
    
    Returns:
        Formatted context string
    """
    results = search_knowledge(query, k=2, filter_type=insurance_type)
    
    if not results:
        return "No relevant information found."
    
    context_parts = []
    for i, doc in enumerate(results, 1):
        context_parts.append(f"**Reference {i}:**\n{doc.page_content}\n")
    
    return "\n".join(context_parts)

# Initialize on import
try:
    initialize_knowledge_base()
except Exception as e:
    print(f"⚠️  Warning: Could not initialize knowledge base: {e}")
    print("   Make sure GEMINI_API_KEY is set in .env file")
