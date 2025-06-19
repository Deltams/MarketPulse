<template>
  <div class="products-page">
    <!-- Фильтрация - растягиваем на всю ширину -->
    <div class="filter-section">
      <div class="container">
        <ProductFilter 
          @filter-change="handleFilterChange" 
          @price-slider-start="handlePriceSliderStart"
          @price-slider-end="handlePriceSliderEnd"
        />
      </div>
    </div>
    
    <div class="products-container">
      <div v-if="error" class="error">
        <v-alert type="error" variant="tonal">
          {{ error }}
        </v-alert>
      </div>
      
      <div v-else>
        <!-- Результаты поиска -->
        <div class="results-info">
          <v-chip color="primary" variant="tonal">
            Найдено: {{ productStore.pagination.count }} товаров
          </v-chip>
          <div class="pagination-info">
            <span class="text-body-2 text-grey">
              Страница {{ productStore.pagination.current_page }} из {{ productStore.pagination.total_pages }}
            </span>
          </div>
        </div>
        
        <!-- Список товаров -->
        <div class="products-list">
          <div
            v-for="(product, idx) in getProductSlots"
            :key="product.id || 'skeleton-' + idx"
            class="product-list-item"
          >
            <div class="product-skeleton-stack">
              <ProductCard
                v-if="product.id"
                :product="product"
              />
              <div
                v-if="showSkeletons"
                :class="['custom-skeleton-card', { 'fade-out': skeletonsFadingOut }]"
              >
                <div class="skeleton-img"></div>
                <div class="skeleton-content">
                  <div class="skeleton-brand"></div>
                  <div class="skeleton-price"></div>
                  <div class="skeleton-desc"></div>
                  <div class="skeleton-title"></div>
                </div>
                <div class="skeleton-actions">
                  <div class="skeleton-btn"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Сообщение если ничего не найдено -->
        <div v-if="productStore.products.length === 0 && !showSkeletons" class="no-results">
          <v-card class="no-results-card" variant="tonal">
            <v-card-text class="text-center">
              <v-icon size="64" color="grey" class="mb-4">mdi-package-variant-closed</v-icon>
              <h3>Товары не найдены</h3>
              <p v-if="filters.category">
                В выбранной категории нет товаров
              </p>
              <p v-else>
                Попробуйте изменить параметры поиска
              </p>
            </v-card-text>
          </v-card>
        </div>
        
        <!-- Пагинация -->
        <div v-if="productStore.pagination.total_pages > 1" class="pagination-section">
          <v-card class="pagination-card" variant="tonal">
            <v-card-text class="pagination-content">
              <div class="pagination-controls">
                <!-- Кнопка "Предыдущая" -->
                <v-btn
                  :disabled="!productStore.hasPreviousPage || loading"
                  variant="outlined"
                  @click="handlePreviousPage"
                  class="pagination-btn"
                >
                  <v-icon start>mdi-chevron-left</v-icon>
                  Предыдущая
                </v-btn>
                
                <!-- Номера страниц -->
                <div class="page-numbers">
                  <v-btn
                    v-for="page in visiblePages"
                    :key="page"
                    :variant="page === productStore.pagination.current_page ? 'elevated' : 'outlined'"
                    :color="page === productStore.pagination.current_page ? 'primary' : undefined"
                    @click="handlePageChange(page)"
                    :disabled="loading"
                    class="page-btn"
                    size="small"
                  >
                    {{ page }}
                  </v-btn>
                  
                  <!-- Многоточие -->
                  <span v-if="showStartEllipsis" class="ellipsis">...</span>
                  <span v-if="showEndEllipsis" class="ellipsis">...</span>
                </div>
                
                <!-- Кнопка "Следующая" -->
                <v-btn
                  :disabled="!productStore.hasNextPage || loading"
                  variant="outlined"
                  @click="handleNextPage"
                  class="pagination-btn"
                >
                  Следующая
                  <v-icon end>mdi-chevron-right</v-icon>
                </v-btn>
              </div>
              
              <!-- Информация о страницах -->
              <div class="pagination-summary">
                <span class="text-body-2 text-grey">
                  Показано {{ (productStore.pagination.current_page - 1) * productStore.pagination.page_size + 1 }} - 
                  {{ Math.min(productStore.pagination.current_page * productStore.pagination.page_size, productStore.pagination.count) }} 
                  из {{ productStore.pagination.count }} товаров
                </span>
              </div>
            </v-card-text>
          </v-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch, computed, onUnmounted } from 'vue'
import { useNotificationStore } from '@/stores/notificationStore'
import { useProductStore } from '@/stores/productStore'
import ProductCard from '@/components/products/ProductCard.vue'
import ProductFilter from '@/components/products/ProductFilter.vue'

const notificationStore = useNotificationStore()
const productStore = useProductStore()

// Состояние
const error = ref('')

