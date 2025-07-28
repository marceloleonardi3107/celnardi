# Sistema de Treinamento Amar Assist - Frontend Netlify

Este é o frontend do Sistema de Treinamento de Vendas da Amar Assist, adaptado para implantação no Netlify.

## 🚀 Implantação no Netlify

### Método 1: Deploy via Git (Recomendado)

1. **Faça upload do código para um repositório Git:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Amar Assist Training Frontend"
   git remote add origin https://github.com/seu-usuario/amar-assist-frontend.git
   git push -u origin main
   ```

2. **Conecte ao Netlify:**
   - Acesse [app.netlify.com](https://app.netlify.com)
   - Clique em "New site from Git"
   - Conecte sua conta GitHub/GitLab/Bitbucket
   - Selecione o repositório
   - Configure as opções de build:
     - **Build command:** `echo 'No build required'`
     - **Publish directory:** `.` (raiz)
   - Clique em "Deploy site"

### Método 2: Deploy Manual

1. **Compacte os arquivos:**
   ```bash
   zip -r amar-assist-frontend.zip . -x "*.git*" "README.md"
   ```

2. **Upload no Netlify:**
   - Acesse [app.netlify.com](https://app.netlify.com)
   - Arraste o arquivo ZIP para a área de deploy
   - Aguarde o processamento

## ⚙️ Configuração da API

### Variáveis de Ambiente

Configure as seguintes variáveis no Netlify:

1. **No painel do Netlify:**
   - Vá para Site settings > Environment variables
   - Adicione as variáveis:

```
API_BASE_URL=https://sua-api-backend.herokuapp.com/api
```

### Configuração do Backend

O frontend está configurado para se comunicar com uma API backend separada. Certifique-se de que:

1. **Backend está implantado** (Heroku, Railway, etc.)
2. **CORS está configurado** para aceitar requisições do domínio Netlify
3. **URL da API está correta** no arquivo `js/config.js`

## 📁 Estrutura de Arquivos

```
amar_assist_frontend_netlify/
├── index.html              # Página principal
├── css/
│   └── style.css           # Estilos personalizados
├── js/
│   ├── config.js           # Configuração da API
│   └── app.js              # JavaScript principal
├── uploads/
│   └── documents/          # Documentos da Amar Assist
├── netlify.toml            # Configuração do Netlify
├── _redirects              # Redirecionamentos
└── README.md               # Este arquivo
```

## 🔧 Funcionalidades

### ✅ Implementadas
- Dashboard interativo com estatísticas
- Navegação entre módulos e lições
- Sistema de quizzes (requer API)
- Upload de arquivos (requer API)
- Modo offline com cache local
- Indicador de status de conexão
- Interface responsiva

### 🔄 Dependentes da API
- Carregamento de módulos e lições
- Submissão de quizzes
- Upload de arquivos
- Sincronização de progresso

## 🌐 Configuração de Domínio Personalizado

1. **No painel do Netlify:**
   - Vá para Site settings > Domain management
   - Clique em "Add custom domain"
   - Digite seu domínio (ex: treinamento.amarassist.com.br)
   - Configure os registros DNS conforme instruções

2. **SSL Automático:**
   - O Netlify configura SSL automaticamente
   - Aguarde a propagação (pode levar até 24h)

## 🔒 Segurança

### Headers de Segurança
O arquivo `netlify.toml` inclui headers de segurança:
- X-Frame-Options
- X-XSS-Protection
- Content Security Policy
- Cache-Control

### HTTPS
- SSL/TLS automático via Let's Encrypt
- Redirecionamento HTTP → HTTPS
- HSTS (HTTP Strict Transport Security)

## 📱 Responsividade

O frontend é totalmente responsivo e funciona em:
- 📱 Dispositivos móveis (smartphones)
- 📱 Tablets
- 💻 Desktops
- 🖥️ Monitores grandes

## 🔧 Troubleshooting

### Problema: API não conecta
**Solução:**
1. Verifique se o backend está online
2. Confirme a URL da API em `js/config.js`
3. Verifique configuração CORS no backend

### Problema: Arquivos não carregam
**Solução:**
1. Verifique se todos os arquivos foram enviados
2. Confirme estrutura de pastas
3. Verifique console do navegador para erros

### Problema: Redirecionamentos não funcionam
**Solução:**
1. Verifique arquivo `_redirects`
2. Confirme configuração em `netlify.toml`
3. Teste em modo incógnito

## 📞 Suporte

Para suporte técnico:
- Verifique logs no painel do Netlify
- Consulte documentação oficial: [docs.netlify.com](https://docs.netlify.com)
- Entre em contato com a equipe de desenvolvimento

## 🚀 Próximos Passos

1. **Configurar backend API** em serviço separado
2. **Testar integração** frontend-backend
3. **Configurar domínio personalizado**
4. **Implementar analytics** (Google Analytics, etc.)
5. **Configurar monitoramento** de uptime

---

**Desenvolvido por:** Manus AI  
**Cliente:** Amar Assist  
**Versão:** 1.0 - Netlify Ready

