<template>
  <div class="questionnaire-screen d-flex justify-content-center align-items-center vh-100">
    <div class="card p-4 shadow-sm" style="max-width: 600px; width: 100%;">
      <!-- Tela de boas-vindas -->
      <div v-if="step === 'welcome'">
        <h1 class="text-primary text-center">Bem-vindo ao Amorfy!</h1>
        <h2 class="text-center">Meça a TEMPERATURA do seu RELACIONAMENTO.</h2>
        <p class="text-center">Nos diga seu nome para começar.</p>
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

        <button class="btn btn-primary w-100 mt-3" @click="emitSessionCompleted">Ver Respostas</button>
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
    };
  },
  created() {
    if (this.originSessionId) {
      this.isDerivedSession = true;
      console.log("Sessão derivada detectada. ID da sessão original:", this.originSessionId);
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

        // Enviar requisição para criar a sessão
        const response = await api.post("/session/create/", { name: this.name });

        // Verificar resposta bem-sucedida
        this.sessionId = response.data.session_id;
        this.sessionLink = `${window.location.origin}/session/${this.sessionId}`;

        console.log("Sessão criada com sucesso:", {
          sessionId: this.sessionId,
          sessionLink: this.sessionLink,
        });

        // Carregar perguntas do backend
        const questionsResponse = await api.get("/questions/");
        this.questions = questionsResponse.data.map((question) => ({
          ...question,
          options: question.options?.map((option, index) => ({
            id: `${question.id}-option-${index + 1}`,
            text: option,
          })),
        }));

        console.log("Perguntas carregadas:", this.questions);

        // Inicializar respostas com valores vazios
        this.answers = new Array(this.questions.length).fill("");
        this.step = "questions";
      } catch (error) {
        console.error("Erro ao iniciar a sessão:", error);

        // Tratar erros específicos do backend
        if (error.response) {
          const status = error.response.status;
          const errorMessage = error.response.data.error || "Erro desconhecido.";

          if (status === 400) {
            alert("Erro: Nome é obrigatório.");
          } else if (status === 500 && errorMessage.includes("A tabela 'Session' não foi encontrada")) {
            alert("Erro crítico: Problema no banco de dados. Por favor, entre em contato com o suporte.");
          } else {
            alert(`Erro inesperado: ${errorMessage}`);
          }
        } else {
          // Tratar erros de conexão ou outros problemas
          alert("Erro de conexão com o servidor. Por favor, tente novamente mais tarde.");
        }
      }
    },
    saveAndAdvance() {
      console.log("Salvando resposta da pergunta:", {
        question: this.currentQuestion,
        answer: this.answers[this.currentQuestionIndex],
      });

      // Avançar para a próxima pergunta ou finalizar
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestionIndex++;
        console.log("Indo para a próxima pergunta. Índice atual:", this.currentQuestionIndex);
      } else {
        console.log("Finalizando questionário. Enviando respostas...");
        this.submitAnswers();
      }
    },
    goToPreviousQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--;
        console.log("Voltando para a pergunta anterior. Índice atual:", this.currentQuestionIndex);
      }
    },
    async submitAnswers() {
      try {
        const answersData = this.questions.map((question, index) => ({
          question_id: question.id,
          response: this.answers[index],
        }));

        console.log("Enviando respostas para o backend:", answersData);

        await api.post(`/session/${this.sessionId}/submit_answers/`, { answers: answersData });

        if (this.isDerivedSession) {
          console.log("Gerando link para resultados...");
          const resultsLink = `${window.location.origin}/results/${this.sessionId}`;
          this.$emit("show-results", { sessionId: this.sessionId, resultsLink });
        } else {
          this.step = "completed";
        }

        console.log("Respostas enviadas com sucesso!");
      } catch (error) {
        console.error("Erro ao salvar respostas:", error);
      }
    },
    emitSessionCompleted() {
      console.log("Emitindo evento session-completed com:", this.sessionId);
      this.$emit("session-completed", {
        sessionId: this.sessionId,
        sessionLink: this.sessionLink,
      });
    },
    copyLink() {
    const fullLink = `${this.sessionLink}/derived_session/`;
    navigator.clipboard.writeText(fullLink)
      .then(() => {
        alert("Link copiado para a área de transferência!");
      })
      .catch((err) => {
        console.error("Erro ao copiar link:", err);
        alert("Erro ao copiar o link.");
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
