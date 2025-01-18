<template>
  <div class="questionnaire-screen d-flex justify-content-center align-items-center vh-100">
    <div class="card p-4 shadow-sm" style="max-width: 600px; width: 100%;">
      <h1 class="text-primary text-center">Sessão Derivada</h1>
      <h2 class="text-center">Bem-vindo ao Amorfy!</h2>

      <!-- Carregando -->
      <div v-if="loading" class="text-center">
        <p class="text-muted">Carregando sessão derivada...</p>
      </div>

      <!-- Erro -->
      <div v-else-if="errorMessage" class="alert alert-danger">
        <p>{{ errorMessage }}</p>
      </div>

      <!-- Conteúdo principal -->
      <div v-else>
        <p class="text-center">
          Você foi convidado por <strong>{{ originCreatorName }}</strong> para participar desta sessão.
        </p>
        <p class="text-center">Clique no botão abaixo para começar o questionário:</p>

        <!-- Botão -->
        <button 
          class="btn btn-primary w-100 mt-4"
          @click="startQuestionnaire"
        >
          Começar Questionário
        </button>
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
      errorMessage: null,
      derivedSessionId: null,
      originCreatorName: null, // Nome do criador da sessão original
    };
  },
  async created() {
    try {
      // Chamar a API para criar a sessão derivada
      const response = await api.get(`/session/${this.sessionId}/derived_session/`);
      this.derivedSessionId = response.data.derived_session_id;
      this.originCreatorName = response.data.origin_creator_name;

      console.log("Sessão derivada criada com sucesso:", response.data);

      this.loading = false;
    } catch (error) {
      console.error("Erro ao carregar sessão derivada:", error);
      this.errorMessage = error.response?.data?.error || "Erro desconhecido ao criar sessão derivada.";
      this.loading = false;
    }
  },
  methods: {
    startQuestionnaire() {
      this.$router.push({
        name: "UserQuestionnaire",
        params: { sessionId: this.derivedSessionId },
      });
    },
  },
};
</script>

<style scoped>
.questionnaire-screen {
  background-color: #f8f9fa; /* Fundo leve */
}
</style>
