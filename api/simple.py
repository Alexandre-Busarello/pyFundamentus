#!/usr/bin/env python
# encoding: utf-8

"""
Versão simplificada da API para teste na Vercel
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Fundamentus API - Simple Version",
    description="API para acessar dados fundamentalistas de ações brasileiras",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Fundamentus API - Simple Version",
        "description": "API para acessar dados fundamentalistas de ações brasileiras",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "/stock/{symbol}": "Obter dados de uma ação específica",
            "/docs": "Documentação interativa da API"
        }
    }

@app.get("/test")
async def test():
    """Test endpoint"""
    return {"status": "API funcionando!", "timestamp": "2025-09-23"}

@app.get("/stock/{symbol}")
async def get_stock_simple(symbol: str):
    """Get stock data - simplified version for testing"""
    return {
        "ticker": symbol.upper(),
        "message": "Endpoint funcionando! Implementação completa em desenvolvimento.",
        "status": "test_mode"
    }

# Handler para Vercel
handler = app
