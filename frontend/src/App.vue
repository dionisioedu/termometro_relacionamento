<template>
  <div id="app">
    <router-view 
      @user-entered="setUserName"
      @session-completed="showSessionAnswers"
      @show-results="showResultsScreen"
      @start-derived-session="showDerivedSessionScreen"
      @go-back="handleGoBackToQuestionnaire"
    />
  </div>
</template>

<script>
import api from "./api";

export default {
  data() {
    return {
      userName: null, // Nome do usuário atual
      sessionId: null, // ID da sessão atual
      originSessionId: null, // ID da sessão original
      derivedSessionId: null, // ID da sessão derivada
      sessionLink: null, // Link compartilhável da sessão
      resultsLink: null, // Link para os resultados comparativos
    };
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

      console.log("Atualizado estado: Exibindo respostas.");
    },

    // Exibe a tela de iniciar sessão derivada
    showDerivedSessionScreen(originSessionId) {
      console.log("Exibindo tela de sessão derivada para a sessão original:", originSessionId);
      this.originSessionId = originSessionId;
    },

    // Inicia uma sessão derivada
    startDerivedQuestionnaire({ sessionId, name }) {
      console.log("Nova sessão derivada iniciada. ID:", sessionId);
      this.sessionId = sessionId;
      this.userName = name;
    },

    // Exibe os resultados após o questionário do segundo ator
    async showResultsScreen(sessionId) {
      console.log("Sessão derivada concluída. ID:", sessionId);

      try {
        // Obter o link dos resultados
        const response = await api.get(`/session/${sessionId}/results/`);
        this.resultsLink = response.data.results_link;

        console.log("Link dos resultados gerado:", this.resultsLink);

        this.derivedSessionId = sessionId;
      } catch (error) {
        console.error("Erro ao obter os resultados:", error);
      }
    },

    // Retorna ao questionário principal
    handleGoBackToQuestionnaire() {
      console.log("Retornando ao questionário principal.");
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
