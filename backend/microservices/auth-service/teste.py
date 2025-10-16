# test.py - Para testar se as dependências funcionam
try:
    from fastapi import FastAPI
    from pydantic import BaseModel
    import jwt
    print("✅ Todas as dependências instaladas corretamente!")
    print("✅ FastAPI funcionando")
    print("✅ Pydantic funcionando") 
    print("✅ JWT funcionando")
except ImportError as e:
    print(f"❌ Erro: {e}")