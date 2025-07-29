# Amar Assist Training API - Backend

API backend para o Sistema de Treinamento de Vendas da Amar Assist.

## 🚀 Deploy Rápido

### Heroku
```bash
# Instalar Heroku CLI
# Fazer login: heroku login

# Criar app
heroku create amar-assist-api

# Deploy
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a amar-assist-api
git push heroku main
```

### Railway
```bash
# Instalar Railway CLI
# Fazer login: railway login

# Deploy
railway deploy
```

## 📋 Endpoints da API

### Health Check
- `GET /api/health` - Status da API

### Usuários
- `GET /api/users` - Listar usuários
- `GET /api/users/{id}` - Detalhes do usuário
- `GET /api/users/{id}/progress` - Progresso do usuário

### Módulos
- `GET /api/modules` - Listar módulos
- `GET /api/modules/{id}` - Detalhes do módulo
- `GET /api/modules/{id}/lessons/{lesson_id}` - Conteúdo da lição

### Quizzes
- `POST /api/quiz/{id}/start` - Iniciar quiz
- `POST /api/quiz/attempt/{id}/answer` - Submeter resposta
- `POST /api/quiz/attempt/{id}/complete` - Finalizar quiz

### Upload
- `POST /api/upload/batch` - Upload de arquivos

## ⚙️ Configuração Local

```bash
# Clonar repositório
git clone <repo-url>
cd amar_assist_api

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar
python src/main.py
```

## 🔧 Variáveis de Ambiente

```bash
# Desenvolvimento
export FLASK_ENV=development
export SECRET_KEY=your-secret-key

# Produção
export FLASK_ENV=production
export DATABASE_URL=postgresql://...
```

## 🗄️ Banco de Dados

- **Desenvolvimento:** SQLite (automático)
- **Produção:** PostgreSQL (recomendado)

### Migração para PostgreSQL
```bash
pip install psycopg2-binary
export DATABASE_URL=postgresql://user:pass@host:port/db
```

## 🔒 CORS

A API está configurada para aceitar requisições de qualquer origem:
```python
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
```

Para produção, configure origens específicas:
```python
CORS(app, origins=["https://seu-frontend.netlify.app"])
```

## 📁 Estrutura

```
amar_assist_api/
├── src/
│   ├── main.py              # Aplicação principal
│   ├── models/              # Modelos SQLAlchemy
│   ├── routes/              # Blueprints da API
│   ├── utils/               # Utilitários
│   └── database/            # Banco SQLite
├── requirements.txt         # Dependências
├── Procfile                # Configuração Heroku
├── runtime.txt             # Versão Python
└── README.md               # Este arquivo
```

## 🧪 Testes

```bash
# Testar health check
curl http://localhost:5000/api/health

# Testar módulos
curl http://localhost:5000/api/modules
```

## 🚀 Deploy em Produção

### 1. Heroku (Recomendado)
- Suporte nativo para Python
- PostgreSQL gratuito
- SSL automático
- Fácil configuração

### 2. Railway
- Deploy automático via Git
- PostgreSQL incluído
- Interface moderna

### 3. DigitalOcean App Platform
- Escalabilidade automática
- Múltiplas regiões
- Monitoramento integrado

## 🔧 Troubleshooting

### Erro de CORS
```python
# Verificar configuração CORS
CORS(app, origins=["https://seu-frontend.com"])
```

### Erro de Banco
```bash
# Verificar URL do banco
echo $DATABASE_URL

# Recriar tabelas
python -c "from src.main import app, db; app.app_context().push(); db.create_all()"
```

### Erro de Dependências
```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

## 📞 Suporte

- Logs do Heroku: `heroku logs --tail`
- Logs do Railway: `railway logs`
- Debug local: `FLASK_DEBUG=1 python src/main.py`

---

**Desenvolvido por:** Manus AI  
**Cliente:** Amar Assist  
**Versão:** 1.0 - API Backend

