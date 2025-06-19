<template>
  <div class="products-page">
    <!-- Фильтрация - растягиваем на всю ширину -->
    <div class="filter-section">
      <div class="container">
        <ProductFilter @filter-change="handleFilterChange" />
      </div>
    </div>
    
    <div class="products-container">
      <div v-if="loading" class="loading">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
        <div class="loading-text">Загрузка...</div>
      </div>
      
      <div v-else-if="error" class="error">
        <v-alert type="error" variant="tonal">
          {{ error }}
        </v-alert>
      </div>
      
      <div v-else>
        <!-- Результаты поиска -->
        <div class="results-info">
          <v-chip color="primary" variant="tonal">
            Найдено: {{ filteredProducts.length }} товаров
          </v-chip>
        </div>
        
        <!-- Список товаров -->
        <div class="products-list">
          <ProductCard
            v-for="product in filteredProducts"
            :key="product.id"
            :product="product"
            class="product-list-item"
          />
        </div>
        
        <!-- Сообщение если ничего не найдено -->
        <div v-if="filteredProducts.length === 0" class="no-results">
          <v-card class="no-results-card" variant="tonal">
            <v-card-text class="text-center">
              <v-icon size="64" color="grey" class="mb-4">mdi-package-variant-closed</v-icon>
              <h3>Товары не найдены</h3>
              <p>Попробуйте изменить параметры поиска</p>
            </v-card-text>
          </v-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useProductStore } from '@/stores/productStore'
import { useNotificationStore } from '@/stores/notificationStore'
import ProductCard from '@/components/products/ProductCard.vue'
import ProductFilter from '@/components/products/ProductFilter.vue'

const productStore = useProductStore()
const notificationStore = useNotificationStore()

// Фильтры
const filters = ref({
  search: '',
  category: '',
  priceSort: '',
  priceRange: [0, 50000]
})

const loading = computed(() => productStore.loading)
const error = computed(() => productStore.error)

// Фильтрация товаров
const filteredProducts = computed(() => {
  let products = productStore.products

  // Фильтр по поиску
  if (filters.value.search) {
    const searchLower = filters.value.search.toLowerCase()
    products = products.filter(product => 
      product.name.toLowerCase().includes(searchLower) ||
      product.description.toLowerCase().includes(searchLower)
    )
  }

  // Фильтр по категории
  if (filters.value.category) {
    products = products.filter(product => 
      product.category === filters.value.category
    )
  }

  // Фильтр по цене
  products = products.filter(product => 
    product.price >= filters.value.priceRange[0] && 
    product.price <= filters.value.priceRange[1]
  )

  // Сортировка по цене
  if (filters.value.priceSort === 'asc') {
    products.sort((a, b) => a.price - b.price)
  } else if (filters.value.priceSort === 'desc') {
    products.sort((a, b) => b.price - a.price)
  }

  return products
})

const handleFilterChange = (newFilters: any) => {
  filters.value = { ...filters.value, ...newFilters }
}

onMounted(async () => {
  try {
    await productStore.fetchProducts()
  } catch (err) {
    console.error('Error fetching products:', err)
  }
})
</script>

<style scoped>
.products-page {
  width: 100vw;
  min-height: 100vh;
  background: #f5f5f5;
  margin-left: calc(-50vw + 50%);
  margin-right: calc(-50vw + 50%);
}

.filter-section {
  background: #fff;
  border-bottom: 1px solid #e0e0e0;
  padding: 1rem 0;
  margin-bottom: 2rem;
}

.container {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 1rem;
}

.products-container {
  padding: 0 1rem;
  width: 100%;
}

.results-info {
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1600px;
  margin-left: auto;
  margin-right: auto;
}

.products-list {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 2rem;
  width: 100%;
  max-width: 1800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.product-list-item {
  width: 100%;
  max-width: none;
}

.loading {
  text-align: center;
  padding: 4rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-text {
  color: #666;
  font-size: 1.1rem;
}

.error {
  margin: 2rem 0;
}

.no-results {
  margin: 2rem 0;
}

.no-results-card {
  max-width: 400px;
  margin: 0 auto;
  text-align: center;
}

.no-results-card h3 {
  margin-bottom: 1rem;
  color: #333;
}

.no-results-card p {
  color: #666;
}

/* Переопределяем ограничения Vuetify */
:deep(.v-container) {
  max-width: none !important;
  width: 100% !important;
}

:deep(.v-container--fluid) {
  max-width: none !important;
  width: 100% !important;
}

@media (max-width: 1600px) {
  .products-list {
    grid-template-columns: repeat(5, 1fr);
  }
}
@media (max-width: 1300px) {
  .products-list {
    grid-template-columns: repeat(4, 1fr);
  }
}
@media (max-width: 1000px) {
  .products-list {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 700px) {
  .products-list {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 500px) {
  .products-list {
    grid-template-columns: 1fr;
  }
}
</style>