<template>
  <div class="service-filter">
    <v-card class="filter-card" elevation="2">
      <v-card-title class="filter-title">
        <v-icon class="mr-2">mdi-filter</v-icon>
        Фильтры услуг
      </v-card-title>
      
      <v-card-text class="filter-content">
        <v-row class="filter-row" justify="space-between" align="center" no-gutters>
          <!-- Поиск -->
          <v-col class="filter-col" style="width: 320px; min-width: 260px;">
            <v-text-field
              v-model="filters.search"
              placeholder="Поиск услуг"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="compact"
              clearable
              hide-details
              @update:model-value="applyFilters"
              class="custom-field search-field"
            />
          </v-col>
          
          <!-- Категория -->
          <v-col class="filter-col" style="width: 320px; min-width: 260px;">
            <v-select
              v-model="filters.category"
              :items="categories"
              item-title="name"
              item-value="id"
              placeholder="Категория услуг"
              prepend-inner-icon="mdi-tag"
              variant="outlined"
              density="compact"
              clearable
              hide-details
              :loading="loadingCategories"
              :disabled="loadingCategories"
              @update:model-value="applyFilters"
              @update:menu="val => categoryMenuOpen = val"
              class="custom-field"
            />
          </v-col>
          
          <!-- Сортировка по цене -->
          <v-col class="filter-col" style="width: 320px; min-width: 260px;">
            <v-select
              v-model="filters.priceSort"
              :items="priceOptions"
              item-title="title"
              item-value="value"
              placeholder="Сортировка по цене"
              prepend-inner-icon="mdi-currency-rub"
              variant="outlined"
              density="compact"
              clearable
              hide-details
              :menu-props="{ contentClass: 'custom-select-menu' }"
              @update:model-value="applyFilters"
              @update:menu="val => priceSortMenuOpen = val"
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
                color="#9c27b0"
                track-color="grey-lighten-2"
                @update:model-value="applyFilters"
                @start="handlePriceSliderStart"
                @end="handlePriceSliderEnd"
              >
                <template #thumb-label="{ modelValue }">
                  {{ formatPrice(modelValue) }} ₽
                </template>
              </v-range-slider>
              <div class="price-range-inputs">
                <div class="price-input-group">
                  <span class="price-label">От</span>
                  <v-text-field
                    v-model="priceFromInput"
                    variant="outlined"
                    density="compact"
                    type="number"
                    min="0"
                    max="999999"
                    step="100"
                    suffix="₽"
                    hide-details
                    @update:model-value="handlePriceFromChange"
                    @blur="validatePriceFrom"
                    class="price-input"
                  />
                </div>
                <div class="price-input-group">
                  <span class="price-label">До</span>
                  <v-text-field
                    v-model="priceToInput"
                    variant="outlined"
                    density="compact"
                    type="number"
                    min="0"
                    max="999999"
                    step="100"
                    suffix="₽"
                    hide-details
                    @update:model-value="handlePriceToChange"
                    @blur="validatePriceTo"
                    class="price-input"
                  />
                </div>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted } from 'vue'
import api from '@/api/config'

interface Filters {
  search: string
  category: number | null
  priceSort: string | null
  priceRange: [number, number]
}

interface Category {
  id: number
  name: string
}

const emit = defineEmits(['filter-change', 'price-slider-start', 'price-slider-end'])

const filters = reactive<Filters>({
  search: '',
  category: null,
  priceSort: null,
  priceRange: [0, 999999]
})

const categories = ref<Category[]>([])
const loadingCategories = ref(false)
const categoryMenuOpen = ref(false)
const priceSortMenuOpen = ref(false)

// Поля для ручного ввода цен
const priceFromInput = ref('0')
const priceToInput = ref('999999')

const priceOptions = [
  { title: 'По возрастанию', value: 'asc' },
  { title: 'По убыванию', value: 'desc' }
]

