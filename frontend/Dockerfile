# Usar imagem base do Node.js
FROM node:18

# Configurar o diretório de trabalho
WORKDIR /app

# Copiar arquivos essenciais para instalação de dependências
COPY package.json package-lock.json ./

# Instalar dependências e corrigir problemas com pacotes
RUN npm install --legacy-peer-deps

# Adicionar resoluções para corrigir versões problemáticas
RUN npm install schema-utils terser-webpack-plugin --save && npm audit fix --force

# Copiar todo o código do projeto para o contêiner
COPY . .

# Construir o projeto para produção
RUN npm run build

# Instalar o pacote "serve" para servir os arquivos estáticos
RUN npm install -g serve

# Comando de execução para servir os arquivos da pasta 'dist'
CMD ["serve", "-s", "dist"]
