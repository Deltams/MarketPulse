<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-6">Бренды</h1>
      </v-col>
    </v-row>

    <v-row v-if="loading">
      <v-col cols="12" class="text-center">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
        <div class="text-h6 mt-4">Загрузка брендов...</div>
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
        v-for="brand in brands"
        :key="brand.id"
        :cols="brands.length === 1 ? 12 : 12"
        :sm="brands.length === 1 ? 12 : 6"
        :md="brands.length === 1 ? 12 : 6"
        :lg="brands.length === 1 ? 12 : 6"
        class="d-flex"
      >
        <v-card
          class="h-100 w-100"
          :to="`/brands/${brand.id}`"
          hover
        >
          <v-card-title class="text-h6">
            {{ brand.name }}
          </v-card-title>

          <v-card-text>
            <p class="text-body-2 text-medium-emphasis">
              {{ brand.description }}
            </p>
          </v-card-text>

          <v-card-actions>
            <v-btn
              block
              color="primary"
              variant="text"
              :to="`/brands/${brand.id}`"
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

interface Brand {
  id: number;
  name: string;
  description: string;
}

const brands = ref<Brand[]>([]);
const loading = ref(true);
const error = ref('');

const fetchBrands = async () => {
  try {
    const response = await api.get('/brandlist/');
    brands.value = [
      ...response.data,
      // {
      //   id: 999,
      //   name: 'Тестовый бренд 1',
      //   description: 'Это тестовый бренд для проверки отображения сетки. Здесь должно быть достаточно текста, чтобы проверить, как он помещается в карточке.'
      // },
      // {
      //   id: 998,
      //   name: 'Тестовый бренд 2',
      //   description: 'Еще один тестовый бренд с длинным описанием для проверки того, как сетка адаптируется под разное количество контента в карточках.'
      // }
    ];
  } catch (err) {
    error.value = 'Не удалось загрузить бренды';
    console.error('Error fetching brands:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchBrands();
});
</script>

<style scoped>
/* Styles are now handled by Vuetify components */
</style>