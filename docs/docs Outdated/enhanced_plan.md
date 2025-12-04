# Enhanced Insurance Quote Forms - Implementation Plan

## Goal Description
Transform the basic quote form into realistic Auto and Home insurance quote forms with comprehensive fields needed for accurate premium calculations. This demonstrates the "Agentic AI" capability to handle complex, domain-specific data collection.

## User Review Required
> [!NOTE]
> I'm adding comprehensive fields for Auto (vehicle details, driver info, coverage options) and Home (property details, construction, coverage limits) insurance. The backend will use more realistic calculation logic.

## Proposed Changes

### Frontend Components

#### [NEW] [InsuranceTypeSelector.jsx](file:///C:/Users/Naveen%20Nalajala/.gemini/antigravity/scratch/insurance_agent/frontend/src/components/InsuranceTypeSelector.jsx)
- Component to select between Auto and Home insurance before showing the quote form
- Clean card-based UI with icons

#### [MODIFY] [QuoteForm.jsx](file:///C:/Users/Naveen%20Nalajala/.gemini/antigravity/scratch/insurance_agent/frontend/src/components/QuoteForm.jsx)
- Split into `AutoInsuranceForm.jsx` and `HomeInsuranceForm.jsx`
- **Auto Insurance Fields**:
  - Personal: Name, Age, Zip Code
  - Vehicle: Year, Make, Model, VIN (optional)
  - Coverage: Liability limits, Collision, Comprehensive, Deductible
  - Driver History: Years licensed, Accidents, Violations
- **Home Insurance Fields**:
  - Property: Address, Zip Code, Year Built, Square Footage
  - Construction: Type (Frame/Brick/Stone), Roof Type, Stories
  - Coverage: Dwelling, Personal Property, Liability
  - Features: Security system, Fire alarm, Pool

#### [MODIFY] [App.jsx](file:///C:/Users/Naveen%20Nalajala/.gemini/antigravity/scratch/insurance_agent/frontend/src/App.jsx)
- Add insurance type selection flow
- Route to appropriate form based on selection

### Backend Updates

#### [MODIFY] [main.py](file:///C:/Users/Naveen%20Nalajala/.gemini/antigravity/scratch/insurance_agent/backend/main.py)
- Update `/api/quote` endpoint to accept insurance type
- Implement realistic calculation formulas:
  - **Auto**: Base rate + age factor + vehicle value + coverage selections + driver history
  - **Home**: Base rate + property value + construction type + coverage limits + risk factors
- Return detailed breakdown of premium components

## Verification Plan

### Manual Verification
1. Test Auto insurance flow with various vehicle types and coverage options
2. Test Home insurance flow with different property characteristics
3. Verify premium calculations are reasonable and consistent
4. Browser agent verification of complete flows
