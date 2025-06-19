<template>
  <v-card
    class="service-card h-100"
    elevation="2"
    hover
    :to="`/services/${service.id}`"
  >
    <v-img
      :src="serviceImage"
      height="220"
      cover
      class="align-end"
    >
      <template v-slot:placeholder>
        <v-row class="fill-height ma-0" align="center" justify="center">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </v-row>
      </template>
    </v-img>
    <v-card-text>
      <div class="service-type">
        <v-chip
          color="secondary"
          size="small"
          class="mb-2"
        >
          Услуга
        </v-chip>
      </div>
      <div class="price">
        {{ formatPrice(service.price) }} ₽
      </div>
      <div class="text-body-2 text-grey mb-2">
        {{ service.description }}
      </div>
      <div class="service-title">
        {{ service.name }}
      </div>
    </v-card-text>
    <v-card-actions @click.stop>
      <v-btn
        class="add-to-cart-btn"
        block
        @click.stop="handleAddToCart"
      >
        В корзину
      </v-btn>
      <v-btn
        v-if="isSeller"
        color="secondary"
        variant="text"
        @click.stop="$emit('edit', service)"
      >
        Редактировать
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cartStore'
import { useNotificationStore } from '@/stores/notificationStore'

interface Service {
  id: number
  name: string
  description: string
  price: number
  category: number
  seller: number
  is_active: boolean
  created_at: string
  updated_at: string
}

interface Props {
  service: Service
}

const props = defineProps<Props>()
const emit = defineEmits<{
  edit: [service: Service]
}>()

const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()
const notificationStore = useNotificationStore()

const isSeller = computed(() => authStore.isAuthenticated && authStore.user?.is_seller)

const serviceImage = computed(() => {
  // Default service image or placeholder
  return 'https://via.placeholder.com/300x300/9c27b0/ffffff?text=Услуга'
})

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB'
  }).format(price)
}

const handleAddToCart = () => {
  if (!authStore.isAuthenticated) {
    notificationStore.addNotification(
      'Для добавления услуг в корзину необходимо войти в систему',
      'warning',
      5000
    )
    return
  }

  cartStore.addToCart({
    id: props.service.id,
    name: props.service.name,
    price: props.service.price,
    type: 'service'
  })

  notificationStore.addNotification(
    `Услуга "${props.service.name}" добавлена в корзину`,
    'success',
    3000
  )
}
</script>

<style scoped>
.service-card {
  transition: transform 0.2s ease-in-out;
}

.service-card:hover {
  transform: translateY(-4px);
}

.service-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: #2c3e50;
}

.price {
  font-size: 1.2rem;
  font-weight: bold;
  color: #e74c3c;
  margin-bottom: 8px;
}

.service-type {
  display: flex;
  justify-content: flex-start;
}

.add-to-cart-btn {
  background: linear-gradient(45deg, #9c27b0, #673ab7);
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
}

.add-to-cart-btn:hover {
  background: linear-gradient(45deg, #7b1fa2, #5e35b1);
  transform: translateY(-1px);
}
</style> 