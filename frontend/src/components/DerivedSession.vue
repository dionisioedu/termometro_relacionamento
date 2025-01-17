<template>
    <div class="derived-session-screen">
      <h1>Bem-vindo à Sessão Derivada!</h1>
      <p>Sessão de origem: {{ originSessionId }}</p>
      <form @submit.prevent="startQuestionnaire">
        <input v-model="name" placeholder="Seu nome" required />
        <button type="submit" class="btn btn-primary mt-3">Começar</button>
      </form>
    </div>
  </template>
  
  <script>
  import api from '../api';
  
  export default {
    props: {
      sessionId: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        name: '',
        originSessionId: null,
      };
    },
    async created() {
      try {
        const response = await api.get(`/session/${this.sessionId}/derived_session/`);
        this.originSessionId = response.data.origin_session_id;
      } catch (error) {
        console.error('Erro ao carregar sessão derivada:', error);
      }
    },
    methods: {
      startQuestionnaire() {
        console.log('Iniciando questionário para:', this.name);
        this.$emit('start-questions', this.sessionId, this.name);
      },
    },
  };
  </script>
  
  <style scoped>
  .derived-session-screen {
    text-align: center;
    padding: 20px;
  }
  </style>
  