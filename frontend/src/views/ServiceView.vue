<template>
  <v-container>
    <div v-if="loading" class="text-center">
      <v-progress-circular
        indeterminate
        color="primary"
        size="64"
      ></v-progress-circular>
      <div class="text-h6 mt-4">Загрузка услуги...</div>
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
      <v-card class="service-card">
        <v-card-text>
          <div class="service-header">
            <div class="service-title">
              {{ service.name }}
            </div>
            <div class="service-price">
              {{ formatPrice(service.price) }} ₽
            </div>
          </div>
          
          <div class="service-description">
            {{ service.description }}
          </div>
          
          <div class="service-meta">
            <div class="service-category">
              <strong>Категория:</strong> {{ service.category_name || 'Без категории' }}
            </div>
            <div class="service-seller">
              <strong>Продавец:</strong> {{ service.seller_name }}
            </div>
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
          <template v-if="isServiceOwner">
            <v-btn
              color="primary"
              variant="outlined"
              block
              @click="editService"
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
            Вы уверены, что хотите удалить эту услугу? Это действие нельзя отменить.
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
              @click="deleteService"
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
import { useServiceStore } from '@/stores/serviceStore'
import { useCartStore } from '@/stores/cartStore'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notificationStore'
import api from '@/api/config'

const route = useRoute()
const router = useRouter()
const serviceStore = useServiceStore()
const cartStore = useCartStore()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const service = ref(null)
const loading = ref(true)
const error = ref('')
const deleteDialog = ref(false)

const isServiceOwner = computed(() => {
  if (!service.value || !authStore.isAuthenticated) return false
  return service.value.seller === authStore.user?.id
})

const fetchService = async () => {
  try {
    const response = await api.get(`/servicelist/${route.params.id}/`)
    service.value = response.data
  } catch (err) {
    error.value = 'Не удалось загрузить услугу'
    console.error('Error fetching service:', err)
  } finally {
    loading.value = false
  }
}

const addToCart = () => {
  if (!authStore.isAuthenticated) {
    notificationStore.addNotification(
      'Для добавления услуг в корзину необходимо войти в систему',
      'warning',
      5000
    )
    return
  }
  cartStore.addToCart({
    id: service.value.id,
    name: service.value.name,
    price: service.value.price,
    type: 'service'
  })
}

const editService = () => {
  router.push(`/services/${service.value.id}/edit`)
}

const confirmDelete = () => {
  deleteDialog.value = true
}

const deleteService = async () => {
  try {
    await api.delete(`/servicelist/${service.value.id}/`)
    router.push('/services')
  } catch (err) {
    error.value = 'Не удалось удалить услугу'
    console.error('Error deleting service:', err)
  }
  deleteDialog.value = false
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU').format(price)
}

onMounted(() => {
  fetchService()
})
</script>

<style scoped>
.service-card {
  max-width: 800px;
  margin: 0 auto;
  border-radius: 16px;
  overflow: hidden;
}

.service-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.service-title {
  font-size: 2rem;
  font-weight: 700;
  color: #222;
  line-height: 1.2;
  flex: 1;
  margin-right: 20px;
}

.service-price {
  color: #1976d2;
  font-size: 2.5rem;
  font-weight: 700;
  white-space: nowrap;
}

.service-description {
  color: #666;
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 24px;
}

.service-meta {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 24px;
}

.service-category,
.service-seller {
  color: #555;
  font-size: 1rem;
  margin-bottom: 8px;
}

.service-seller {
  font-weight: 500;
}
</style> 