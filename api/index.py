#!/usr/bin/env python
# encoding: utf-8

import sys
import os

# Adicionar o diretório raiz ao path para importar a biblioteca fundamentus
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fundamentus
import json
from decimal import Decimal
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Fundamentus API",
    description="API para acessar dados fundamentalistas de ações brasileiras",
    version="1.0.0"
)

def convert_to_json_serializable(obj):
    """Convert InformationItem objects and other non-serializable types to JSON-serializable format"""
    if hasattr(obj, 'value') and hasattr(obj, 'title') and hasattr(obj, 'tooltip'):
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

def get_stock_data(symbol: str) -> dict:
    """Get the stock data."""
    try:
        main_pipeline = fundamentus.Pipeline(symbol.upper())
        response = main_pipeline.get_all_information()

        # Extract the information from the response
        price_information = response.transformed_information['price_information']
        detailed_information = response.transformed_information['detailed_information']
        oscillations = response.transformed_information['oscillations']
        valuation_indicators = response.transformed_information['valuation_indicators']
        profitability_indicators = response.transformed_information['profitability_indicators']
        indebtedness_indicators = response.transformed_information['indebtedness_indicators']
        balance_sheet = response.transformed_information['balance_sheet']
        income_statement = response.transformed_information['income_statement']

        # Convert all data to JSON-serializable format
        stock_data = {
            "ticker": symbol.upper(),
            "extraction_date": datetime.now().strftime("%Y-%m-%d"),
            "price_information": convert_to_json_serializable(price_information),
            "detailed_information": convert_to_json_serializable(detailed_information),
            "oscillations": convert_to_json_serializable(oscillations),
            "valuation_indicators": convert_to_json_serializable(valuation_indicators),
            "profitability_indicators": convert_to_json_serializable(profitability_indicators),
            "indebtedness_indicators": convert_to_json_serializable(indebtedness_indicators),
            "balance_sheet": convert_to_json_serializable(balance_sheet),
            "income_statement": convert_to_json_serializable(income_statement)
        }

        return stock_data

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erro ao obter dados da ação {symbol}: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Fundamentus API",
        "description": "API para acessar dados fundamentalistas de ações brasileiras",
        "version": "1.0.0",
        "endpoints": {
            "/stock/{symbol}": "Obter dados de uma ação específica",
            "/docs": "Documentação interativa da API"
        }
    }

@app.get("/stock/{symbol}")
async def get_stock(symbol: str):
    """Get stock fundamental data"""
    try:
        data = get_stock_data(symbol)
        return JSONResponse(content=data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# Handler para Vercel
handler = app
