<template>
  <div class="answers-link-screen container mt-5">
    <h1 class="text-primary text-center">Sessão Criada</h1>

    <p class="text-center">
      Compartilhe este link com seu parceiro(a):
      <strong class="text-break">{{ sessionLink + "/devired_session/" }}</strong>
    </p>

    <div class="text-center mt-3">
      <!-- Botão para copiar o link -->
      <button 
        class="btn btn-secondary me-2" 
        @click="copyLink"
      >
        Copiar Link
      </button>

      <!-- Botão para compartilhar no WhatsApp -->
      <a 
        :href="whatsAppLink" 
        class="btn btn-success" 
        target="_blank" 
        rel="noopener noreferrer"
      >
        Compartilhar no WhatsApp
      </a>
    </div>

    <button class="btn btn-primary mt-4" @click="$emit('go-back')">
      Voltar para o Questionário
    </button>
  </div>
</template>

<script>
export default {
  props: {
    sessionLink: {
      type: String,
      required: true,
    },
  },
  computed: {
    whatsAppLink() {
      // Gera o link para compartilhar no WhatsApp
      const message = `Olá! Clique aqui para responder algumas perguntar sobre o nosso relacionamento: ${this.sessionLink}/derived_session`;
      return `https://wa.me/?text=${encodeURIComponent(message)}`;
    },
  },
  methods: {
    copyLink() {
      // Copia o link para a área de transferência
      navigator.clipboard.writeText(this.sessionLink + "/derived_session/").then(
        () => {
          alert("Link copiado para a área de transferência!");
        },
        (error) => {
          console.error("Erro ao copiar o link:", error);
          alert("Não foi possível copiar o link.");
        }
      );
    },
  },
};
</script>

<style scoped>
.answers-link-screen {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
}
</style>
