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
            Товары/Услуги?
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
        <v-list-item to="/products" title="Товары/Услуги?"></v-list-item>
        <v-list-item to="/about" title="О нас"></v-list-item>
        <v-divider></v-divider>
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
  </v-app>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import CartWidget from '@/components/cart/CartWidget.vue'
import { useAuthStore } from '@/stores/auth'

const drawer = ref(false)
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>

<style scoped>
.v-main {
  min-height: calc(100vh - 64px - 36px); /* viewport height - app bar - footer */
}

.v-container {
  max-width: 1920px !important;
  padding: 0 24px !important;
}

@media (max-width: 600px) {
  .v-container {
    padding: 0 16px !important;
  }
}
</style>