<template>
  <div class="answers-screen container mt-5">
    <h1 class="text-primary text-center">Respostas da Sessão</h1>

    <!-- Exibe as respostas -->
    <div v-if="answers.length > 0">
      <table class="table table-bordered mt-4">
        <thead class="table-light">
          <tr>
            <th scope="col">Pergunta</th>
            <th scope="col">Resposta</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="answer in answers" :key="answer.question">
            <td>{{ answer.question }}</td>
            <td>{{ answer.response }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Botão para voltar -->
      <div class="text-center mt-4">
        <p>
          Compartilhe este link com seu parceiro(a):
          <strong class="text-break">{{ sessionLink + "/derived_session/" }}</strong>
        </p>
        <button class="btn btn-primary mt-3" @click="goBack">Voltar</button>
      </div>
    </div>

    <!-- Caso nenhuma resposta seja encontrada -->
    <div v-else-if="!loading">
      <p class="text-center text-muted">Nenhuma resposta encontrada para esta sessão.</p>
    </div>

    <!-- Mensagem de carregamento -->
    <div v-else>
      <p class="text-center text-muted">Carregando respostas...</p>
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
    sessionLink: {
      type: String,
      required: true, // Link da sessão fornecido pelo componente pai
    },
  },
  data() {
    return {
      answers: [], // Lista de respostas obtidas da API
      loading: true, // Estado de carregamento
    };
  },
  async created() {
    try {
      // Consulta a API para obter as respostas
      const response = await api.get(`/session/${this.sessionId}/answers/`);
      this.answers = response.data;
    } catch (error) {
      console.error("Erro ao buscar respostas:", error);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    goBack() {
      // Emite um evento para o componente pai voltar à tela anterior
      this.$emit("go-back");
    },
  },
};
</script>

<style scoped>
.answers-screen {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
}
</style>
