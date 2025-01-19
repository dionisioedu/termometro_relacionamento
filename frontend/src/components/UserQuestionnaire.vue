<template>
  <div class="questionnaire-screen d-flex justify-content-center align-items-start vh-100">
    <div class="card p-4 shadow-lg animate__animated animate__fadeIn" style="max-width: 600px; width: 100%; border-radius: 20px;">
      <!-- Tela de boas-vindas -->
      <div v-if="step === 'welcome'">
        <div class="text-center">
          <img src="/amorfy-logo.png" alt="Amorfy" style="width: 150px; margin-bottom: 20px;" />
          <h1 class="text-gradient">Bem-vindo ao <span class="highlight">Amorfy!</span></h1>
          <p class="tagline">Descubra a temperatura do seu relacionamento com estilo.</p>
        </div>
        <form @submit.prevent="startSession" class="mt-4">
          <div class="mb-3">
            <input
              v-model="name"
              type="text"
              class="form-control custom-input"
              placeholder="Digite seu nome"
              required
            />
          </div>
          <button type="submit" class="btn btn-gradient w-100">Começar</button>
        </form>
      </div>

      <!-- Tela de perguntas -->
      <div v-else-if="step === 'questions'">
        <h2 class="text-primary text-center">Pergunta {{ currentQuestionIndex + 1 }} de {{ questions.length }}</h2>
        <p class="lead text-center">{{ currentQuestion.text }}</p>

        <!-- Barra de progresso -->
        <div class="progress-container">
          <div 
            class="progress-bar" 
            :style="{ width: ((currentQuestionIndex + 1) / questions.length * 100) + '%' }">
          </div>
        </div>

        <!-- Opções ou campo aberto -->
        <div v-if="currentQuestion.options && currentQuestion.options.length" class="options-container">
          <div 
            v-for="option in currentQuestion.options" 
            :key="option.id" 
            class="btn-option" 
            :class="{ 'selected': answers[currentQuestionIndex] === option.text }"
            @click="selectOption(option.text)">
            {{ option.text }}
          </div>
        </div>
        <div v-else>
          <input 
            type="text" 
            class="form-control mt-3" 
            v-model="answers[currentQuestionIndex]" 
            :placeholder="'Digite sua resposta aqui...'"
          />
        </div>

        <!-- Botões de navegação -->
        <div class="d-flex justify-content-between mt-4">
          <button
            type="button"
            class="btn btn-outline-secondary"
            @click="goToPreviousQuestion"
            :disabled="currentQuestionIndex === 0"
          >
            Voltar
          </button>
          <button
            type="button"
            class="btn btn-gradient"
            @click="saveAndAdvance"
            :disabled="!answers[currentQuestionIndex]"
          >
            Próxima
          </button>
        </div>
      </div>

      <!-- Tela de finalização -->
      <div v-else-if="step === 'completed'">
        <div class="text-center">
          <img src="/success.png" alt="Sucesso" style="width: 120px; margin-bottom: 20px;" />
          <h1 class="text-success">Obrigado!</h1>
          <p class="lead text-centered">Suas respostas foram salvas com sucesso.</p>
          <p class="text-center text-break"><strong>{{ sessionLink + '/derived_session/' }}</strong></p>

          <div class="d-flex justify-content-around mt-3">
            <button class="btn btn-gradient" @click="copyLink">Copiar Link</button>
            <a :href="whatsappLink" target="_blank" class="btn btn-success">Enviar no WhatsApp</a>
          </div>
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
      default: null,
    },
    isDerivedSession: {
      type: Boolean,
      default: false,
    },
    originCreatorName: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      step: "welcome",
      name: "",
      sessionLink: "",
      sessionId: null,
      questions: [],
      currentQuestionIndex: 0,
      answers: [],
    };
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
        else {
          const response = await api.post("/session/create/", { name: this.name, origin_session_id: this.originSessionId });
          this.sessionId = response.data.session_id;
          this.sessionLink = `${window.location.origin}/session/${this.sessionId}`;
          console.log("Sessão derivada iniciada:", this.sessionId);
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
    selectOption(optionText) {
      this.answers[this.currentQuestionIndex] = optionText;
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

        console.log(`(${this.sessionId})Enviando respostas para o backend:`, answersData);

        await api.post(`/session/${this.sessionId}/submit_answers/`, { answers: answersData });

        if (this.isDerivedSession) {
          this.$router.push({
            name: "ResultsView",
            query: {
              derivedSessionId: this.sessionId,
            },
          });
        } else {
          this.step = "completed";
        }
      } catch (error) {
        console.error("Erro ao salvar respostas:", error);
      }
    },
    copyLink() {
      navigator.clipboard.writeText(`${this.sessionLink}/derived_session/`).then(() => {
        alert("Link copiado com sucesso!");
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

.custom-input {
  border-radius: 12px;
  border: 2px solid #3b3b3b;
  background-color: #1e1e1e;
  color: #ffffff;
  padding: 10px;
  transition: 0.3s;
}

.custom-input:focus {
  border-color: #cfa877;
  background-color: #2a2a2a;
  outline: none;
  box-shadow: 0 0 8px rgba(207, 168, 119, 0.6);
}

.custom-input::placeholder {
  color: #bbbbbb;
}

.lead {
  color: #f7e2c6; /* Escolha uma cor clara para contraste */
  font-size: 1.2rem; /* Opcional: Aumentar o tamanho da fonte para melhor leitura */
  font-weight: 500; /* Opcional: Tornar o texto mais destacado */
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

.btn-outline-secondary {
  border: 2px solid #3b3b3b;
  background-color: transparent;
  color: #ffffff;
  border-radius: 12px;
  transition: 0.3s;
}

.btn-outline-secondary:hover {
  background-color: #3b3b3b;
  border-color: #cfa877;
  color: #cfa877;
}

.options-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  justify-content: center;
}

.btn-option {
  background-color: #2a2a2a;
  color: #ffffff; /* Cor da fonte ajustada para maior contraste */
  border: 2px solid transparent;
  border-radius: 12px;
  padding: 12px 24px;
  cursor: pointer;
  transition: 0.3s;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
  text-align: center;
  font-weight: 500; /* Tornar o texto um pouco mais legível */
  font-size: 1rem; /* Ajustar o tamanho do texto */
}

.btn-option:hover {
  background-color: #3b3b3b;
  color: #cfa877; /* Texto com destaque ao passar o mouse */
  border-color: #cfa877;
}

.btn-option.selected {
  background-color: #cfa877;
  color: #2a2a2a; /* Texto escuro para contraste com o fundo claro */
  border-color: #f7e2c6;
  box-shadow: 0 4px 10px rgba(207, 168, 119, 0.4);
}

.text-break {
  word-wrap: break-word;
  color: white;
}

a.btn-success {
  background-color: #4caf50;
  border-color: #45a049;
  color: white;
  transition: 0.3s;
}

a.btn-success:hover {
  background-color: #45a049;
  border-color: #3e923d;
  box-shadow: 0px 4px 12px rgba(72, 161, 75, 0.6);
}

/* Estilo da barra de progresso */
.progress-container {
  height: 10px;
  background-color: #f1f1f1; /* Cor do fundo da barra */
  border-radius: 5px;
  margin: 10px 0;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background-color: #5cb85c; /* Cor da barra preenchida */
  transition: width 0.3s ease-in-out;
}

.animate__fadeIn {
  animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