// Скелетоны
const showSkeletons = ref(true)
const skeletonsFadingOut = ref(false)
const SKELETON_COUNT = 10 // Количество скелетонов для отображения

// Таймеры
let dataLoaded = false
let timerDone = false
let timerId: number | null = null

// Фильтры
const filters = ref({
  search: '',
  category: null as number | null,
  priceSort: '',
  priceRange: [0, 100000] as [number, number]
})

// Вычисляемое свойство для отображения товаров или скелетонов
const getProductSlots = computed(() => {
  // Если скелетоны показываются, всегда показываем SKELETON_COUNT слотов
  if (showSkeletons.value) {
    if (productStore.products.length >= SKELETON_COUNT) {
      return productStore.products.slice(0, SKELETON_COUNT)
    }
    return [
      ...productStore.products,
      ...Array(SKELETON_COUNT - productStore.products.length).fill({})
    ]
  }
  
  // Если скелетоны скрыты, показываем только реальные товары
  return productStore.products
})

// Вычисляемое свойство для видимых страниц пагинации
const visiblePages = computed(() => {
  const current = productStore.pagination.current_page
  const total = productStore.pagination.total_pages
  const pages: number[] = []
  
  if (total <= 7) {
    // Если страниц мало, показываем все
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    // Показываем первую, последнюю и 5 страниц вокруг текущей
    pages.push(1)
    
    const start = Math.max(2, current - 2)
    const end = Math.min(total - 1, current + 2)
    
    for (let i = start; i <= end; i++) {
      pages.push(i)
    }
    
    if (total > 1) {
      pages.push(total)
    }
  }
  
  return pages
})

const showStartEllipsis = computed(() => {
  return visiblePages.value.length > 0 && visiblePages.value[1] > 2
})

const showEndEllipsis = computed(() => {
  const pages = visiblePages.value
  return pages.length > 0 && pages[pages.length - 2] < productStore.pagination.total_pages - 1
})

const loading = computed(() => productStore.loading)

const finishSkeletons = () => {
  skeletonsFadingOut.value = true
  setTimeout(() => {
    showSkeletons.value = false
  }, 400) // 400ms = время transition
}

const maybeShowProducts = () => {
  if (dataLoaded && timerDone) {
    finishSkeletons()
  }
}

const fetchProducts = async (customParams = {}) => {
  error.value = ''
  try {
    const params: Record<string, any> = { ...customParams }
    // Добавляем параметры фильтрации
    if (filters.value.search) {
      params.search = filters.value.search
    }
    if (filters.value.category) {
      params.category_0 = filters.value.category
    }
    if (filters.value.priceRange[0] > 0) {
      params.min_price = filters.value.priceRange[0]
    }
    if (filters.value.priceRange[1] < 999999) {
      params.max_price = filters.value.priceRange[1]
    }
    await productStore.fetchProducts(params)
    dataLoaded = true
    maybeShowProducts()
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Ошибка при загрузке товаров'
    console.error('Error fetching products:', err)
    dataLoaded = true
    maybeShowProducts()
  }
}

const handleFilterChange = (newFilters: any) => {
  filters.value = { ...filters.value, ...newFilters }
  showSkeletons.value = true
  skeletonsFadingOut.value = false
  dataLoaded = false
  if (timerId) clearTimeout(timerId)
  timerDone = false
  timerId = setTimeout(() => {
    timerDone = true
    maybeShowProducts()
  }, 3000) as unknown as number
  fetchProducts()
}

const handlePriceSliderStart = () => {
  // Показываем скелетоны при начале взаимодействия с ползунком
  showSkeletons.value = true
  skeletonsFadingOut.value = false
}

const handlePriceSliderEnd = () => {
  // Делаем запрос к backend после отпускания ползунка
  fetchProducts()
  
  // Скрываем скелетоны через секунду после отпускания ползунка
  setTimeout(() => {
    if (!dataLoaded) {
      finishSkeletons()
    }
  }, 1000)
}

const handleNextPage = async () => {
  if (!productStore.hasNextPage || loading.value) return
  showSkeletons.value = true
  skeletonsFadingOut.value = false
  dataLoaded = false
  if (timerId) clearTimeout(timerId)
  timerDone = false
  timerId = setTimeout(() => {
    timerDone = true
    maybeShowProducts()
  }, 3000) as unknown as number
  try {
    await productStore.fetchNextPage()
    dataLoaded = true
    maybeShowProducts()
  } catch (err) {
    dataLoaded = true
    maybeShowProducts()
  }
}

const handlePreviousPage = async () => {
  if (!productStore.hasPreviousPage || loading.value) return
  showSkeletons.value = true
  skeletonsFadingOut.value = false
  dataLoaded = false
  if (timerId) clearTimeout(timerId)
  timerDone = false
  timerId = setTimeout(() => {
    timerDone = true
    maybeShowProducts()
  }, 3000) as unknown as number
  try {
    await productStore.fetchPreviousPage()
    dataLoaded = true
    maybeShowProducts()
  } catch (err) {
    dataLoaded = true
    maybeShowProducts()
  }
}

