import { createRouter, createWebHistory } from 'vue-router';
import UserQuestionnaire from './components/UserQuestionnaire.vue';
import DerivedSession from './components/DerivedSession.vue';

const routes = [
  {
    path: '/',
    component: UserQuestionnaire,
  },
  {
    path: '/derived_session/:sessionId',
    component: DerivedSession,
    props: true, // Passa o `sessionId` como prop para o componente
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
