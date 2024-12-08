<template>
  <div id="app">
    <UserQuestionnaire ser-entered="setUserName" v-if="!userName" />
    <NextComponent v-else :userName="userName" />
  </div>
</template>

<script>
import UserQuestionnaire from "./components/UserQuestionnaire.vue";

export default {
  data() {
    return {
      userName: null, // Estado para armazenar o nome
    };
  },
  components: {
    UserQuestionnaire,
  },
  methods: {
    setUserName(name) {
      this.userName = name;
    },
  },
};
</script>
