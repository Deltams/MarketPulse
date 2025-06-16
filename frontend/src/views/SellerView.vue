<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-6">
          <h1 class="text-h4">Управление товарами</h1>
          <BaseButton
            color="primary"
            variant="elevated"
            prepend-icon="mdi-plus"
            @click="openProductDialog()"
          >
            Добавить товар
          </BaseButton>
        </div>

        <ProductFilter
          :categories="categories"
          @filter="handleFilter"
        />

        <ProductList
          :products="products"
          :loading="loading"
          :is-seller="true"
          :total-items="totalItems"
          :items-per-page="itemsPerPage"
          :current-page="currentPage"
          @add="openProductDialog"
          @edit="openProductDialog"
          @page-change="handlePageChange"
        />
      </v-col>
    </v-row>

    <v-dialog
      v-model="dialog"
      max-width="800px"
    >
      <v-card>
        <v-card-title class="text-h5">
          {{ editingProduct ? 'Редактирование товара' : 'Добавление товара' }}
        </v-card-title>

        <v-card-text>
          <ProductForm
            ref="productForm"
            :product="editingProduct"
            :loading="saving"
            @submit="handleProductSubmit"
            @cancel="dialog = false"
          />
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import BaseButton from '../components/common/BaseButton.vue'
import ProductFilter from '../components/products/ProductFilter.vue'
import ProductList from '../components/products/ProductList.vue'
import ProductForm from '../components/products/ProductForm.vue'

interface Product {
  id?: number
  name: string
  description: string
  price: number
  image: File | null
  categoryId?: number
}

interface Category {
  id: number
  name: string
}

const authStore = useAuthStore()
const loading = ref(true)
const saving = ref(false)
const dialog = ref(false)
const editingProduct = ref<Product | null>(null)
const products = ref<Product[]>([])
const categories = ref<Category[]>([])
const totalItems = ref(0)
const itemsPerPage = ref(12)
const currentPage = ref(1)
const filterParams = ref({
  search: '',
  minPrice: null as number | null,
  maxPrice: null as number | null,
  categories: [] as number[]
})

const productForm = ref()

const fetchProducts = async () => {
  loading.value = true
  try {
    // Здесь будет запрос к API
    // const response = await axios.get('/api/seller/products', {
    //   params: {
    //     page: currentPage.value,
    //     limit: itemsPerPage.value,
    //     ...filterParams.value
    //   }
    // })
    // products.value = response.data.items
    // totalItems.value = response.data.total

    // Временные данные для демонстрации
    products.value = [
      {
        id: 1,
        name: 'Товар 1',
        description: 'Описание товара 1',
        price: 1000,
        image: null
      }
    ]
    totalItems.value = 1
  } catch (error) {
    console.error('Failed to fetch products:', error)
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    // Здесь будет запрос к API
    // const response = await axios.get('/api/categories')
    // categories.value = response.data

    // Временные данные для демонстрации
    categories.value = [
      { id: 1, name: 'Категория 1' },
      { id: 2, name: 'Категория 2' }
    ]
  } catch (error) {
    console.error('Failed to fetch categories:', error)
  }
}

const handleFilter = (params: typeof filterParams.value) => {
  filterParams.value = params
  currentPage.value = 1
  fetchProducts()
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchProducts()
}

const openProductDialog = (product?: Product) => {
  editingProduct.value = product || null
  dialog.value = true
}

const handleProductSubmit = async (product: Product) => {
  saving.value = true
  try {
    if (editingProduct.value?.id) {
      // Здесь будет запрос к API для обновления
      // await axios.put(`/api/seller/products/${editingProduct.value.id}`, product)
      console.log('Updating product:', product)
    } else {
      // Здесь будет запрос к API для создания
      // await axios.post('/api/seller/products', product)
      console.log('Creating product:', product)
    }
    dialog.value = false
    fetchProducts()
  } catch (error) {
    console.error('Failed to save product:', error)
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchProducts()
  fetchCategories()
})
</script> 