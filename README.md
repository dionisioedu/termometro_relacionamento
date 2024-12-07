# Termômetro de Relacionamentos

O **Termômetro de Relacionamentos** é uma aplicação web interativa para ajudar casais a avaliarem a saúde do relacionamento, baseando-se em perguntas personalizadas e análises psicológicas. A aplicação foi desenvolvida utilizando **Django** no backend e **Vue.js** no frontend.

---

## **Índice**
- [Visão Geral](#visão-geral)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Como Configurar e Rodar o Projeto](#como-configurar-e-rodar-o-projeto)
  - [Requisitos](#requisitos)
  - [Passos](#passos)
- [Funcionalidades](#funcionalidades)
- [Contribuições](#contribuições)
- [Licença](#licença)

---

## **Visão Geral**

Este projeto oferece uma experiência simples e prática para casais identificarem áreas de melhoria em seus relacionamentos. O sistema é baseado em perguntas categorizadas que permitem traçar perfis individuais e combinados.

---

## **Tecnologias Utilizadas**

### Backend:
- **Django**: Framework web em Python para gerenciar a lógica de negócios e APIs.
- **Django REST Framework**: Para criar endpoints RESTful.
- **SQLite**: Banco de dados local para desenvolvimento (PostgreSQL será usado em produção).
- **Docker**: Para containerização do ambiente.

### Frontend:
- **Vue.js**: Framework JavaScript para construção da interface do usuário.
- **Axios**: Para consumo de APIs REST.
- **Tailwind CSS** (ou similar): Para estilização (planejado).

---

## **Como Configurar e Rodar o Projeto**

### Requisitos:
- **Docker** e **Docker Compose** instalados na máquina.
- Acesso ao repositório via SSH configurado.

### Passos:
1. **Clone o repositório**:
   ```bash
   git clone git@github.com:dionisioedu/termometro_relacionamento.git
   cd termometro_relacionamento
