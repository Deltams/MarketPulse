<template>
  <AppLayout>
    <router-view></router-view>
  </AppLayout>
</template>

<script setup lang="ts">
import AppLayout from './components/AppLayout.vue';
</script>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: linear-gradient(-45deg, #f0f4f8, hsl(210, 100%, 76%), #d8e1e8, hsl(205, 44%, 16%));
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
  min-height: 100vh;
}

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

#app {
  min-height: 100vh;
}

.v-application {
  background: transparent !important;
}

.v-application__wrap {
  background: transparent !important;
}

.v-main {
  background: transparent !important;
}

.v-card {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(10px);
}

.v-container {
  background: transparent !important;
}

.v-sheet {
  background: transparent !important;
}

.v-navigation-drawer {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(10px);
}

.v-list {
  background: transparent !important;
}

.v-list-item {
  background: transparent !important;
}

.v-text-field {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(10px);
}

.v-field__input {
  background: transparent !important;
}
</style>