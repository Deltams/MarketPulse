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
}

#app {
  min-height: 100vh;
}
</style>