import { createRouter, createWebHistory } from 'vue-router';
import CatalogView from '../views/CatalogView.vue';
import ProductView from '../views/ProductView.vue';
import LoginView from '../views/LoginView.vue';

const routes = [
  { path: '/', name: 'catalog', component: CatalogView },
  { path: '/product/:id', name: 'product', component: ProductView },
  { path: '/login', name: 'login', component: LoginView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;