<template>
    <div class="container py-5">
      <div class="card shadow-sm p-4">
        <h1 class="text-primary">Pergunta {{ currentQuestionIndex + 1 }} de {{ questions.length }}</h1>
        <p class="lead">{{ questions[currentQuestionIndex].text }}</p>
        <form @submit.prevent="submitAnswer">
          <div class="mb-3">
            <input
              v-model="currentAnswer"
              type="text"
              class="form-control"
              placeholder="Digite sua resposta"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary w-100">Próxima</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import api from "../api";
  
  export default {
    data() {
      return {
        session: "",
        userId: null,
        questions: [],
        currentQuestionIndex: 0,
        currentAnswer: "",
      };
    },
    async created() {
      this.session = this.$route.query.session;
      const response = await api.get("/questions/");
      this.questions = response.data;
    },
    methods: {
      async submitAnswer() {
        const question = this.questions[this.currentQuestionIndex];
        await api.post(`/session/${this.session}/answers/`, {
          user_id: this.userId,
          answers: [{ question_id: question.id, response: this.currentAnswer }],
        });
        this.currentAnswer = "";
        if (this.currentQuestionIndex < this.questions.length - 1) {
          this.currentQuestionIndex++;
        } else {
          this.$router.push("/completed");
        }
      },
    },
  };
  </script>
  