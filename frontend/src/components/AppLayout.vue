<template>
  <v-app>
    <v-app-bar color="primary" density="compact" elevation="1">
      <v-container class="d-flex align-center">
        <v-app-bar-title>
          <router-link to="/" class="text-decoration-none text-white">
            MarketPulse
          </router-link>
        </v-app-bar-title>

        <v-spacer></v-spacer>

        <v-btn-group class="d-none d-md-flex">
          <v-btn to="/categories" variant="text" color="white">
            Категории
          </v-btn>
          <v-btn to="/brands" variant="text" color="white">
            Бренды
          </v-btn>
          <v-btn to="/products" variant="text" color="white">
            Товары
          </v-btn>
          <v-btn to="/services" variant="text" color="white">
            Услуги
          </v-btn>
          <v-btn to="/about" variant="text" color="white">
            О нас
          </v-btn>
        </v-btn-group>

        <v-spacer></v-spacer>

        <div class="d-flex align-center">
          <CartWidget />
          <v-btn to="/login" variant="text" color="white" class="ml-2">
            Войти
          </v-btn>
          <v-btn v-if="isAuthenticated" to="/profile" variant="text" color="white">
            Профиль
          </v-btn>
        </div>

        <v-app-bar-nav-icon
          class="d-md-none"
          @click="drawer = !drawer"
        ></v-app-bar-nav-icon>
      </v-container>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" location="right" temporary>
      <v-list>
        <v-list-item to="/categories" title="Категории"></v-list-item>
        <v-list-item to="/brands" title="Бренды"></v-list-item>
        <v-list-item to="/products" title="Каталог"></v-list-item>
        <v-list-item to="/services" title="Услуги"></v-list-item>
        <v-list-item to="/about" title="О нас"></v-list-item>
        <v-divider></v-divider>
        <v-list-item @click="handleCartClick" title="Корзина">
          <template v-slot:prepend>
            <v-badge
              :content="cartStore.totalItems"
              :model-value="cartStore.totalItems > 0"
              color="error"
              location="top end"
            >
              <v-icon>mdi-cart</v-icon>
            </v-badge>
          </template>
        </v-list-item>
        <v-list-item to="/login" title="Войти"></v-list-item>
        <v-list-item v-if="isAuthenticated" to="/profile" title="Профиль"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid class="fill-height pa-4">
        <slot></slot>
      </v-container>
    </v-main>

    <v-footer app color="primary" class="text-center d-flex justify-center">
      <span class="text-white">&copy; {{ new Date().getFullYear() }} MarketPulse. Все права защищены.</span>
    </v-footer>

    <!-- Система уведомлений -->
    <NotificationSystem />
  </v-app>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import CartWidget from '@/components/cart/CartWidget.vue'
import NotificationSystem from '@/components/common/NotificationSystem.vue'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cartStore'
import { useNotificationStore } from '@/stores/notificationStore'

const router = useRouter()
const drawer = ref(false)
const authStore = useAuthStore()
const cartStore = useCartStore()
const notificationStore = useNotificationStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

const handleCartClick = () => {
  if (authStore.isAuthenticated) {
    router.push('/cart')
  } else {
    notificationStore.addNotification(
      'Для просмотра корзины необходимо войти в систему',
      'warning',
      5000
    )
  }
}
</script>

<style scoped>
.v-main {
  min-height: calc(100vh - 64px - 36px); /* viewport height - app bar - footer */
}

.v-container {
  max-width: none !important;
  padding: 0 24px !important;
}

@media (max-width: 600px) {
  .v-container {
    padding: 0 16px !important;
  }
}
</style>