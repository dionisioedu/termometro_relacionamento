<template>
  <div id="app">
    <!-- Tela do questionário do primeiro ator -->
    <UserQuestionnaire 
      v-if="!showDerivedSession && !showAnswers && !showLink && !showResults" 
      @user-entered="setUserName"
      @session-completed="showSessionAnswers"
    />

    <!-- Tela do segundo ator para iniciar nova sessão derivada -->
    <DerivedSession 
      v-if="showDerivedSession" 
      :originSessionId="originSessionId"
      @start-questions="startDerivedQuestionnaire"
    />

    <!-- Tela de respostas -->
    <SessionAnswers 
      v-if="showAnswers"
      :sessionId="sessionId"
      :sessionLink="sessionLink"
      @go-back="handleShowLink"
    />

    <!-- Tela com o link -->
    <SessionAnswersWithLink 
      v-if="showLink"
      :sessionLink="sessionLink"
      @go-back="handleGoBackToQuestionnaire"
    />

    <!-- Tela de resultados -->
    <ResultsView 
      v-if="showResults"
      :derivedSessionId="derivedSessionId"
      :originSessionId="originSessionId"
      @go-back="handleShowLink"
    />
  </div>
</template>

<script>
import UserQuestionnaire from "./components/UserQuestionnaire.vue";
import DerivedSession from "./components/DerivedSession.vue";
import SessionAnswers from "./components/SessionAnswers.vue";
import SessionAnswersWithLink from "./components/SessionAnswersWithLink.vue";
import ResultsView from "./components/ResultsView.vue";

export default {
  data() {
    return {
      userName: null, // Nome do usuário
      sessionId: null, // ID da sessão atual (nova sessão para o segundo ator)
      originSessionId: null, // ID da sessão original
      derivedSessionId: null, // ID da sessão derivada
      sessionLink: null, // Link compartilhável da sessão
      showAnswers: false, // Exibe tela de respostas
      showLink: false, // Exibe tela com o link
      showDerivedSession: false, // Exibe a tela para iniciar a sessão derivada
      showResults: false, // Exibe tela de resultados
    };
  },
  components: {
    UserQuestionnaire,
    DerivedSession,
    SessionAnswers,
    SessionAnswersWithLink,
    ResultsView,
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
      this.showDerivedSession = false;
      this.showResults = false;

      console.log("Atualizado estado: showAnswers =", this.showAnswers);
    },

    // Exibe o link da sessão
    handleShowLink() {
      console.log("Usuário deseja ver o link da sessão.");
      this.showAnswers = false;
      this.showLink = true;
      this.showDerivedSession = false;
      this.showResults = false;
    },

    // Manipula o retorno à tela do questionário
    handleGoBackToQuestionnaire() {
      console.log("Usuário voltou para o questionário.");
      this.showAnswers = false;
      this.showLink = false;
      this.showDerivedSession = false;
      this.showResults = false;
    },

    // Inicia uma sessão derivada
    startDerivedQuestionnaire({ sessionId, name }) {
      console.log("Nova sessão derivada iniciada. ID:", sessionId);
      this.sessionId = sessionId;
      this.userName = name;
      this.showDerivedSession = false;
      this.showAnswers = false;
      this.showLink = false;
      this.showResults = false;
    },

    // Exibe os resultados após o questionário do segundo ator
    showResultsScreen(sessionId) {
      console.log("Sessão derivada concluída. ID:", sessionId);
      this.derivedSessionId = sessionId;
      this.showDerivedSession = false;
      this.showAnswers = false;
      this.showLink = false;
      this.showResults = true;
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
