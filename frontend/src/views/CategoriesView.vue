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
        :cols="categories.length === 1 ? 12 : 12"
        :sm="categories.length === 1 ? 12 : 6"
        :md="categories.length === 1 ? 12 : 6"
        :lg="categories.length === 1 ? 12 : 6"
        class="d-flex"
      >
        <v-card
          class="category-card h-100 w-100"
          :to="`/category/${category.id}`"
          hover
        >
          <v-card-title class="category-title">
            {{ category.name }}
          </v-card-title>
          <v-card-text>
            <div class="category-description">
              {{ category.description }}
            </div>
          </v-card-text>
          <v-card-actions class="category-card-actions">
            <v-btn
              block
              class="category-btn"
              :to="`/category/${category.id}`"
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
    const data = Array.isArray(response.data) ? response.data : response.data.results;
    categories.value = (data || []).filter((c: any) => c && typeof c.id === 'number');
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
/* Стилизация карточки категории под стиль карточки бренда */
.category-card {
  background: #fff !important;
  box-shadow: 0 4px 16px rgba(0,0,0,0.10), 0 1.5px 4px rgba(0,0,0,0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s;
  border-radius: 16px;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
  will-change: transform;
  border: 2px solid transparent;
}
.category-card:hover {
  transform: translateY(-4px) scale(1.01);
  box-shadow: 0 8px 32px rgba(25, 118, 210, 0.25), 0 3px 8px rgba(0,0,0,0.10);
  border-color: #1976d2;
}
.category-title {
  color: #222;
  font-size: 1.2rem;
  font-weight: 600;
  text-align: center;
  margin-top: 12px;
  margin-bottom: 0;
  line-height: 1.3;
  word-break: break-word;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
.category-description {
  color: #6b7280;
  font-size: 1rem;
  text-align: center;
  margin: 12px 0 0 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
.category-card-actions {
  padding: 8px 16px 16px;
  margin-top: auto;
}
.category-btn {
  background: linear-gradient(90deg, #1976d2 0%, #42a5f5 100%);
  color: #fff !important;
  font-weight: 700;
  font-size: 0.95rem;
  height: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.08);
  transition: background 0.2s, box-shadow 0.2s;
}
.category-btn:hover {
  background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%);
  box-shadow: 0 4px 16px rgba(25, 118, 210, 0.16);
}
</style>