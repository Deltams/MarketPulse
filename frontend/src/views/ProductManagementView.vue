<template>
  <div class="product-management">
    <h1>Управление товарами</h1>

    <!-- Форма добавления/редактирования товара -->
    <v-card class="mb-6">
      <v-card-title>
        {{ editingProduct ? 'Редактирование товара' : 'Добавление нового товара' }}
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="saveProduct" ref="form">
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="productForm.name"
                label="Название товара"
                :rules="[v => !!v || 'Название обязательно']"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="productForm.price"
                label="Цена"
                type="number"
                :rules="[
                  v => !!v || 'Цена обязательна',
                  v => v > 0 || 'Цена должна быть положительной'
                ]"
                required
              ></v-text-field>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12">
              <v-textarea
                v-model="productForm.description"
                label="Описание"
                rows="3"
              ></v-textarea>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="6">
              <v-select
                v-model="productForm.category"
                :items="categories"
                item-title="name"
                item-value="id"
                label="Категория"
              ></v-select>
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                v-model="productForm.brand"
                :items="brands"
                item-title="name"
                item-value="id"
                label="Бренд"
              ></v-select>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12">
              <v-file-input
                v-model="productForm.image"
                label="Изображение товара"
                accept="image/*"
                :rules="[
                  v => !v || v.size < 5000000 || 'Размер изображения должен быть меньше 5MB'
                ]"
                prepend-icon="mdi-camera"
              ></v-file-input>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" class="d-flex justify-end">
              <v-btn
                color="primary"
                type="submit"
                :loading="loading"
              >
                {{ editingProduct ? 'Сохранить изменения' : 'Добавить товар' }}
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>

    <!-- Список товаров -->
    <v-card>
      <v-card-title>
        Мои товары
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Поиск"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="products"
        :search="search"
        :loading="loading"
      >
        <template v-slot:item.image="{ item }">
          <v-img
            :src="item.image || '/placeholder.png'"
            max-width="50"
            max-height="50"
            contain
          ></v-img>
        </template>

        <template v-slot:item.price="{ item }">
          {{ formatPrice(item.price) }}
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn
            icon
            size="small"
            color="primary"
            @click="editProduct(item)"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn
            icon
            size="small"
            color="error"
            @click="deleteProduct(item)"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useProductStore } from '@/stores/productStore'
import api from '@/api/config'

const productStore = useProductStore()
const loading = ref(false)
const search = ref('')
const editingProduct = ref(null)

const productForm = ref({
  name: '',
  description: '',
  price: '',
  category: null,
  brand: null,
  image: null
})

const headers = [
  { title: 'Изображение', key: 'image', sortable: false },
  { title: 'Название', key: 'name' },
  { title: 'Цена', key: 'price' },
  { title: 'Категория', key: 'category_name' },
  { title: 'Бренд', key: 'brand_name' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const products = ref([])
const categories = ref([])
const brands = ref([])

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB'
  }).format(price)
}

const loadData = async () => {
  loading.value = true
  try {
    const [productsRes, categoriesRes, brandsRes] = await Promise.all([
      api.get('/productlist/'),
      api.get('/categories/'),
      api.get('/brands/')
    ])
    products.value = productsRes.data
    categories.value = categoriesRes.data
    brands.value = brandsRes.data
  } catch (error) {
    console.error('Error loading data:', error)
  } finally {
    loading.value = false
  }
}

const saveProduct = async () => {
  loading.value = true
  try {
    const formData = new FormData()
    Object.keys(productForm.value).forEach(key => {
      if (productForm.value[key] !== null) {
        formData.append(key, productForm.value[key])
      }
    })

    if (editingProduct.value) {
      await api.put(`/productlist/${editingProduct.value.id}/`, formData)
    } else {
      await api.post('/productlist/', formData)
    }

    await loadData()
    resetForm()
  } catch (error) {
    console.error('Error saving product:', error)
  } finally {
    loading.value = false
  }
}

const editProduct = (product) => {
  editingProduct.value = product
  productForm.value = {
    name: product.name,
    description: product.description,
    price: product.price,
    category: product.category,
    brand: product.brand,
    image: null
  }
}

const deleteProduct = async (product) => {
  if (!confirm('Вы уверены, что хотите удалить этот товар?')) return

  loading.value = true
  try {
    await api.delete(`/productlist/${product.id}/`)
    await loadData()
  } catch (error) {
    console.error('Error deleting product:', error)
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  editingProduct.value = null
  productForm.value = {
    name: '',
    description: '',
    price: '',
    category: null,
    brand: null,
    image: null
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.product-management {
  padding: 2rem;
}
</style> 