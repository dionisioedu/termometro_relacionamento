# Usar a imagem oficial do Node.js
FROM node:18

# Diretório de trabalho
WORKDIR /app

# Copiar os arquivos necessários para instalar dependências
COPY package.json package-lock.json ./

# Instalar dependências com npm
RUN npm install

# Copiar todo o código do frontend
COPY . .

# Gerar build para produção
RUN npm run build

# Servir os arquivos estáticos com um servidor simples
RUN npm install -g serve

# Configurar o comando de execução
CMD ["serve", "-s", "dist"]
