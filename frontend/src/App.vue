<template>
  <div id="app">
    <WelcomeScreen @user-entered="setUserName" v-if="!userName" />
    <NextComponent v-else :userName="userName" />
  </div>
</template>

<script>
import WelcomeScreen from "./components/WelcomeScreen.vue";

export default {
  data() {
    return {
      userName: null, // Estado para armazenar o nome
    };
  },
  components: {
    WelcomeScreen,
  },
  methods: {
    setUserName(name) {
      this.userName = name;
    },
  },
};
</script>
