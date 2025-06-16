<template>
  <v-card class="product-filter mb-4">
    <v-card-text>
      <v-row>
        <v-col cols="12" md="6">
          <BaseInput
            v-model="searchQuery"
            label="Поиск товаров"
            prepend-icon="mdi-magnify"
            clearable
            @update:model-value="handleSearch"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-row>
            <v-col cols="6">
              <BaseInput
                v-model.number="minPrice"
                label="Мин. цена"
                type="number"
                prepend-icon="mdi-currency-rub"
                @update:model-value="handleFilter"
              />
            </v-col>
            <v-col cols="6">
              <BaseInput
                v-model.number="maxPrice"
                label="Макс. цена"
                type="number"
                prepend-icon="mdi-currency-rub"
                @update:model-value="handleFilter"
              />
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <v-row class="mt-2">
        <v-col cols="12">
          <v-chip-group
            v-model="selectedCategories"
            multiple
            @update:model-value="handleFilter"
          >
            <v-chip
              v-for="category in categories"
              :key="category.id"
              :value="category.id"
              filter
              variant="outlined"
            >
              {{ category.name }}
            </v-chip>
          </v-chip-group>
        </v-col>
      </v-row>

      <v-row class="mt-2">
        <v-col cols="12" class="d-flex justify-end">
          <BaseButton
            color="secondary"
            variant="text"
            size="small"
            @click="resetFilters"
          >
            Сбросить фильтры
          </BaseButton>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import BaseInput from '../common/BaseInput.vue'
import BaseButton from '../common/BaseButton.vue'

const props = defineProps({
  categories: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['filter'])

const searchQuery = ref('')
const minPrice = ref<number | null>(null)
const maxPrice = ref<number | null>(null)
const selectedCategories = ref<number[]>([])

let searchTimeout: number | null = null

const handleSearch = () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  searchTimeout = window.setTimeout(() => {
    emitFilter()
  }, 300)
}

const handleFilter = () => {
  emitFilter()
}

const emitFilter = () => {
  emit('filter', {
    search: searchQuery.value,
    minPrice: minPrice.value,
    maxPrice: maxPrice.value,
    categories: selectedCategories.value
  })
}

const resetFilters = () => {
  searchQuery.value = ''
  minPrice.value = null
  maxPrice.value = null
  selectedCategories.value = []
  emitFilter()
}

watch(() => props.categories, (newCategories) => {
  if (newCategories.length === 0) {
    selectedCategories.value = []
  }
})
</script>

<style scoped>
.product-filter {
  background-color: var(--v-theme-surface);
}
</style> 