const fetchCategories = async () => {
  loadingCategories.value = true
  try {
    const response = await api.get('/service-categories/')
    categories.value = response.data.results
  } catch (error) {
    console.error('Error fetching service categories:', error)
    // Если не удалось загрузить категории, используем пустой массив
    categories.value = []
  } finally {
    loadingCategories.value = false
  }
}

const applyFilters = () => {
  emit('filter-change', { ...filters })
}

const handlePriceSliderStart = () => {
  emit('price-slider-start')
}

const handlePriceSliderEnd = () => {
  emit('price-slider-end')
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU').format(price)
}

const handlePriceFromChange = (value: string) => {
  const numValue = parseInt(value) || 0
  if (numValue >= 0 && numValue <= 999999) {
    filters.priceRange[0] = numValue
    applyFilters()
  }
}

const handlePriceToChange = (value: string) => {
  const numValue = parseInt(value) || 999999
  if (numValue >= 0 && numValue <= 999999) {
    filters.priceRange[1] = numValue
    applyFilters()
  }
}

const validatePriceFrom = () => {
  const numValue = parseInt(priceFromInput.value) || 0
  if (numValue < 0) {
    priceFromInput.value = '0'
    filters.priceRange[0] = 0
  } else if (numValue > 999999) {
    priceFromInput.value = '999999'
    filters.priceRange[0] = 999999
  } else {
    priceFromInput.value = numValue.toString()
    filters.priceRange[0] = numValue
  }
  
  // Проверяем, чтобы "от" не было больше "до"
  if (filters.priceRange[0] > filters.priceRange[1]) {
    filters.priceRange[1] = filters.priceRange[0]
    priceToInput.value = filters.priceRange[1].toString()
  }
  
  applyFilters()
}

const validatePriceTo = () => {
  const numValue = parseInt(priceToInput.value) || 999999
  if (numValue < 0) {
    priceToInput.value = '0'
    filters.priceRange[1] = 0
  } else if (numValue > 999999) {
    priceToInput.value = '999999'
    filters.priceRange[1] = 999999
  } else {
    priceToInput.value = numValue.toString()
    filters.priceRange[1] = numValue
  }
  
  // Проверяем, чтобы "до" не было меньше "от"
  if (filters.priceRange[1] < filters.priceRange[0]) {
    filters.priceRange[0] = filters.priceRange[1]
    priceFromInput.value = filters.priceRange[0].toString()
  }
  
  applyFilters()
}

// Синхронизация полей ввода со слайдером
watch(() => filters.priceRange, (newRange) => {
  priceFromInput.value = newRange[0].toString()
  priceToInput.value = newRange[1].toString()
}, { deep: true })

// Автоматическое применение фильтров при изменении
watch(filters, () => {
  applyFilters()
}, { deep: true })

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.service-filter {
  width: 100%;
}

.filter-card {
  border-radius: 12px;
  background: #fff;
  width: 100%;
}

