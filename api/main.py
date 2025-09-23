#!/usr/bin/env python
# encoding: utf-8

import sys
import os
from decimal import Decimal
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException

app = FastAPI()

def convert_to_serializable(obj):
    """Converte objetos InformationItem para formato serializável"""
    if hasattr(obj, 'value') and hasattr(obj, 'title'):
        return {
            'title': obj.title,
            'value': float(obj.value) if isinstance(obj.value, Decimal) else obj.value,
            'tooltip': getattr(obj, 'tooltip', '')
        }
    elif isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

@app.get("/")
def root():
    """Endpoint raiz"""
    return {
        "message": "Fundamentus API",
        "status": "online",
        "version": "1.0.0",
        "endpoints": {
            "/": "Informações da API",
            "/health": "Status de saúde",
            "/stock/{symbol}": "Dados de ações brasileiras"
        }
    }

@app.get("/health")
def health():
    """Endpoint de saúde"""
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "service": "fundamentus-api"
    }

@app.get("/stock/{symbol}")
def get_stock_data(symbol: str):
    """Obter dados fundamentalistas de uma ação"""
    try:
        # Import fundamentus localmente para evitar problemas de inicialização
        import fundamentus
        
        # Executar pipeline
        pipeline = fundamentus.Pipeline(symbol.upper())
        response = pipeline.get_all_information()
        
        # Extrair dados
        transformed = response.transformed_information
        
        result = {
            "ticker": symbol.upper(),
            "extraction_date": datetime.now().strftime("%Y-%m-%d"),
            "status": "success"
        }
        
        # Adicionar seções de dados se disponíveis
        sections = [
            'price_information',
            'detailed_information', 
            'oscillations',
            'valuation_indicators',
            'profitability_indicators',
            'indebtedness_indicators',
            'balance_sheet',
            'income_statement'
        ]
        
        for section in sections:
            if section in transformed:
                result[section] = convert_to_serializable(transformed[section])
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=404, 
            detail={
                "error": "Erro ao obter dados da ação",
                "symbol": symbol.upper(),
                "message": str(e)
            }
        )
