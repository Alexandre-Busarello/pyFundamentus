# 🚀 Deploy da API Fundamentus na Vercel

Este guia explica como fazer o deploy da API FastAPI (`run_fastapi.py`) na plataforma Vercel.

## 📋 Pré-requisitos

- Conta na [Vercel](https://vercel.com)
- Repositório Git (GitHub, GitLab, ou Bitbucket)
- Node.js instalado localmente (para CLI da Vercel)

## 🔧 Preparação do Projeto

### 1. Criar arquivo `vercel.json`

Crie o arquivo de configuração da Vercel na raiz do projeto:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "run_fastapi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "run_fastapi.py"
    }
  ]
}
```

### 2. Criar arquivo `requirements.txt`

Se não existir, crie o arquivo com as dependências:

```txt
fastapi
uvicorn[standard]
beautifulsoup4
requests
lxml
```

### 3. Modificar o arquivo principal

Crie um arquivo `api/index.py` (estrutura recomendada pela Vercel):

```python
#!/usr/bin/env python
# encoding: utf-8

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
```

## 📁 Estrutura de Arquivos Recomendada

```
pyFundamentus/
├── api/
│   └── index.py          # Arquivo principal da API
├── fundamentus/          # Biblioteca fundamentus
├── vercel.json          # Configuração da Vercel
├── requirements.txt     # Dependências Python
└── README.md
```

## 🚀 Métodos de Deploy

### Método 1: Deploy via GitHub (Recomendado)

1. **Conectar repositório à Vercel:**
   - Acesse [vercel.com](https://vercel.com)
   - Faça login e clique em "New Project"
   - Conecte sua conta do GitHub
   - Selecione o repositório `pyFundamentus`

2. **Configurar o projeto:**
   - Framework Preset: `Other`
   - Root Directory: `./` (raiz do projeto)
   - Build Command: (deixe vazio)
   - Output Directory: (deixe vazio)
   - Install Command: `pip install -r requirements.txt`

3. **Deploy automático:**
   - A Vercel fará o deploy automaticamente
   - Cada push para a branch main acionará um novo deploy

### Método 2: Deploy via CLI da Vercel

1. **Instalar CLI da Vercel:**
   ```bash
   npm install -g vercel
   ```

2. **Login na Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy do projeto:**
   ```bash
   cd /home/busamar/projetos/pyFundamentus
   vercel
   ```

4. **Seguir as instruções:**
   - Set up and deploy? `Y`
   - Which scope? (selecione sua conta)
   - Link to existing project? `N`
   - Project name: `pyfundamentus-api`
   - In which directory is your code located? `./`

## 🔧 Configurações Avançadas

### Variáveis de Ambiente

Se necessário, adicione variáveis de ambiente no dashboard da Vercel:
- Acesse o projeto na Vercel
- Vá em Settings > Environment Variables
- Adicione as variáveis necessárias

### Configuração de Domínio Customizado

1. No dashboard da Vercel, vá em Settings > Domains
2. Adicione seu domínio customizado
3. Configure os DNS conforme instruções

### Monitoramento e Logs

- Acesse Functions > View Function Logs para ver logs em tempo real
- Use o Analytics para monitorar performance
- Configure alertas em Settings > Notifications

## 📊 Testando a API

Após o deploy, sua API estará disponível em:
```
https://seu-projeto.vercel.app
```

### Endpoints disponíveis:

- **GET /** - Informações da API
- **GET /stock/{symbol}** - Dados de uma ação específica
- **GET /docs** - Documentação interativa (Swagger UI)

### Exemplos de uso:

```bash
# Informações da API
curl https://seu-projeto.vercel.app/

# Dados da WEGE3
curl https://seu-projeto.vercel.app/stock/WEGE3

# Dados da PETR4
curl https://seu-projeto.vercel.app/stock/PETR4
```

## ⚠️ Limitações da Vercel

- **Timeout:** 10 segundos para Hobby plan, 60s para Pro
- **Tamanho:** Máximo 50MB por função
- **Memória:** 1024MB para Hobby plan
- **Execuções:** 100GB-hours/mês para Hobby plan

## 🐛 Troubleshooting

### Erro de timeout
Se a API demorar mais que 10 segundos:
- Otimize o código da biblioteca fundamentus
- Considere usar cache para dados frequentes
- Upgrade para plano Pro (60s timeout)

### Erro de dependências
Se houver problemas com dependências:
- Verifique se todas estão no `requirements.txt`
- Use versões específicas das dependências
- Teste localmente antes do deploy

### Erro de importação
Se houver erro ao importar a biblioteca fundamentus:
- Verifique se a estrutura de pastas está correta
- Confirme que `__init__.py` existe em todas as pastas
- Use imports relativos quando necessário

## 📝 Comandos Úteis

```bash
# Deploy local
vercel dev

# Deploy para produção
vercel --prod

# Ver logs
vercel logs

# Listar deployments
vercel ls

# Remover projeto
vercel remove
```

## 🎯 Próximos Passos

1. Configure monitoramento de uptime
2. Implemente cache para melhor performance
3. Adicione rate limiting para evitar abuso
4. Configure CORS se necessário
5. Adicione autenticação se for API privada

---

**🚀 Sua API Fundamentus estará online e acessível globalmente via Vercel!**
