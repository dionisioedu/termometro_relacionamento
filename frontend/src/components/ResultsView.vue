<template>
  <div class="results-screen d-flex justify-content-center align-items-start vh-100">
    <div class="card p-4 shadow-lg animate__animated animate__fadeIn" style="max-width: 800px; width: 100%; border-radius: 20px;">
      <div class="text-center">
        <h1 class="solid-title">Resultados do Casal</h1>
        <p class="tagline">Veja como as respostas se comparam.</p>
      </div>

      <!-- Placar Total -->
      <div class="scoreboard d-flex justify-content-between align-items-center mb-4">
        <div class="actor-score">
          <span class="badge badge-total">{{ user1Name }}: {{ user1TotalScore }}</span>
        </div>
        <div class="actor-score">
          <span class="badge badge-total">{{ user2Name }}: {{ user2TotalScore }}</span>
        </div>
      </div>

      <!-- Insights em Cards -->
      <div v-if="insights.length > 0" class="results-cards mt-4">
        <div
          v-for="insight in insights"
          :key="insight.title"
          class="card shadow-sm mb-3 p-3"
          :class="getCustomCardClass(insight.color_flag)"
        >
          <div class="d-flex justify-content-between align-items-center">
            <h5 class="insight-title">{{ insight.title }}</h5>
          </div>
          <div class="d-flex justify-content-between mt-2">
            <span :class="getBadgeClass(insight.color_flag)" class="badge">{{ user1Name }}: {{ insight.user1_score }}</span>
            <span :class="getBadgeClass(insight.color_flag)" class="badge">{{ user2Name }}: {{ insight.user2_score }}</span>
          </div>
          <p class="insight-description mt-3">{{ insight.description }}</p>
        </div>
      </div>

      <!-- Mensagem de Carregamento -->
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
    derivedSessionId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      insights: [], // Lista de insights
      user1Name: "Usuário 1", // Nome do primeiro ator
      user2Name: "Usuário 2", // Nome do segundo ator
      user1TotalScore: 0, // Pontuação total do primeiro ator
      user2TotalScore: 0, // Pontuação total do segundo ator
      resultsLink: `${window.location.origin}/results?derivedSessionId=${this.derivedSessionId}`,
    };
  },
  async created() {
    try {
      const response = await api.get(`/results/${this.derivedSessionId}`);
      const { insights, user1_total_score, user2_total_score } = response.data.insights;
      this.insights = insights;
      this.user1TotalScore = user1_total_score;
      this.user2TotalScore = user2_total_score;
      this.user1Name = response.data.user1_name;
      this.user2Name = response.data.user2_name;
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
    getCustomCardClass(colorFlag) {
      switch (colorFlag) {
        case "green":
          return "custom-card-success";
        case "yellow":
          return "custom-card-warning";
        case "red":
          return "custom-card-danger";
        default:
          return "custom-card-default";
      }
    },
    getBadgeClass(colorFlag) {
      switch (colorFlag) {
        case "green":
          return "badge-success";
        case "yellow":
          return "badge-warning";
        case "red":
          return "badge-danger";
        default:
          return "badge-default";
      }
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

.solid-title {
  background: linear-gradient(to right, #cfa877, #f7e2c6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.card {
  background-color: #2a2a2a;
  border: none;
  border-radius: 20px;
  box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.3);
}

.tagline {
  font-size: 1.1rem;
  color: #cccccc;
  margin-bottom: 20px;
}

.results-cards .card {
  border-radius: 12px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  padding: 15px;
  color: inherit;
}

.insight-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: inherit; /* Herdar cor definida pelo card */
}

.insight-description {
  color: inherit; /* Herdar cor definida pelo card */
  font-size: 1rem;
  line-height: 1.5;
}

.actor-score {
  font-size: 1.2rem;
  font-weight: bold;
  color: #ffffff;
  display: flex;
  align-items: center;
}

.badge-total {
  background-color: #007bff;
  color: #ffffff;
  font-size: 1rem;
  padding: 5px 10px;
  border-radius: 8px;
  margin-left: 10px;
}

.custom-card-success {
  background-color: #eafaf1; /* Fundo suave verde */
  border-color: #c7e8d4;
  color: #2b6041; /* Texto verde escuro */
}

.custom-card-warning {
  background-color: #fff9e6; /* Fundo suave amarelo */
  border-color: #ffe4a3;
  color: #856404; /* Texto amarelo escuro */
}

.custom-card-danger {
  background-color: #fdecea; /* Fundo suave vermelho */
  border-color: #f5b4b4;
  color: #8a1f1f; /* Texto vermelho escuro */
}

.custom-card-default {
  background-color: #f5f5f5; /* Fundo neutro */
  border-color: #e0e0e0;
  color: #333333; /* Texto padrão escuro */
}

.badge {
  padding: 5px 10px;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: bold;
}

.badge-success {
  background-color: #28a745;
  color: #ffffff;
}

.badge-warning {
  background-color: #ffc107;
  color: #212529;
}

.badge-danger {
  background-color: #dc3545;
  color: #ffffff;
}

.badge-default {
  background-color: #6c757d;
  color: #ffffff;
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
