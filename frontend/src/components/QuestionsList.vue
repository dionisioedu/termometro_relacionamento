<template>
  <div>
    <h1>Questions</h1>
    <ul>
      <li v-for="question in questions" :key="question.id">
        {{ question.text }}
      </li>
    </ul>
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import api from '../api'; // Importa a instância do Axios configurada

export default {
  name: 'QuestionsList',
  data() {
    return {
      questions: [], // Armazena as perguntas
      loading: false, // Indica se os dados estão carregando
      error: null, // Armazena mensagens de erro, se houver
    };
  },
  mounted() {
    this.fetchQuestions(); // Busca as perguntas ao montar o componente
  },
  methods: {
    async fetchQuestions() {
      this.loading = true; // Ativa o indicador de carregamento
      this.error = null; // Limpa erros anteriores
      try {
        const response = await api.get('questions/'); // Faz a requisição
        this.questions = response.data; // Armazena as perguntas no estado
      } catch (err) {
        this.error = 'Failed to load questions'; // Define a mensagem de erro
        console.error(err); // Loga o erro no console
      } finally {
        this.loading = false; // Desativa o indicador de carregamento
      }
    },
  },
};
</script>

<style scoped>
/* Estilo básico para o componente */
.error {
  color: red;
}
</style>