const handlePageChange = async (page: number) => {
  if (page === productStore.pagination.current_page || loading.value) return
  showSkeletons.value = true
  skeletonsFadingOut.value = false
  dataLoaded = false
  if (timerId) clearTimeout(timerId)
  timerDone = false
  timerId = setTimeout(() => {
    timerDone = true
    maybeShowProducts()
  }, 3000) as unknown as number
  try {
    const params: Record<string, any> = {}
    if (filters.value.search) {
      params.search = filters.value.search
    }
    if (filters.value.category) {
      params.category_0 = filters.value.category
    }
    if (filters.value.priceRange[0] > 0) {
      params.min_price = filters.value.priceRange[0]
    }
    if (filters.value.priceRange[1] < 999999) {
      params.max_price = filters.value.priceRange[1]
    }
    await productStore.fetchPage(page, params)
    dataLoaded = true
    maybeShowProducts()
  } catch (err) {
    dataLoaded = true
    maybeShowProducts()
  }
}

// Следим за изменениями фильтров (кроме диапазона цен)
watch(filters, (newFilters, oldFilters) => {
  if (JSON.stringify(newFilters.priceRange) !== JSON.stringify(oldFilters?.priceRange)) {
    return
  }
  fetchProducts()
}, { deep: true })

onMounted(() => {
  fetchProducts()
  if (timerId) clearTimeout(timerId)
  timerDone = false
  timerId = setTimeout(() => {
    timerDone = true
    maybeShowProducts()
  }, 3000) as unknown as number
})

onUnmounted(() => {
  if (timerId) clearTimeout(timerId)
})
</script>

<style scoped>
.results-info {
  padding-left: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  max-width: 1600px;
  margin-left: auto;
  margin-right: auto;
}

.pagination-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

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

/* Пагинация */
.pagination-section {
  margin: 3rem 0;
  display: flex;
  justify-content: center;
}

.pagination-card {
  max-width: 800px;
  width: 100%;
  border-radius: 16px;
}

.pagination-content {
  padding: 2rem;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.pagination-btn {
  min-width: 120px;
  border-radius: 8px;
  color: #fff;
  background-color: #1976d2;
  border: none;
}

.pagination-btn:disabled {
  background-color: #90caf9;
  color: #fff;
}

.page-btn {
  min-width: 40px;
  border-radius: 8px;
  color: #1976d2;
  border: 1.5px solid #1976d2;
  background: #fff;
}

.page-btn[aria-pressed="true"], .page-btn.elevated, .page-btn--active {
  background: #1976d2;
  color: #fff;
  border: 1.5px solid #1976d2;
}

.ellipsis {
  color: #666;
  font-weight: 500;
  padding: 0 0.5rem;
}

.pagination-summary {
  text-align: center;
  margin-top: 1rem;
}

/* Скелетоны */
.product-skeleton-stack {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 380px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: stretch;
}

.custom-skeleton-card {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.10), 0 1.5px 4px rgba(0,0,0,0.08);
  width: 100%;
  height: 100%;
  max-width: none;
  margin: 0;
  background: #f3f6fa;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  opacity: 1;
  transition: opacity 0.5s;
}

.custom-skeleton-card.fade-out {
  opacity: 0;
}

.skeleton-img,
.skeleton-brand,
.skeleton-price,
.skeleton-desc,
.skeleton-title,
.skeleton-btn {
  background: linear-gradient(90deg, #e0e7ef 25%, #f3f6fa 50%, #e0e7ef 75%);
  background-size: 400px 100%;
  animation: skeleton-loading 3s infinite linear;
}

.skeleton-img {
  height: 220px;
  width: 100%;
}

.skeleton-content {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-brand, .skeleton-price, .skeleton-desc, .skeleton-title {
  height: 18px;
  border-radius: 4px;
}

.skeleton-brand { width: 60%; }
.skeleton-price { width: 40%; height: 22px; }
.skeleton-desc { width: 100%; height: 16px; }
.skeleton-title { width: 90%; height: 20px; margin-top: 8px; }

.skeleton-actions {
  padding: 8px 16px 16px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.skeleton-btn {
  height: 48px;
  border-radius: 8px;
  width: 100%;
}

@keyframes skeleton-loading {
  0% { background-position: -400px 0; }
  100% { background-position: 400px 0; }
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
  
  .pagination-controls {
    flex-direction: column;
    gap: 1rem;
  }
  
  .page-numbers {
    order: -1;
  }
}
@media (max-width: 500px) {
  .products-list {
    grid-template-columns: 1fr;
  }
  
  .results-info {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>