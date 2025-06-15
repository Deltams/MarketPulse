<template>
  <div class="products-view">
    <div class="header">
      <h1>{{ isSeller ? 'Управление товарами' : 'Каталог товаров' }}</h1>
      <button 
        v-if="isSeller" 
        @click="showAddForm = true" 
        class="add-button"
      >
        Добавить товар
      </button>
    </div>

    <div v-if="loading" class="loading">
      Загрузка...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else-if="!storeProducts.length" class="no-products">
      Товары не найдены
    </div>

    <ProductList
      v-else
      :products="storeProducts"
      :is-seller="isSeller"
      @edit="handleEdit"
      @add-to-cart="handleAddToCart"
    />

    <!-- Модальное окно для добавления/редактирования товара -->
    <div v-if="showAddForm || editingProduct" class="modal">
      <div class="modal-content">
        <ProductForm
          :product="editingProduct"
          :is-editing="!!editingProduct"
          @submit="handleSubmit"
          @cancel="closeModal"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { useProductStore } from '@/stores/productStore'
import ProductList from '@/components/products/ProductList.vue'
import ProductForm from '@/components/products/ProductForm.vue'

// TODO: Replace with actual auth check
const isSeller = ref(false)

const productStore = useProductStore()
const { loading, error } = productStore

// Используем computed для получения реактивных данных из store
const storeProducts = computed(() => productStore.products)

// Функция для загрузки данных
const loadProducts = async () => {
  try {
    await productStore.fetchProducts()
  } catch (e) {
    console.error('Failed to load products:', e)
  }
}

// Загружаем данные при монтировании компонента
onMounted(loadProducts)

// Следим за изменениями в products
watch(storeProducts, (newProducts) => {
  console.log('ProductsView: products updated:', newProducts)
}, { deep: true })

const showAddForm = ref(false)
const editingProduct = ref(null)

const handleEdit = (product) => {
  editingProduct.value = product
}

const handleAddToCart = (product) => {
  // TODO: Implement add to cart functionality
  console.log('Add to cart:', product)
}

const handleSubmit = async (formData) => {
  try {
    if (editingProduct.value) {
      await productStore.updateProduct(editingProduct.value.id, formData)
    } else {
      await productStore.createProduct(formData)
    }
    closeModal()
    // Перезагружаем список после изменений
    await loadProducts()
  } catch (error) {
    console.error('Failed to save product:', error)
  }
}

const closeModal = () => {
  showAddForm.value = false
  editingProduct.value = null
}
</script>

<style scoped>
.products-view {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header h1 {
  margin: 0;
  font-size: 1.8rem;
  color: #2c3e50;
}

.add-button {
  padding: 10px 20px;
  background-color: #2ecc71;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-button:hover {
  background-color: #27ae60;
}

.loading,
.error,
.no-products {
  text-align: center;
  padding: 40px;
  font-size: 1.2rem;
}

.error {
  color: #e74c3c;
}

.no-products {
  color: #666;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}
</style>