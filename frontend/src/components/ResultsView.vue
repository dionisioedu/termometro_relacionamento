<template>
    <div class="results-screen container mt-5">
      <h1 class="text-primary text-center">Relatório Comparativo</h1>
      <div v-if="report.length > 0">
        <table class="table table-bordered mt-4">
          <thead class="table-light">
            <tr>
              <th>Pergunta</th>
              <th>Resposta (Origem)</th>
              <th>Resposta (Derivada)</th>
              <th>Semelhança</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in report" :key="item.question">
              <td>{{ item.question }}</td>
              <td>{{ item.origin_response }}</td>
              <td>{{ item.derived_response }}</td>
              <td>{{ item.similarity }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>Carregando relatório...</p>
      </div>
    </div>
  </template>
  
  <script>
  import api from "../api";
  
  export default {
    props: {
      derivedSessionId: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        report: [],
      };
    },
    async created() {
      try {
        const response = await api.get(`/session/${this.derivedSessionId}/results/`);
        this.report = response.data.report;
        console.log("Relatório carregado:", this.report);
      } catch (error) {
        console.error("Erro ao carregar relatório:", error);
      }
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
  