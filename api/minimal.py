#!/usr/bin/env python
# encoding: utf-8

"""
Versão minimalista da API para máxima compatibilidade com Vercel
"""

import sys
import os
import json
from decimal import Decimal
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from fastapi import FastAPI, HTTPException
    
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {
            "message": "Fundamentus API - Minimal Version",
            "status": "online",
            "version": "1.0.0-minimal"
        }
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "timestamp": datetime.now().isoformat()}
    
    @app.get("/stock/{symbol}")
    async def get_stock_minimal(symbol: str):
        try:
            # Import fundamentus apenas quando necessário
            import fundamentus
            
            def convert_to_serializable(obj):
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
            
            # Executar pipeline
            pipeline = fundamentus.Pipeline(symbol.upper())
            response = pipeline.get_all_information()
            
            # Extrair dados essenciais
            data = {
                "ticker": symbol.upper(),
                "extraction_date": datetime.now().strftime("%Y-%m-%d"),
                "price_information": convert_to_serializable(
                    response.transformed_information.get('price_information', {})
                ),
                "valuation_indicators": convert_to_serializable(
                    response.transformed_information.get('valuation_indicators', {})
                )
            }
            
            return data
            
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Erro: {str(e)}")
    
    # Handler para Vercel
    handler = app

except ImportError:
    # Fallback se FastAPI não funcionar
    def handler(request):
        return {
            "statusCode": 200,
            "body": json.dumps({"error": "FastAPI not available", "message": "Minimal fallback"})
        }
