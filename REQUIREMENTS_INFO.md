# 📦 Arquivos de Dependências

Este projeto possui diferentes arquivos de requirements para diferentes ambientes:

## 📋 Arquivos Disponíveis

### `requirements.txt` - **PRODUÇÃO (Vercel)**
```txt
fastapi==0.82.0
uvicorn==0.18.3
beautifulsoup4==4.11.1
requests==2.28.1
requests-cache==0.9.6
lxml==4.9.2
pydantic==1.10.2
starlette==0.19.1
```

**Uso:** Deploy na Vercel e produção
- ✅ Apenas dependências essenciais
- ✅ Versões fixas para estabilidade
- ✅ Otimizado para serverless

### `requirements-dev.txt` - **DESENVOLVIMENTO**
Contém todas as dependências de desenvolvimento incluindo:
- Ferramentas de teste (pytest, coverage)
- Linters (pylint, pre-commit)
- Ferramentas de build (poetry, twine)
- Documentação (rich, textual)

**Uso:** Desenvolvimento local
```bash
pip install -r requirements-dev.txt
```

### `requirements-production.txt` - **BACKUP**
Backup do requirements.txt anterior (versões flexíveis)

## 🚀 Para Deploy na Vercel

**Use sempre `requirements.txt`** - Este arquivo é otimizado para:
- ⚡ Build rápido
- 📦 Tamanho mínimo
- 🔒 Versões estáveis
- 🌐 Compatibilidade serverless

## 🛠️ Para Desenvolvimento Local

**Use `requirements-dev.txt`** para ter acesso a:
- 🧪 Ferramentas de teste
- 📝 Linters e formatadores
- 📚 Ferramentas de documentação
- 🔧 Utilitários de desenvolvimento

## ⚠️ Importante

**Nunca** use `requirements-dev.txt` na Vercel pois:
- ❌ Muitas dependências desnecessárias
- ❌ Build lento
- ❌ Possíveis conflitos de versão
- ❌ Tamanho excessivo da função
