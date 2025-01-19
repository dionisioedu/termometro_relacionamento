<template>
  <div class="results-screen d-flex justify-content-center align-items-start vh-100">
    <div class="card p-4 shadow-lg animate__animated animate__fadeIn" style="max-width: 800px; width: 100%; border-radius: 20px;">
      <div class="text-center">
        <h1 class="text-gradient">Resultados Comparativos</h1>
        <p class="tagline">Veja como as respostas se comparam.</p>
      </div>

      <div v-if="report.length > 0" class="results-table mt-4">
        <table class="table table-hover table-dark">
          <thead>
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
              <td :class="{'text-success': result.similarity === 'igual', 'text-danger': result.similarity === 'diferente'}">
                {{ result.similarity }}
              </td>
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
          class="btn btn-gradient" 
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
  background: linear-gradient(135deg, #1e1e1e, #343434);
  color: #ffffff;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 40px;
  height: 100vh;
  overflow: auto;
}

.card {
  background-color: #2a2a2a;
  border: none;
  border-radius: 20px;
  box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.3);
}

.text-gradient {
  background: linear-gradient(to right, #cfa877, #f7e2c6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.tagline {
  font-size: 1.1rem;
  color: #cccccc;
  margin-bottom: 20px;
}

.table {
  color: #ffffff;
  background-color: #2a2a2a;
  border-radius: 10px;
  overflow: hidden;
}

.table th {
  background-color: #3b3b3b;
  color: #f7e2c6;
  font-weight: bold;
}

.table td {
  background-color: #2a2a2a;
  color: #ffffff;
  border-top: 1px solid #444444;
}

.text-success {
  color: #4caf50 !important;
  font-weight: bold;
}

.text-danger {
  color: #f44336 !important;
  font-weight: bold;
}

.btn-gradient {
  background: linear-gradient(90deg, #cfa877, #f7e2c6);
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  border-radius: 12px;
  font-weight: bold;
  transition: 0.3s;
  box-shadow: 0px 4px 12px rgba(207, 168, 119, 0.4);
}

.btn-gradient:hover {
  background: linear-gradient(90deg, #f7e2c6, #cfa877);
  color: #ffffff;
  box-shadow: 0px 6px 18px rgba(207, 168, 119, 0.6);
}

.btn-success {
  background-color: #4caf50;
  border-color: #45a049;
  color: white;
  transition: 0.3s;
}

.btn-success:hover {
  background-color: #45a049;
  border-color: #3e923d;
  box-shadow: 0px 4px 12px rgba(72, 161, 75, 0.6);
}
</style>
