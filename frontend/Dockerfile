# Usar uma imagem base do Node.js
FROM node:18

# Diretório de trabalho
WORKDIR /app

# Copiar arquivos essenciais para o build
COPY package.json package-lock.json ./

# Resolver problemas de dependências e instalar pacotes
RUN npm install --legacy-peer-deps \
    && npm install terser-webpack-plugin@^5.1.4 schema-utils@^3.1.1 --save-dev \
    && npm audit fix --force

# Copiar o restante do projeto
COPY . .

# Compilar os arquivos estáticos para produção
RUN npm run build

# Instalar o servidor para servir arquivos estáticos
RUN npm install -g serve

# Comando para iniciar o servidor de arquivos estáticos
CMD ["serve", "-s", "dist"]
