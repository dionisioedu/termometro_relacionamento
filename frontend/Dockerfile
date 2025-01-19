# Usar uma imagem base do Node.js
FROM node:18

# Definir o diretório de trabalho
WORKDIR /app

# Copiar arquivos essenciais para instalar dependências
COPY package.json package-lock.json ./

# Instalar dependências, incluindo js-cookie
RUN npm install --legacy-peer-deps \
    && npm install js-cookie --save \
    && npm install entities@latest --save \
    && npm audit fix --force

# Copiar o restante do código do projeto
COPY . .

# Construir o projeto
RUN npm run build

# Instalar o servidor para servir os arquivos estáticos
RUN npm install -g serve

# Comando para servir os arquivos estáticos
CMD ["serve", "-s", "dist"]
