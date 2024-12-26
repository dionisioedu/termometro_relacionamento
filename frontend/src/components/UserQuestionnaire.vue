<template>
  <div class="questionnaire-screen d-flex justify-content-center align-items-center vh-100">
    <div class="card p-4 shadow-sm" style="max-width: 600px; width: 100%;">
      <!-- Tela de boas-vindas -->
      <div v-if="step === 'welcome'">
        <h1 class="text-primary text-center">Bem-vindo!</h1>
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
        <form @submit.prevent="submitAnswer">
          <!-- Perguntas com opções -->
          <div v-if="currentQuestion.options && currentQuestion.options.length > 0">
            <div v-for="option in currentQuestion.options" :key="option.id" class="form-check">
              <input
                type="radio"
                :id="option.id"
                :value="option.text"
                v-model="selectedAnswer"
                class="form-check-input"
                required
              />
              <label :for="option.id" class="form-check-label">{{ option.text }}</label>
            </div>
          </div>

          <!-- Perguntas abertas -->
          <div v-else>
            <textarea
              v-model="selectedAnswer"
              class="form-control"
              placeholder="Digite sua resposta"
              rows="3"
              required
            ></textarea>
          </div>

          <!-- Botão "Próxima" -->
          <button
            type="submit"
            class="btn btn-primary w-100 mt-3"
            :disabled="!selectedAnswer"
          >
            Próxima
          </button>
        </form>
      </div>

      <!-- Tela de finalização -->
      <div v-else-if="step === 'completed'">
        <h1 class="text-success text-center">Obrigado!</h1>
        <p class="text-center">Respostas salvas com sucesso. Use o link abaixo para compartilhar com seu parceiro(a):</p>
        <p class="text-center text-break"><strong>{{ sessionLink }}</strong></p>
        <button class="btn btn-primary w-100 mt-3" @click="emitSessionCompleted">Ver Respostas</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../api";

export default {
  data() {
    return {
      step: "welcome", // welcome | questions | completed
      name: "",
      sessionId: null,
      sessionLink: "",
      questions: [], // Estrutura das perguntas: [{ id, text, options: [{ id, text }] }]
      currentQuestionIndex: 0,
      selectedAnswer: "", // Resposta selecionada ou preenchida para a pergunta atual
      answers: [],
    };
  },
  computed: {
    currentQuestion() {
      return this.questions[this.currentQuestionIndex];
    },
  },
  methods: {
    async startSession() {
      try {
        const response = await api.post("/session/create/", { name: this.name });
        this.sessionId = response.data.session_id;
        this.sessionLink = response.data.link;

        // Carregar perguntas do backend
        const questionsResponse = await api.get("/questions/");
        this.questions = questionsResponse.data.map((question) => ({
          ...question,
          options: question.options?.map((option, index) => ({
            id: `${question.id}-option-${index + 1}`,
            text: option,
          })),
        }));

        // Mudar para a tela de perguntas
        this.step = "questions";
      } catch (error) {
        console.error("Erro ao iniciar a sessão:", error);
      }
    },
    async submitAnswer() {
      // Salvar a resposta atual
      this.answers.push({
        question_id: this.currentQuestion.id,
        response: this.selectedAnswer,
      });

      // Resetar a resposta selecionada
      this.selectedAnswer = "";

      // Avançar para a próxima pergunta ou finalizar
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestionIndex++;
      } else {
        // Salvar todas as respostas no backend
        try {
          await api.post(`/session/${this.sessionId}/submit_answers/`, {
            answers: this.answers,
          });
          this.step = "completed";
        } catch (error) {
          console.error("Erro ao salvar respostas:", error);
        }
      }
    },
    emitSessionCompleted() {
      // Emite o evento para o componente pai
      this.$emit("session-completed", this.sessionId);
    },
  },
};
</script>

<style scoped>
.questionnaire-screen {
  background-color: #f8f9fa; /* Fundo leve */
}
</style>