.filter-title {
  background: linear-gradient(90deg, #9c27b0 0%, #673ab7 100%);
  color: white;
  border-radius: 12px 12px 0 0;
  padding: 1rem 1.5rem;
}

.filter-content {
  padding: 1.5rem;
}

.filter-row {
  margin-top: 16px;
  padding-top: 8px;
  margin-bottom: 1.5rem;
  gap: 8px;
}

.filter-col {
  display: flex;
  align-items: center;
  justify-content: center;
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

.price-range-inputs {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.01rem;
  justify-content: space-between;
}

.price-input-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
  max-width: 200px;
}

.price-input-group:last-child {
  justify-content: flex-end;
}

.price-label {
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
  min-width: 25px;
}

.price-input {
  flex: 1;
}

.price-separator {
  font-size: 1.2rem;
  font-weight: 600;
  color: #666;
  margin: 0 0.5rem;
}

.v-range-slider {
  margin-top: 1rem;
}

@media (max-width: 1100px) {
  .filter-row {
    flex-wrap: wrap;
    gap: 1rem;
  }
  .filter-col {
    width: 100% !important;
    min-width: 0 !important;
    margin-bottom: 1rem;
  }
}

@media (max-width: 768px) {
  .filter-content {
    padding: 1rem;
  }
  
  .price-range {
    padding: 0.75rem;
  }
  
  .price-range-inputs {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .price-input-group {
    max-width: 100%;
  }
  
  .price-separator {
    display: none;
  }
}

:deep(.custom-field) {
  background: #fff;
}
:deep(.custom-field:hover) {
  background: #fff;
}
:deep(.custom-field .v-field) {
  border: 2px solid #9c27b0 !important;
  border-radius: 8px;
  box-shadow: none !important;
  background: #fff;
  height: 40px !important;
  min-height: 40px !important;
  max-height: 40px !important;
}
:deep(.custom-field .v-field--focused) {
  border-color: #9c27b0;
  box-shadow: 0 0 0 2px rgba(156, 39, 176, 0.1);
}
:deep(.custom-field .v-field__input) {
  padding-top: 6px !important;
  padding-bottom: 6px !important;
  color: #222 !important;
  font-weight: 500;
  min-height: 28px !important;
  max-height: 28px !important;
}
:deep(.custom-field .v-label) {
  color: #6b7280 !important;
  font-weight: 500;
  letter-spacing: 0.02em;
}
:deep(.custom-field .v-field--focused .v-label) {
  color: #9c27b0 !important;
}
:deep(.custom-field .v-icon) {
  color: #6b7280;
  opacity: 0.8;
}
:deep(.custom-field .v-field--focused .v-icon) {
  color: #9c27b0;
}
:deep(.v-menu .v-list .v-list-item-title) {
  color: #222 !important;
  opacity: 1 !important;
}
:deep(.v-menu .v-list .v-list-item) {
  color: #222 !important;
  opacity: 1 !important;
}
:deep(.v-field) {
  border-radius: 8px;
}

:deep(.search-field .v-field) {
  height: 40px !important;
  min-height: 40px !important;
  max-height: 40px !important;
}
:deep(.search-field .v-field__input) {
  padding-top: 0px !important;
  padding-bottom: 0px !important;
  min-height: 36px !important;
  max-height: 36px !important;
  line-height: 24px !important;
  display: flex !important;
  align-items: center !important;
}

:deep(.v-menu__content) {
  background: #fff !important;
}
:deep(.v-menu .v-list .v-list-item-title) {
  color: #9c27b0 !important;
  opacity: 1 !important;
}
:deep(.v-menu .v-list .v-list-item) {
  color: #9c27b0 !important;
  opacity: 1 !important;
}

:deep(.custom-field .v-select__selection) {
  max-height: 20px !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
}
:deep(.custom-field .v-select__selection-text) {
  max-height: 20px !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
}

:deep(.custom-field .v-field__placeholder) {
  color: #6b7280 !important;
  opacity: 1 !important;
  font-weight: 500;
  letter-spacing: 0.02em;
}

/* Стили для полей ввода цен */
:deep(.price-input .v-field) {
  border: 2px solid #9c27b0 !important;
  border-radius: 8px;
  box-shadow: none !important;
  background: #fff;
  height: 40px !important;
  min-height: 40px !important;
  max-height: 40px !important;
}
:deep(.price-input .v-field--focused) {
  border-color: #9c27b0;
  box-shadow: 0 0 0 2px rgba(156, 39, 176, 0.1);
}
:deep(.price-input .v-field__input) {
  padding-top: 0px !important;
  padding-bottom: 0px !important;
  color: #222 !important;
  font-weight: 500;
  min-height: 36px !important;
  max-height: 36px !important;
  line-height: 24px !important;
  display: flex !important;
  align-items: center !important;
}
:deep(.price-input .v-label) {
  color: #6b7280 !important;
  font-weight: 500;
  letter-spacing: 0.02em;
}
:deep(.price-input .v-field--focused .v-label) {
  color: #9c27b0 !important;
}
:deep(.price-input .v-field__suffix) {
  color: #6b7280;
  font-weight: 500;
}
</style> 