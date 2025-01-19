<template>
  <div class="questionnaire-screen d-flex justify-content-center align-items-start vh-100">
    <div class="card p-4 shadow-lg animate__animated animate__fadeIn" style="max-width: 600px; width: 100%; border-radius: 20px;">
      <div v-if="loading" class="text-center">
        <img src="/loading.gif" alt="Carregando" style="width: 100px; margin-bottom: 20px;" />
        <p class="text-muted">Carregando sessão derivada...</p>
      </div>

      <div v-else>
        <div class="text-center">
          <img src="/amorfy-logo.png" alt="Amorfy" style="width: 150px; margin-bottom: 20px;" />
          <h1 class="text-gradient">Descubra qual a temperatura do seu relacionamento!</h1>
          <p class="tagline">
            Você foi convidado(a) por
            <strong>{{ originCreatorName }}</strong>.
          </p>
        </div>

        <div class="text-center mt-4">
          <p class="lead">Clique no botão abaixo para começar o questionário.</p>
          <button class="btn btn-gradient w-100" @click="startQuestionnaire">Começar Questionário</button>
        </div>
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
      const response = await api.get(`/session/${this.sessionId}/derived_session/`);
      const { origin_creator_name, answers_submitted } = response.data;

      this.originCreatorName = origin_creator_name || "Desconhecido";
      console.log("Sessão derivada carregada:", response.data);

      if (answers_submitted) {
        console.log("Respostas já enviadas. Redirecionando para resultados...");
        this.$router.push({ name: "ResultsView", query: { derivedSessionId: this.sessionId } });
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

.lead {
  color: #f7e2c6;
  font-size: 1.2rem;
  font-weight: 500;
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
</style>
