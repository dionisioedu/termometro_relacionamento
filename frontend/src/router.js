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
  },
  {
    path: '/session/:sessionId/questions',
    name: 'UserQuestionnaire',
    component: UserQuestionnaire,
    props: (route) => ({
      sessionId: route.params.sessionId,
      originSessionId: route.query.originSessionId || null, // Passa o originSessionId como query (nulo se não existir)
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
    path: '/results/:sessionId',
    name: 'ResultsView',
    component: ResultsView,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
