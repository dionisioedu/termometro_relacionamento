<template>
  <div class="results-screen container mt-5">
    <h1 class="text-primary text-center">Resultados Comparativos</h1>

    <!-- Mensagem de Erro -->
    <div v-if="errorMessage" class="alert alert-danger text-center mt-4">
      {{ errorMessage }}
    </div>

    <!-- Mensagem de Carregamento -->
    <div v-if="loading" class="text-center">
      <p class="text-muted">Carregando resultados...</p>
    </div>

    <!-- Mensagem para resultados vazios -->
    <div v-if="!loading && report.length === 0 && !errorMessage" class="text-center">
      <p class="text-muted">Nenhum resultado encontrado para esta sessão.</p>
    </div>

    <!-- Resultados -->
    <div v-if="!loading && report.length > 0">
      <table class="table table-bordered mt-4">
        <thead class="table-light">
          <tr>
            <th scope="col">Pergunta</th>
            <th scope="col">Primeiro Ator</th>
            <th scope="col">Segundo Ator</th>
            <th scope="col">Compatibilidade</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="result in report" :key="result.question">
            <td>{{ result.question }}</td>
            <td>{{ result.origin_response }}</td>
            <td>{{ result.derived_response }}</td>
            <td>{{ result.similarity }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Link compartilhável -->
    <div class="text-center mt-4" v-if="resultsLink">
      <p>Link para compartilhar os resultados:</p>
      <p class="text-break"><strong>{{ resultsLink }}</strong></p>
      <button class="btn btn-outline-primary mt-2" @click="copyLink">Copiar Link</button>
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
      report: [],
      resultsLink: "",
      errorMessage: "",
      loading: true,
    };
  },
  async created() {
    try {
      const response = await api.get(`/session/${this.sessionId}/results/`);
      this.report = response.data.report;
      this.resultsLink = response.data.results_link;
    } catch (error) {
      console.error("Erro ao carregar resultados:", error);
      this.errorMessage = "Não foi possível carregar os resultados. Por favor, tente novamente mais tarde.";
    } finally {
      this.loading = false;
    }
  },
  methods: {
    copyLink() {
      navigator.clipboard.writeText(this.resultsLink)
        .then(() => alert("Link copiado para a área de transferência!"))
        .catch((err) => alert("Erro ao copiar o link: " + err));
    },
  },
};
</script>

<style scoped>
.results-screen {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
}
</style>
