<template>
    <div class="welcome-screen d-flex justify-content-center align-items-center vh-100">
      <div class="card p-4 shadow-sm" style="max-width: 400px; width: 100%;">
        <h1 class="text-primary text-center">Bem-vindo!</h1>
        <p class="text-center">Nos diga seu nome para começar.</p>
        <form @submit.prevent="startSession">
          <div class="mb-3">
            <input
              v-model="name"
              type="text"
              class="form-control"
              placeholder="Digite seu nome"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary w-100">Começar</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import api from "../api";
  
  export default {
    data() {
      return {
        name: "",
      };
    },
    methods: {
      async startSession() {
        try {
          const response = await api.post("/session/create/", { name: this.name });
          const { link } = response.data;
          this.$router.push(`/questionnaire?session=${link}`);
        } catch (error) {
          console.error("Erro ao iniciar a sessão:", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .welcome-screen {
    background-color: #f8f9fa; /* Fundo leve e agradável */
  }
  </style>
  