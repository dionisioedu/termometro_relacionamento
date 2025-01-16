<template>
  <div id="app">
    <!-- Tela do questionário -->
    <UserQuestionnaire 
      v-if="!showAnswers && !showLink" 
      @user-entered="setUserName"
      @session-completed="showSessionAnswers"
    />

    <!-- Tela de respostas -->
    <SessionAnswers 
      v-if="showAnswers"
      :sessionId="sessionId"
      :session-link="sessionLink"
      @go-back="handleShowLink"
    />

    <!-- Tela com o link -->
    <SessionAnswersWithLink 
      v-if="showLink"
      :sessionLink="sessionLink"
      @go-back="handleGoBackToQuestionnaire"
    />
  </div>
</template>

<script>
import UserQuestionnaire from "./components/UserQuestionnaire.vue";
import SessionAnswers from "./components/SessionAnswers.vue";
import SessionAnswersWithLink from "./components/SessionAnswersWithLink.vue";

export default {
  data() {
    return {
      userName: null, // Nome do usuário
      sessionId: null, // ID da sessão atual
      sessionLink: null, // Link compartilhável da sessão
      showAnswers: false, // Exibe tela de respostas
      showLink: false, // Exibe tela com o link
    };
  },
  components: {
    UserQuestionnaire,
    SessionAnswers,
    SessionAnswersWithLink,
  },
  methods: {
    // Define o nome do usuário quando ele é inserido
    setUserName(name) {
      console.log("Nome do usuário definido:", name);
      this.userName = name;
    },

    // Exibe as respostas ao final do questionário
    showSessionAnswers({ sessionId, sessionLink }) {
      console.log("Recebido sessionId e sessionLink:", sessionId, sessionLink);

      if (!sessionId || !sessionLink) {
        console.error("Erro: sessionId ou sessionLink estão indefinidos.");
        return;
      }

      this.sessionId = sessionId;
      this.sessionLink = sessionLink;
      this.showAnswers = true;
      this.showLink = false;

      console.log("Atualizado estado: showAnswers =", this.showAnswers);
    },

    // Exibe o link da sessão
    handleShowLink() {
      console.log("Usuário deseja ver o link da sessão.");
      this.showAnswers = false;
      this.showLink = true;
    },

    // Manipula o retorno à tela do questionário
    handleGoBackToQuestionnaire() {
      console.log("Usuário voltou para o questionário.");
      this.showAnswers = false;
      this.showLink = false;
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
