# Dockerfile (frontend)
FROM node:18

WORKDIR /app

# Copiar os arquivos necessários para instalar dependências
COPY package.json yarn.lock ./

# Instalar dependências com Yarn
RUN yarn install && yarn add bootstrap @popperjs/core @vue/cli @vue/compiler-sfc

# Copiar todo o código do frontend
COPY . .

# Executar o servidor de desenvolvimento
CMD ["yarn", "serve"]
