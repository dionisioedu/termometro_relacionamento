<template>
  <div id="app">
    <!-- Tela do questionário -->
    <UserQuestionnaire 
      v-if="!showAnswers" 
      @user-entered="setUserName"
      @session-completed="showSessionAnswers"
    />

    <!-- Tela de respostas -->
    <SessionAnswers 
      v-else 
      :sessionId="sessionId"
    />
  </div>
</template>

<script>
import UserQuestionnaire from "./components/UserQuestionnaire.vue";
import SessionAnswers from "./components/SessionAnswers.vue";

export default {
  data() {
    return {
      userName: null, // Nome do usuário
      sessionId: null, // ID da sessão atual
      showAnswers: false, // Controla qual tela será exibida
    };
  },
  components: {
    UserQuestionnaire,
    SessionAnswers,
  },
  methods: {
    // Define o nome do usuário quando ele é inserido
    setUserName(name) {
      this.userName = name;
    },

    // Exibe as respostas ao final do questionário
    showSessionAnswers(sessionId) {
      this.sessionId = sessionId;
      this.showAnswers = true;
    },
  },
};
</script>
