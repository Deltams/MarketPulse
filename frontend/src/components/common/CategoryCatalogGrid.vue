<template>
  <div class="category-catalog-grid">
    <ProductFilter
      :initialCategoryId="categoryId"
      :hideCategorySelect="true"
      :brands="brands"
      :filters="filters"
      @filter-change="onFilterChange"
      @price-slider-start="onPriceSliderStart"
      @price-slider-end="onPriceSliderEnd"
    />
    <div v-if="products.length">
      <h2 class="section-title">Товары категории</h2>
      <v-row>
        <v-col v-for="product in products" :key="product.id" cols="12" sm="6" md="4" lg="3">
          <ProductCard :product="product" />
        </v-col>
      </v-row>
    </div>
    <v-divider class="my-8" v-if="products.length && services.length" />
    <div v-if="services.length">
      <h2 class="section-title">Услуги категории</h2>
      <v-row>
        <v-col v-for="service in services" :key="service.id" cols="12" sm="6" md="4" lg="3">
          <ServiceCard :service="service" />
        </v-col>
      </v-row>
    </div>
    <div v-if="!products.length && !services.length" class="empty-block">
      Нет товаров или услуг для этой категории.
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import ProductCard from '@/components/products/ProductCard.vue'
import ServiceCard from '@/components/services/ServiceCard.vue'
import ProductFilter from '@/components/products/ProductFilter.vue'
import api from '@/api/config'

interface Product {
  id: number;
  name?: string;
  description?: string;
  price?: number;
  category?: number;
  seller?: number;
  is_active?: boolean;
  created_at?: string;
  updated_at?: string;
  [key: string]: any;
}

interface Service {
  id: number;
  name?: string;
  description?: string;
  price?: number;
  category?: number;
  seller?: number;
  is_active?: boolean;
  created_at?: string;
  updated_at?: string;
  [key: string]: any;
}

const props = defineProps({
  categoryId: {
    type: Number,
    required: true
  }
})

const products = ref<Product[]>([])
const services = ref<Service[]>([])
const allBrands = ref<any[]>([])
const brands = ref<any[]>([])
const filters = ref({
  search: '',
  brand: null,
  priceSort: null,
  priceRange: [0, 999999]
})

const fetchBrands = async () => {
  const res = await api.get('/brandlist/')
  allBrands.value = res.data
  brands.value = res.data
}

const fetchProducts = async () => {
  const params = { ...filters.value }
  delete params.category
  params.category_0 = props.categoryId
  console.log('Fetching products with params:', params)
  const res = await api.get('/productlist/', { params })
  products.value = Array.isArray(res.data) ? res.data : res.data.results || []
  console.log('Products received:', products.value.length)
}

const fetchServices = async () => {
  const params = { ...filters.value }
  delete params.category
  params.category_0 = props.categoryId
  console.log('Fetching services with params:', params)
  const res = await api.get('/servicelist/', { params })
  services.value = Array.isArray(res.data) ? res.data : res.data.results || []
  console.log('Services received:', services.value.length)
}

const fetchAll = async () => {
  await Promise.all([fetchProducts(), fetchServices()])
  filterBrandsByCategory()
}

const filterBrandsByCategory = () => {
  const productBrandIds = products.value.map(p => p.brand).filter(Boolean)
  const serviceBrandIds = services.value.map(s => s.brand).filter(Boolean)
  const usedBrandIds = Array.from(new Set([...productBrandIds, ...serviceBrandIds]))

  // Фильтруем по allBrands, чтобы не терять полный список
  brands.value = Array.isArray(allBrands.value)
    ? allBrands.value.filter((brand: any) => usedBrandIds.includes(brand.id))
    : []
}

const onFilterChange = (newFilters: any) => {
  // Не добавляем category в фильтры, так как он фиксирован
  console.log('Filter change received:', newFilters)
  filters.value = { ...newFilters }
  console.log('Updated filters:', filters.value)
  fetchAll()
}

const onPriceSliderStart = () => {}
const onPriceSliderEnd = () => {}

watch(() => props.categoryId, () => {
  // Не обновляем filters.value.category, так как он фиксирован
  fetchAll()
})

onMounted(() => {
  fetchBrands()
  fetchAll()
})
</script>

<style scoped>
.category-catalog-grid {
  width: 100%;
}
.section-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin: 2rem 0 1rem 0;
  color: #1976d2;
}
.empty-block {
  text-align: center;
  color: #888;
  margin: 2rem 0;
}
</style> 