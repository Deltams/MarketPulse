<template>
  <v-container>
    <div v-if="loading" class="text-center">
      <v-progress-circular
        indeterminate
        color="primary"
        size="64"
      ></v-progress-circular>
      <div class="text-h6 mt-4">Загрузка товара...</div>
    </div>

    <div v-else-if="error">
      <v-alert
        type="error"
        variant="tonal"
        class="mb-4"
      >
        {{ error }}
      </v-alert>
    </div>

    <template v-else>
      <v-card class="product-card">
        <v-img
          :src="product.image"
          height="400"
          cover
          class="align-end"
        >
          <v-card-title class="text-white text-shadow">
            {{ product.name }}
          </v-card-title>
        </v-img>

        <v-card-text>
          <div class="text-subtitle-1 text-primary mb-2">
            {{ product.brand_name || product.brand?.name || 'Без бренда' }}
          </div>
          <div class="text-h4 font-weight-bold mb-4">
            {{ product.price }} ₽
          </div>
          <div class="text-body-1 mb-6">
            {{ product.description }}
          </div>
        </v-card-text>

        <v-card-actions>
          <v-btn
            color="primary"
            variant="tonal"
            block
            @click="addToCart"
            class="mb-2"
          >
            В корзину
          </v-btn>

          <!-- Кнопки для продавца -->
          <template v-if="isProductOwner">
            <v-btn
              color="primary"
              variant="outlined"
              block
              @click="editProduct"
              class="mb-2"
            >
              Редактировать
            </v-btn>
            <v-btn
              color="error"
              variant="outlined"
              block
              @click="confirmDelete"
            >
              Удалить
            </v-btn>
          </template>
        </v-card-actions>
      </v-card>

      <!-- Диалог подтверждения удаления -->
      <v-dialog v-model="deleteDialog" max-width="400">
        <v-card>
          <v-card-title class="text-h5">
            Подтверждение удаления
          </v-card-title>
          <v-card-text>
            Вы уверены, что хотите удалить этот товар? Это действие нельзя отменить.
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="grey-darken-1"
              variant="text"
              @click="deleteDialog = false"
            >
              Отмена
            </v-btn>
            <v-btn
              color="error"
              variant="text"
              @click="deleteProduct"
            >
              Удалить
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </template>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cartStore'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/config'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()

const product = ref(null)
const loading = ref(true)
const error = ref('')
const deleteDialog = ref(false)

const isProductOwner = computed(() => {
  if (!product.value || !authStore.isAuthenticated) return false
  return product.value.brand?.id === authStore.user?.brand_id
})

const fetchProduct = async () => {
  try {
    const response = await api.get(`/productlist/${route.params.id}/`)
    product.value = response.data
  } catch (err) {
    error.value = 'Не удалось загрузить товар'
    console.error('Error fetching product:', err)
  } finally {
    loading.value = false
  }
}

const addToCart = () => {
  cartStore.addItem(product.value)
}

const editProduct = () => {
  router.push(`/products/${product.value.id}/edit`)
}

const confirmDelete = () => {
  deleteDialog.value = true
}

const deleteProduct = async () => {
  try {
    await api.delete(`/productlist/${product.value.id}/`)
    router.push('/catalog')
  } catch (err) {
    error.value = 'Не удалось удалить товар'
    console.error('Error deleting product:', err)
  }
  deleteDialog.value = false
}

onMounted(() => {
  fetchProduct()
})
</script>

<style scoped>
.product-card {
  max-width: 800px;
  margin: 0 auto;
  border-radius: 16px;
  overflow: hidden;
}

.text-shadow {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}
</style>