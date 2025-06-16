<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" class="text-center">
        <h1 class="text-h2 mb-4">404</h1>
        <p class="text-h5 mb-6">Страница не найдена</p>
        <BaseButton
          color="primary"
          variant="elevated"
          @click="$router.push('/')"
        >
          Вернуться на главную
        </BaseButton>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import BaseButton from '../components/common/BaseButton.vue'
</script> 