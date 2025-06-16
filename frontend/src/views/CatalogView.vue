<template>
  <div class="catalog">
    <!-- Header Section -->
    <div class="catalog-header">
      <div class="header-content">
        <h1 class="catalog-title">Каталог товаров</h1>
        <div class="catalog-controls">
          <v-text-field
            v-model="searchQuery"
            density="comfortable"
            variant="outlined"
            hide-details
            placeholder="Поиск товаров..."
            prepend-inner-icon="mdi-magnify"
            class="search-field"
            @update:model-value="handleSearch"
          ></v-text-field>
          <v-btn
            color="primary"
            variant="tonal"
            class="filter-btn"
            @click="toggleFilters"
          >
            <v-icon start icon="mdi-filter-variant"></v-icon>
            Фильтры
          </v-btn>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="catalog-content">
      <!-- Filters Sidebar -->
      <v-navigation-drawer
        v-model="isFiltersOpen"
        location="right"
        temporary
        width="320"
      >
        <v-list>
          <v-list-item>
            <template v-slot:prepend>
              <v-icon icon="mdi-filter-variant"></v-icon>
            </template>
            <v-list-item-title>Фильтры</v-list-item-title>
            <template v-slot:append>
              <v-btn
                icon="mdi-close"
                variant="text"
                @click="isFiltersOpen = false"
              ></v-btn>
            </template>
          </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list>
          <!-- Categories -->
          <v-list-item>
            <v-list-item-title class="text-subtitle-1 font-weight-medium mb-2">
              Категории
            </v-list-item-title>
            <v-list-item-subtitle>
              <v-chip-group
                v-model="selectedCategories"
                multiple
                column
                @update:model-value="handleCategoryChange"
              >
                <v-chip
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                  variant="outlined"
                  class="ma-1"
                >
                  {{ category.name }}
                </v-chip>
              </v-chip-group>
            </v-list-item-subtitle>
          </v-list-item>

          <v-divider class="my-2"></v-divider>

          <!-- Price Range -->
          <v-list-item>
            <v-list-item-title class="text-subtitle-1 font-weight-medium mb-2">
              Цена
            </v-list-item-title>
            <v-list-item-subtitle>
              <v-range-slider
                v-model="priceRange"
                :min="0"
                :max="maxPrice"
                :step="100"
                class="mt-4"
                @update:model-value="handlePriceChange"
              >
                <template v-slot:prepend>
                  {{ formatPrice(priceRange[0]) }}
                </template>
                <template v-slot:append>
                  {{ formatPrice(priceRange[1]) }}
                </template>
              </v-range-slider>
            </v-list-item-subtitle>
          </v-list-item>

          <v-divider class="my-2"></v-divider>

          <!-- Sort -->
          <v-list-item>
            <v-list-item-title class="text-subtitle-1 font-weight-medium mb-2">
              Сортировка
            </v-list-item-title>
            <v-list-item-subtitle>
              <v-select
                v-model="sortBy"
                :items="sortOptions"
                variant="outlined"
                density="comfortable"
                hide-details
                @update:model-value="handleSort"
              ></v-select>
            </v-list-item-subtitle>
          </v-list-item>
        </v-list>

        <template v-slot:append>
          <div class="pa-4">
            <v-btn
              block
              color="primary"
              variant="tonal"
              @click="clearFilters"
            >
              Сбросить фильтры
            </v-btn>
          </div>
        </template>
      </v-navigation-drawer>

      <!-- Products Grid -->
      <div class="products-container">
        <div v-if="loading" class="products-grid">
          <v-card
            v-for="n in 8"
            :key="n"
            class="product-card skeleton-card"
            flat
          >
            <v-skeleton-loader
              type="image"
              height="200"
            ></v-skeleton-loader>
            <v-skeleton-loader
              type="list-item-two-line"
              class="px-4 pt-4"
            ></v-skeleton-loader>
            <v-skeleton-loader
              type="button"
              class="px-4 pb-4"
            ></v-skeleton-loader>
          </v-card>
        </div>

        <div v-else-if="error" class="error-state">
          <v-alert
            type="error"
            variant="tonal"
            class="mb-4"
          >
            {{ error }}
          </v-alert>
        </div>

        <div v-else-if="filteredProducts.length === 0" class="empty-state">
          <v-icon
            size="64"
            color="grey"
            class="mb-4"
          >
            mdi-package-variant-closed
          </v-icon>
          <h3 class="text-h6 mb-2">Товары не найдены</h3>
          <p class="text-body-1 text-medium-emphasis">
            Попробуйте изменить параметры поиска
          </p>
        </div>

        <div v-else class="products-grid">
          <v-card
            v-for="product in filteredProducts"
            :key="product.id"
            class="product-card"
            :to="`/products/${product.id}`"
            hover
          >
            <v-img
              :src="product.image || '/placeholder.png'"
              :alt="product.name"
              height="200"
              cover
              class="product-image"
            >
              <template v-slot:placeholder>
                <v-row
                  class="fill-height ma-0"
                  align="center"
                  justify="center"
                >
                  <v-progress-circular
                    indeterminate
                    color="primary"
                  ></v-progress-circular>
                </v-row>
              </template>
            </v-img>

            <v-card-title class="product-title">
              {{ product.name }}
            </v-card-title>

            <v-card-text>
              <p class="text-body-2 text-medium-emphasis mb-2">
                {{ product.description }}
              </p>
              <p class="text-h6 text-primary mb-2">
                {{ formatPrice(product.price) }}
              </p>
            </v-card-text>

            <v-card-actions>
              <v-btn
                block
                color="primary"
                variant="tonal"
                @click.stop="addToCart(product)"
              >
                <v-icon start icon="mdi-cart-plus"></v-icon>
                В корзину
              </v-btn>
            </v-card-actions>
          </v-card>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination">
          <v-pagination
            v-model="currentPage"
            :length="totalPages"
            :total-visible="5"
            @update:model-value="handlePageChange"
          ></v-pagination>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useCartStore } from '@/stores/cartStore'
