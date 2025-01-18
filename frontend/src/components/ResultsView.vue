<template>
  <div class="results-screen d-flex justify-content-center align-items-center vh-100">
    <div class="card p-4 shadow-sm" style="max-width: 800px; width: 100%;">
      <h1 class="text-primary text-center">Resultados Comparativos</h1>

      <div v-if="report.length > 0">
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

      <div v-else class="text-center">
        <p class="text-muted">Carregando resultados...</p>
      </div>

      <!-- Botões de Ação -->
      <div class="d-flex justify-content-around mt-4">
        <button 
          class="btn btn-outline-primary"
          @click="copyLink">
          Copiar Link
        </button>
        <a 
          :href="whatsappLink" 
          target="_blank"
          class="btn btn-success">
          Enviar no WhatsApp
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../api";

export default {
  props: {
    originSessionId: {
      type: String,
      required: true,
    },
    derivedSessionId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      report: [], // Resultados comparativos
      resultsLink: `${window.location.origin}/results?originSessionId=${this.originSessionId}&derivedSessionId=${this.derivedSessionId}`,
    };
  },
  async created() {
    try {
      const response = await api.get(`/results/${this.derivedSessionId}`);
      this.report = response.data.report;
    } catch (error) {
      console.error("Erro ao carregar resultados:", error);
    }
  },
  computed: {
    whatsappLink() {
      return `https://api.whatsapp.com/send?text=${encodeURIComponent(
        "Veja os resultados do questionário Amorfy:\n" + this.resultsLink
      )}`;
    },
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
.table {
  margin-top: 20px;
}
</style>
