<template>
  <div class="product-filter">
    <v-card class="filter-card" elevation="2">
      <v-card-title class="filter-title">
        <v-icon class="mr-2">mdi-filter</v-icon>
        Фильтры товаров
      </v-card-title>
      
      <v-card-text class="filter-content">
        <v-row>
          <!-- Поиск -->
          <v-col cols="12" lg="3" md="6" style="margin-top: 16px;">
            <v-text-field
              v-model="filters.search"
              label="Поиск товаров"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="compact"
              clearable
              @update:model-value="applyFilters"
              class="custom-field"
            />
          </v-col>
          
          <!-- Категория -->
          <v-col cols="12" lg="3" md="6" style="margin-top: 16px;">
            <v-select
              v-model="filters.category"
              :items="categories"
              label="Категория"
              prepend-inner-icon="mdi-tag"
              variant="outlined"
              density="compact"
              clearable
              @update:model-value="applyFilters"
              class="custom-field"
            />
          </v-col>
          
          <!-- Сортировка по цене -->
          <v-col cols="12" lg="3" md="6" style="margin-top: 16px;">
            <v-select
              v-model="filters.priceSort"
              :items="priceOptions"
              label="Сортировка по цене"
              prepend-inner-icon="mdi-currency-rub"
              variant="outlined"
              density="compact"
              clearable
              @update:model-value="applyFilters"
              class="custom-field"
            />
          </v-col>
        </v-row>
        
        <!-- Диапазон цен -->
        <v-row>
          <v-col cols="12">
            <div class="price-range">
              <div class="price-range-label">
                <v-icon class="mr-1">mdi-currency-rub</v-icon>
                Диапазон цен
              </div>
              <v-range-slider
                v-model="filters.priceRange"
                :min="0"
                :max="999999"
                :step="100"
                thumb-label="always"
                color="primary"
                track-color="grey-lighten-2"
                @update:model-value="applyFilters"
              >
                <template #thumb-label="{ modelValue }">
                  {{ formatPrice(modelValue) }} ₽
                </template>
              </v-range-slider>
              <div class="price-range-values">
                <span>{{ formatPrice(filters.priceRange[0]) }} ₽</span>
                <span>{{ formatPrice(filters.priceRange[1]) }} ₽</span>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'

interface Filters {
  search: string
  category: string
  priceSort: string
  priceRange: [number, number]
}

const emit = defineEmits(['filter-change'])

const filters = reactive<Filters>({
  search: '',
  category: '',
  priceSort: '',
  priceRange: [0, 100000]
})

const categories = [
  'Электроника',
  'Одежда',
  'Книги',
  'Спорт',
  'Дом и сад',
  'Красота',
  'Игрушки',
  'Автотовары'
]

const priceOptions = [
  { title: 'По возрастанию', value: 'asc' },
  { title: 'По убыванию', value: 'desc' }
]

const applyFilters = () => {
  emit('filter-change', { ...filters })
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU').format(price)
}

// Автоматическое применение фильтров при изменении
watch(filters, () => {
  applyFilters()
}, { deep: true })
</script>

<style scoped>
.product-filter {
  width: 100%;
}

.filter-card {
  border-radius: 12px;
  background: #fff;
  width: 100%;
}

.filter-title {
  background: linear-gradient(90deg, #1976d2 0%, #42a5f5 100%);
  color: white;
  border-radius: 12px 12px 0 0;
  padding: 1rem 1.5rem;
}

.filter-content {
  padding: 1.5rem;
}

.price-range {
  margin-top: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.price-range-label {
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
  display: flex;
  align-items: center;
  font-size: 1rem;
}

.price-range-values {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
}

.v-range-slider {
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .filter-content {
    padding: 1rem;
  }
  
  .price-range {
    padding: 0.75rem;
  }
}

:deep(.custom-field) {
  background: #fff;
}
:deep(.custom-field:hover) {
  background: #fff;
}
:deep(.custom-field .v-field) {
  border: 2px solid #1976d2 !important;
  border-radius: 8px;
  box-shadow: none !important;
  background: #fff;
}
:deep(.custom-field .v-field--focused) {
  border-color: #1976d2;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.1);
}
:deep(.custom-field .v-field__input) {
  padding-top: 12px;
  padding-bottom: 12px;
  color: #222 !important;
  font-weight: 500;
}
:deep(.custom-field .v-label) {
  color: #6b7280 !important;
  font-weight: 500;
  letter-spacing: 0.02em;
}
:deep(.custom-field .v-field--focused .v-label) {
  color: #1976d2 !important;
}
:deep(.custom-field .v-icon) {
  color: #6b7280;
  opacity: 0.8;
}
:deep(.custom-field .v-field--focused .v-icon) {
  color: #1976d2;
}
:deep(.v-menu .v-list .v-list-item-title) {
  color: #222 !important;
}
:deep(.v-menu .v-list .v-list-item) {
  color: #222 !important;
}
</style> 