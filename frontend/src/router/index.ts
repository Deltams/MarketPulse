import { createRouter, createWebHistory } from 'vue-router';
import CatalogView from '../views/CatalogView.vue';

const routes = [
  { path: '/', name: 'catalog', component: CatalogView },
  // Добавь другие маршруты позже
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;