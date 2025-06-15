import { createRouter, createWebHistory } from 'vue-router';
import CatalogView from '../views/CatalogView.vue';
import ProductView from '../views/ProductView.vue';
import LoginView from '../views/LoginView.vue';
import AboutView from '../views/AboutView.vue';
import CategoriesView from '../views/CategoriesView.vue';
import CategoryView from '../views/CategoryView.vue';
import BrandsView from '../views/BrandsView.vue';
import BrandView from '../views/BrandView.vue';
import ProductsView from '../views/ProductsView.vue';
import UserProfileView from '../views/UserProfileView.vue';

const routes = [
  { path: '/', name: 'catalog', component: CatalogView },
  { path: '/about', name: 'about', component: AboutView },
  { path: '/categories', name: 'categories', component: CategoriesView },
  { path: '/category/:id', name: 'category', component: CategoryView },
  { path: '/category/:slug', name: 'category-by-slug', component: CategoryView },
  { path: '/brands', name: 'brands', component: BrandsView },
  { path: '/brands/:id', name: 'brand', component: BrandView },
  { path: '/products', name: 'products', component: ProductsView },
  { path: '/products/:id', name: 'product', component: ProductView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/profile', name: 'profile', component: UserProfileView },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;