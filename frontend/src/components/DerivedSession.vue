<template>
  <div class="questionnaire-screen d-flex justify-content-center align-items-center vh-100">
    <div class="card p-4 shadow-sm" style="max-width: 600px; width: 100%;">
      <h1 class="text-primary text-center">Sessão Derivada</h1>
      <p class="text-center">
        Bem-vindo(a)! Você está participando de uma sessão derivada iniciada por
        <strong>{{ originCreatorName }}</strong>.
      </p>

      <!-- Tela de carregamento -->
      <div v-if="loading">
        <p class="text-center">Carregando sessão derivada...</p>
      </div>

      <!-- Tela com opção de iniciar o questionário -->
      <div v-else>
        <p class="text-center">Clique no botão abaixo para começar o questionário.</p>
        <button class="btn btn-primary w-100" @click="startQuestionnaire">Começar Questionário</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../api";

export default {
  props: {
    sessionId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      loading: true,
      originCreatorName: null,
    };
  },
  async created() {
    try {
      // Verificar a sessão derivada e buscar informações do criador
      const response = await api.get(`/session/${this.sessionId}/derived_session/`);
      const { session_id, derived_session_id, origin_creator_name, answers_submitted } = response.data;

      this.originCreatorName = origin_creator_name || "Desconhecido";
      console.log("Sessão derivada carregada:", response.data);

      // Verificar se o segundo ator já respondeu
      if (derived_session_id && answers_submitted) {
        console.log("Respostas já enviadas. Redirecionando para resultados...");
        this.$router.push({ name: "ResultsView", params: { sessionId: session_id } });
      } else {
        this.loading = false;
      }
    } catch (error) {
      console.error("Erro ao carregar sessão derivada:", error);
      alert("Erro ao carregar sessão derivada. Tente novamente mais tarde.");
    }
  },
  methods: {
    startQuestionnaire() {
      this.$router.push({
        name: "UserQuestionnaire",
        query: { originSessionId: this.sessionId, isDerivedSession: true, originCreatorName: this.originCreatorName },
      });
    },
  },
};
</script>

<style scoped>
.questionnaire-screen {
  background-color: #f8f9fa;
}
</style>