import api from '@/api/config'

const cartStore = useCartStore()

// State
const products = ref([])
const categories = ref([])
const loading = ref(true)
const error = ref('')
const searchQuery = ref('')
const selectedCategories = ref([])
const priceRange = ref([0, 100000])
const maxPrice = ref(100000)
const sortBy = ref('popular')
const currentPage = ref(1)
const totalPages = ref(1)
const isFiltersOpen = ref(false)
const isFirstLoad = ref(true)

// Sort options
const sortOptions = [
  { title: 'По популярности', value: 'popular' },
  { title: 'По возрастанию цены', value: 'price_asc' },
  { title: 'По убыванию цены', value: 'price_desc' },
  { title: 'По названию (А-Я)', value: 'name_asc' },
  { title: 'По названию (Я-А)', value: 'name_desc' }
]

// Computed
const filteredProducts = computed(() => {
  return products.value
})

// Methods
const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB'
  }).format(price)
}

const toggleFilters = () => {
  isFiltersOpen.value = !isFiltersOpen.value
}

const handleSearch = async () => {
  loading.value = true
  await new Promise(resolve => setTimeout(resolve, 1500))
  fetchProducts()
}

const handlePriceChange = async () => {
  loading.value = true
  await new Promise(resolve => setTimeout(resolve, 1500))
  fetchProducts()
}

const handleSort = async () => {
  loading.value = true
  await new Promise(resolve => setTimeout(resolve, 1500))
  fetchProducts()
}

const handlePageChange = async (page: number) => {
  currentPage.value = page
  loading.value = true
  await new Promise(resolve => setTimeout(resolve, 1500))
  fetchProducts()
}

const handleCategoryChange = async () => {
  loading.value = true
  await new Promise(resolve => setTimeout(resolve, 1500))
  fetchProducts()
}

const clearFilters = async () => {
  searchQuery.value = ''
  selectedCategories.value = []
  priceRange.value = [0, maxPrice.value]
  sortBy.value = 'popular'
  loading.value = true
  await new Promise(resolve => setTimeout(resolve, 1500))
  fetchProducts()
}

const addToCart = (product: any) => {
  cartStore.addItem(product)
}

const fetchProducts = async () => {
  try {
    // Add artificial delay for first load
    if (isFirstLoad.value) {
      await new Promise(resolve => setTimeout(resolve, 3000))
      isFirstLoad.value = false
    }

    const params: Record<string, any> = {
      search: searchQuery.value,
      min_price: priceRange.value[0],
      max_price: priceRange.value[1],
      sort: sortBy.value,
      page: currentPage.value
    }

    // Add each category as a separate parameter
    if (selectedCategories.value.length > 0) {
      selectedCategories.value.forEach((categoryId, index) => {
        params[`category_${index}`] = categoryId
      })
    }

    const response = await api.get('/productlist/', { params })
    products.value = response.data.results || response.data
    totalPages.value = Math.ceil(response.data.count / 12) || 1
  } catch (err) {
    error.value = 'Не удалось загрузить товары'
    console.error('Error fetching products:', err)
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const response = await api.get('/categories/')
    categories.value = response.data
  } catch (err) {
    console.error('Error fetching categories:', err)
  }
}

onMounted(() => {
  fetchProducts()
  fetchCategories()
})
</script>

<style scoped>
.catalog {
  min-height: 100%;
  background-color: #f5f5f5;
  width: 100vw;
  margin: 0;
  padding: 0;
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
}

.catalog-header {
  background-color: white;
  padding: 24px 0;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.catalog-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #1a1a1a;
  text-align: center;
}

.catalog-controls {
  display: flex;
  gap: 16px;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 800px;
}

.search-field {
  max-width: 400px;
  width: 100%;
}

.catalog-content {
  width: 100%;
  padding: 0;
  margin: 0;
}

.products-container {
  position: relative;
  min-height: 400px;
  width: 100%;
  padding: 0;
  box-sizing: border-box;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin: 0 auto;
  padding: 0 24px;
  width: 100%;
  min-height: 600px;
  max-width: 1400px;
}

.product-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease;
  width: 100%;
  min-height: 400px;
}

.product-card:hover {
  transform: translateY(-4px);
}

.product-image {
  aspect-ratio: 1;
  object-fit: cover;
}

.product-title {
  font-size: 16px;
  font-weight: 500;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 44px;
}

.loading-state,
.error-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}

.skeleton-card {
  background: transparent !important;
  min-height: 400px;
}

.skeleton-card :deep(.v-skeleton-loader__image) {
  height: 200px !important;
  width: 100% !important;
}

.skeleton-card :deep(.v-skeleton-loader__list-item-two-line) {
  height: 72px !important;
  width: 100% !important;
}

.skeleton-card :deep(.v-skeleton-loader__button) {
  height: 36px !important;
  width: 100% !important;
}

@media (max-width: 1200px) {
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .catalog-header {
    padding: 16px 0;
  }

  .header-content {
    padding: 0 16px;
  }

  .catalog-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .search-field {
    max-width: none;
  }

  .products-grid {
    grid-template-columns: 1fr;
    gap: 16px;
    padding: 0 16px;
  }
}
</style> 