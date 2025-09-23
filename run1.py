import fundamentus
import json
from decimal import Decimal

main_pipeline = fundamentus.Pipeline('WEGE3')
response = main_pipeline.get_all_information()

# Extract the information from the response.
price_information = response.transformed_information['price_information']
detailed_information = response.transformed_information['detailed_information']
oscillations = response.transformed_information['oscillations']
valuation_indicators = response.transformed_information['valuation_indicators']
profitability_indicators = response.transformed_information['profitability_indicators']
indebtedness_indicators = response.transformed_information['indebtedness_indicators']
balance_sheet = response.transformed_information['balance_sheet']
income_statement = response.transformed_information['income_statement']

def convert_to_json_serializable(obj):
    """Convert InformationItem objects and other non-serializable types to JSON-serializable format"""
    if hasattr(obj, 'value') and hasattr(obj, 'title') and hasattr(obj, 'tooltip'):
        # It's an InformationItem object
        return {
            'title': obj.title,
            'value': float(obj.value) if isinstance(obj.value, Decimal) else obj.value,
            'tooltip': obj.tooltip
        }
    elif isinstance(obj, dict):
        return {key: convert_to_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

# Convert all data to JSON-serializable format
wege3_data = {
    "ticker": "WEGE3",
    "extraction_date": "2025-09-23",
    "price_information": convert_to_json_serializable(price_information),
    "detailed_information": convert_to_json_serializable(detailed_information),
    "oscillations": convert_to_json_serializable(oscillations),
    "valuation_indicators": convert_to_json_serializable(valuation_indicators),
    "profitability_indicators": convert_to_json_serializable(profitability_indicators),
    "indebtedness_indicators": convert_to_json_serializable(indebtedness_indicators),
    "balance_sheet": convert_to_json_serializable(balance_sheet),
    "income_statement": convert_to_json_serializable(income_statement)
}

# Print the JSON with proper formatting
print(json.dumps(wege3_data, indent=2, ensure_ascii=False))