import { createRouter, createWebHistory } from 'vue-router';
import UserQuestionnaire from './components/UserQuestionnaire.vue';
import DerivedSession from './components/DerivedSession.vue';
import SessionAnswers from './components/SessionAnswers.vue';
import SessionAnswersWithLink from './components/SessionAnswersWithLink.vue';
import ResultsView from './components/ResultsView.vue';

const routes = [
  {
    path: '/',
    name: 'UserQuestionnaire',
    component: UserQuestionnaire,
    props: (route) => ({
      originSessionId: route.query.originSessionId || null, // Passa o originSessionId como query (nulo se não existir)
      isDerivedSession: route.query.isDerivedSession === "true", // Passa o isDerivedSession como parâmetro (falso se não existir)
      originCreatorName: route.query.originCreatorName || null, // Passa o originCreatorName como query (nulo se não existir)
    }),
  },
  {
    path: '/session/:sessionId/derived_session',
    name: 'DerivedSession',
    component: DerivedSession,
    props: true,
  },
  {
    path: '/session/:sessionId/answers',
    name: 'SessionAnswers',
    component: SessionAnswers,
    props: true,
  },
  {
    path: '/session/:sessionId/link',
    name: 'SessionAnswersWithLink',
    component: SessionAnswersWithLink,
    props: true,
  },
  {
    path: '/results',
    name: 'ResultsView',
    component: ResultsView,
    props: (route) => ({
      derivedSessionId: route.query.derivedSessionId || null, // Passa o derivedSessionId como query (nulo se não existir)
    }),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
