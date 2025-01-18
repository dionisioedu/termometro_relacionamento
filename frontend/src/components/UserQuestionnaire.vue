<template>
  <div class="questionnaire-screen d-flex justify-content-center align-items-center vh-100">
    <div class="card p-4 shadow-sm" style="max-width: 600px; width: 100%;">
      <!-- Tela de boas-vindas -->
      <div v-if="step === 'welcome'">
        <h1 class="text-primary text-center">Bem-vindo ao Amorfy!</h1>
        <h2 class="text-center">Meça a TEMPERATURA do seu RELACIONAMENTO.</h2>
        <p class="text-center">
          {{ isDerivedSession 
            ? `Você está participando de uma sessão derivada iniciada por ${originCreatorName}.` 
            : "Nos diga seu nome para começar."
          }}
        </p>
        <form @submit.prevent="startSession">
          <div class="mb-3">
            <input
              v-model="name"
              type="text"
              class="form-control"
              placeholder="Digite seu nome"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary w-100">Começar</button>
        </form>
      </div>

      <!-- Tela de perguntas -->
      <div v-else-if="step === 'questions'">
        <h2 class="text-primary">Pergunta {{ currentQuestionIndex + 1 }} de {{ questions.length }}</h2>
        <p class="lead">{{ currentQuestion.text }}</p>
        <form @submit.prevent="saveAndAdvance">
          <!-- Perguntas com opções -->
          <div v-if="currentQuestion.options && currentQuestion.options.length > 0">
            <div v-for="option in currentQuestion.options" :key="option.id" class="form-check">
              <input
                type="radio"
                :id="option.id"
                :value="option.text"
                v-model="answers[currentQuestionIndex]"
                class="form-check-input"
                required
              />
              <label :for="option.id" class="form-check-label">{{ option.text }}</label>
            </div>
          </div>

          <!-- Perguntas abertas -->
          <div v-else>
            <textarea
              v-model="answers[currentQuestionIndex]"
              class="form-control"
              placeholder="Digite sua resposta"
              rows="3"
              required
            ></textarea>
          </div>

          <!-- Botões de navegação -->
          <div class="d-flex justify-content-between mt-3">
            <button
              type="button"
              class="btn btn-secondary"
              @click="goToPreviousQuestion"
              :disabled="currentQuestionIndex === 0"
            >
              Voltar
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="!answers[currentQuestionIndex]"
            >
              Próxima
            </button>
          </div>
        </form>
      </div>

      <!-- Tela de finalização -->
      <div v-else-if="step === 'completed'">
        <h1 class="text-success text-center">Obrigado!</h1>
        <p class="text-center">Respostas salvas com sucesso. Use o link abaixo para compartilhar com seu parceiro(a):</p>
        <p class="text-center text-break"><strong>{{ sessionLink + "/derived_session/" }}</strong></p>

        <!-- Botões de Copiar e Enviar para WhatsApp -->
        <div class="d-flex justify-content-around mt-3">
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
  </div>
</template>

<script>
import api from "../api";

export default {
  props: {
    originSessionId: {
      type: String,
      default: null, // Nulo para sessões normais, preenchido para derivadas
    },
  },
  data() {
    return {
      step: "welcome", // welcome | questions | completed
      name: "",
      sessionId: null,
      sessionLink: "",
      questions: [], // Estrutura das perguntas: [{ id, text, options: [{ id, text }] }]
      currentQuestionIndex: 0,
      answers: [], // Armazena as respostas para cada pergunta
      isDerivedSession: false,
      originCreatorName: null,
    };
  },
  async created() {
    this.isDerivedSession = !!this.originSessionId;
    if (this.isDerivedSession) {
      try {
        const response = await api.get(`/session/${this.originSessionId}/`);
        this.originCreatorName = response.data.creator_name || "Desconhecido";
        console.log("Sessão derivada iniciada pelo criador:", this.originCreatorName);
      } catch (error) {
        console.error("Erro ao carregar sessão original:", error);
      }
    }
  },
  computed: {
    currentQuestion() {
      return this.questions?.[this.currentQuestionIndex] || null;
    },
    whatsappLink() {
      const fullLink = `${this.sessionLink}/derived_session/`;
      return `https://api.whatsapp.com/send?text=${encodeURIComponent(
        "Olá! Acesse o link abaixo para participar do questionário Amorfy:\n" + fullLink
      )}`;
    },
  },
  methods: {
    async startSession() {
      try {
        console.log("Iniciando sessão para:", this.name);

        if (!this.isDerivedSession) {
          const response = await api.post("/session/create/", { name: this.name });
          this.sessionId = response.data.session_id;
          this.sessionLink = `${window.location.origin}/session/${this.sessionId}`;
          console.log("Sessão criada:", this.sessionId);
        }

        const questionsResponse = await api.get("/questions/");
        this.questions = questionsResponse.data.map((question) => ({
          ...question,
          options: question.options?.map((option, index) => ({
            id: `${question.id}-option-${index + 1}`,
            text: option,
          })),
        }));

        console.log("Perguntas carregadas:", this.questions);

        this.answers = new Array(this.questions.length).fill("");
        this.step = "questions";
      } catch (error) {
        console.error("Erro ao iniciar sessão:", error);
        alert("Erro ao carregar as perguntas. Tente novamente.");
      }
    },
    saveAndAdvance() {
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestionIndex++;
      } else {
        this.submitAnswers();
      }
    },
    goToPreviousQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--;
      }
    },
    async submitAnswers() {
      try {
        const answersData = this.questions.map((question, index) => ({
          question_id: question.id,
          response: this.answers[index],
        }));

        await api.post(`/session/${this.sessionId}/submit_answers/`, { answers: answersData });

        if (this.isDerivedSession) {
          const resultsLink = `${window.location.origin}/results/${this.sessionId}`;
          this.$emit("show-results", { sessionId: this.sessionId, resultsLink });
        } else {
          this.step = "completed";
        }
      } catch (error) {
        console.error("Erro ao salvar respostas:", error);
      }
    },
    copyLink() {
      const fullLink = `${this.sessionLink}/derived_session/`;
      navigator.clipboard.writeText(fullLink).then(() => {
        alert("Link copiado para a área de transferência!");
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
