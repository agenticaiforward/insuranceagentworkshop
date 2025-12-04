"""
Tools for the insurance agent.
These are functions the agent can call autonomously.
"""

from langchain.tools import tool

@tool
def calculate_auto_premium(
    age: int,
    vehicle_year: int,
    years_licensed: int,
    accidents: int = 0,
    violations: int = 0
) -> dict:
    """
    Calculate auto insurance premium based on driver profile.
    
    Args:
        age: Driver's age
        vehicle_year: Year vehicle was manufactured
        years_licensed: Years driver has been licensed
        accidents: Number of accidents in last 3 years
        violations: Number of violations in last 3 years
    
    Returns:
        dict: Premium breakdown with monthly/annual costs
    """
    
    base_rate = 800
    
    # Age factor
    if age < 25:
        age_factor = 400
    elif age < 30:
        age_factor = 200
    else:
        age_factor = 0
    
    # Experience discount
    experience_factor = -100 if years_licensed > 10 else 0
    
    # Accident/violation surcharges
    accident_factor = accidents * 300
    violation_factor = violations * 200
    
    # Vehicle age factor
    vehicle_age = 2025 - vehicle_year
    if vehicle_age < 5:
        vehicle_factor = 100  # Newer cars cost more
    elif vehicle_age > 15:
        vehicle_factor = -50  # Older cars cost less
    else:
        vehicle_factor = 0
    
    annual_premium = (base_rate + age_factor + experience_factor + 
                     accident_factor + violation_factor + vehicle_factor)
    monthly_premium = round(annual_premium / 12, 2)
    
    return {
        "monthly_premium": monthly_premium,
        "annual_premium": annual_premium,
        "breakdown": {
            "base_rate": base_rate,
            "age_adjustment": age_factor,
            "experience_discount": experience_factor,
            "accident_surcharge": accident_factor,
            "violation_surcharge": violation_factor,
            "vehicle_age_factor": vehicle_factor
        }
    }


@tool
def calculate_home_premium(
    year_built: int,
    square_footage: int,
    construction_type: str,
    dwelling_coverage: int
) -> dict:
    """
    Calculate home insurance premium.
    
    Args:
        year_built: Year home was built
        square_footage: Total square footage
        construction_type: Type of construction (frame, masonry, etc.)
        dwelling_coverage: Desired dwelling coverage amount
    
    Returns:
        dict: Premium breakdown
    """
    
    # Base rate: $0.50 per $1000 of coverage
    base_rate = (dwelling_coverage / 1000) * 0.50
    
    # Age factor
    home_age = 2025 - year_built
    if home_age < 10:
        age_factor = -50  # Newer homes get discount
    elif home_age > 50:
        age_factor = 200  # Older homes cost more
    else:
        age_factor = 0
    
    # Size factor
    if square_footage > 3000:
        size_factor = 150
    elif square_footage < 1500:
        size_factor = -50
    else:
        size_factor = 0
    
    # Construction type factor
    construction_factors = {
        "masonry": -100,  # Brick/stone is safer
        "frame": 0,       # Wood frame is standard
        "mobile": 200     # Mobile homes cost more
    }
    construction_factor = construction_factors.get(construction_type.lower(), 0)
    
    annual_premium = base_rate + age_factor + size_factor + construction_factor
    monthly_premium = round(annual_premium / 12, 2)
    
    return {
        "monthly_premium": monthly_premium,
        "annual_premium": annual_premium,
        "breakdown": {
            "base_rate": base_rate,
            "age_adjustment": age_factor,
            "size_adjustment": size_factor,
            "construction_adjustment": construction_factor
        }
    }


# Test the tools
if __name__ == "__main__":
    print("Testing Auto Premium Calculator:")
    auto_result = calculate_auto_premium.invoke({
        "age": 28,
        "vehicle_year": 2020,
        "years_licensed": 10,
        "accidents": 0,
        "violations": 0
    })
    print(f"Monthly: ${auto_result['monthly_premium']}")
    print(f"Annual: ${auto_result['annual_premium']}")
    print(f"Breakdown: {auto_result['breakdown']}")
    
    print("\nTesting Home Premium Calculator:")
    home_result = calculate_home_premium.invoke({
        "year_built": 2015,
        "square_footage": 2000,
        "construction_type": "frame",
        "dwelling_coverage": 300000
    })
    print(f"Monthly: ${home_result['monthly_premium']}")
    print(f"Annual: ${home_result['annual_premium']}")
    print(f"Breakdown: {home_result['breakdown']}")
