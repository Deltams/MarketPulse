import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import HomeView from '../views/HomeView.vue';
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
import CartView from '@/views/CartView.vue';
import ProductManagementView from '@/views/ProductManagementView.vue';

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/catalog', name: 'catalog', component: CatalogView },
  { path: '/about', name: 'about', component: AboutView },
  { path: '/categories', name: 'categories', component: CategoriesView },
  { path: '/category/:id', name: 'category', component: CategoryView },
  { path: '/category/:slug', name: 'category-by-slug', component: CategoryView },
  { path: '/brands', name: 'brands', component: BrandsView },
  { path: '/brands/:id', name: 'brand', component: BrandView },
  { path: '/products', name: 'products', component: ProductsView },
  { path: '/products/:id', name: 'product', component: ProductView },
  { path: '/login', name: 'login', component: LoginView, meta: { guest: true } },
  { path: '/register', name: 'register', component: () => import('../views/RegisterView.vue'), meta: { guest: true } },
  { path: '/profile', name: 'profile', component: UserProfileView },
  { path: '/cart', name: 'cart', component: CartView, meta: { requiresAuth: true } },
  { path: '/orders', name: 'orders', component: () => import('../views/OrdersView.vue'), meta: { requiresAuth: true } },
  { path: '/seller', name: 'seller', component: () => import('../views/SellerView.vue'), meta: { requiresAuth: true, requiresSeller: true } },
  { path: '/admin', name: 'admin', component: () => import('../views/AdminView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('../views/NotFoundView.vue') }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiresSeller = to.matched.some(record => record.meta.requiresSeller);
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin);
  const isGuestOnly = to.matched.some(record => record.meta.guest);

  if (authStore.token) {
    await authStore.checkAuth();
  }

  if (requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } });
  } else if (requiresSeller && !authStore.isSeller) {
    next({ name: 'home' });
  } else if (requiresAdmin && !authStore.isAdmin) {
    next({ name: 'home' });
  } else if (isGuestOnly && authStore.isAuthenticated) {
    next({ name: 'home' });
  } else {
    next();
  }
});

export default router;