<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>MarketPulse</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn to="/">Каталог</v-btn>
      <v-btn to="/cart">Корзина</v-btn>
      <v-btn v-if="authStore.user" to="/profile">Профиль</v-btn>
      <v-btn v-if="authStore.user" @click="authStore.logout">Выйти</v-btn>
      <v-btn v-else to="/login">Войти</v-btn>
    </v-app-bar>
    <v-main>
      <v-container>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="js">
import { useAuthStore } from './stores/auth';
const authStore = useAuthStore();
</script>