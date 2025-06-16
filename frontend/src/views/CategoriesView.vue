<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-6">Категории</h1>
      </v-col>
    </v-row>

    <v-row v-if="loading">
      <v-col cols="12" class="text-center">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
        <div class="text-h6 mt-4">Загрузка категорий...</div>
      </v-col>
    </v-row>

    <v-row v-else-if="error">
      <v-col cols="12">
        <v-alert
          type="error"
          variant="tonal"
          class="mb-4"
        >
          {{ error }}
        </v-alert>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col
        v-for="category in categories"
        :key="category.id"
        cols="12"
        sm="6"
        md="6"
        lg="6"
      >
        <v-card
          class="h-100"
          :to="`/category/${category.id}`"
          hover
        >
          <v-card-title class="text-h6">
            {{ category.name }}
          </v-card-title>

          <v-card-text>
            <p class="text-body-2 text-medium-emphasis">
              {{ category.description }}
            </p>
          </v-card-text>

          <v-card-actions>
            <v-btn
              block
              color="primary"
              variant="text"
              :to="`/category/${category.id}`"
              class="d-flex justify-center align-center"
            >
              Смотреть товары
              <v-icon end icon="mdi-arrow-right" class="ml-2"></v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../api/config';

interface Category {
  id: number;
  name: string;
  description: string;
}

const categories = ref<Category[]>([]);
const loading = ref(true);
const error = ref('');

const fetchCategories = async () => {
  try {
    const response = await api.get('/categories/');
    categories.value = response.data;
  } catch (err) {
    error.value = 'Не удалось загрузить категории';
    console.error('Error fetching categories:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchCategories();
});
</script>

<style scoped>
/* Styles are now handled by Vuetify components */
</style>