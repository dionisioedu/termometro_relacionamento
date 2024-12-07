<template>
  <div id="app">
    <QuestionsList />
  </div>
</template>

<script>
import QuestionsList from './components/QuestionsList.vue';

export default {
  name: 'App',
  components: {
    QuestionsList, // Registra o componente
  },
};
</script>
