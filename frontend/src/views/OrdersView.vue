<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-6">Мои заказы</h1>

        <div v-if="loading" class="d-flex justify-center align-center pa-4">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </div>

        <div v-else-if="orders.length === 0" class="text-center pa-4">
          <p class="text-h6 text-medium-emphasis">У вас пока нет заказов</p>
          <BaseButton
            color="primary"
            variant="elevated"
            class="mt-4"
            @click="$router.push('/products')"
          >
            Перейти к товарам
          </BaseButton>
        </div>

        <v-expansion-panels v-else>
          <v-expansion-panel
            v-for="order in orders"
            :key="order.id"
            class="mb-4"
          >
            <v-expansion-panel-title>
              <div class="d-flex justify-space-between align-center w-100">
                <div>
                  <span class="font-weight-bold">Заказ #{{ order.id }}</span>
                  <span class="text-medium-emphasis ml-4">
                    {{ formatDate(order.createdAt) }}
                  </span>
                </div>
                <v-chip
                  :color="getStatusColor(order.status)"
                  size="small"
                >
                  {{ getStatusText(order.status) }}
                </v-chip>
              </div>
            </v-expansion-panel-title>

            <v-expansion-panel-text>
              <v-list>
                <v-list-item
                  v-for="item in order.items"
                  :key="item.id"
                  :title="item.product.name"
                  :subtitle="`${item.quantity} шт. × ${formatPrice(item.price)}`"
                >
                  <template v-slot:prepend>
                    <v-img
                      :src="item.product.image || '/placeholder.png'"
                      width="50"
                      height="50"
                      cover
                      class="rounded"
                    ></v-img>
                  </template>
                  <template v-slot:append>
                    <span class="text-body-1 font-weight-bold">
                      {{ formatPrice(item.price * item.quantity) }}
                    </span>
                  </template>
                </v-list-item>
              </v-list>

              <v-divider class="my-4"></v-divider>

              <div class="d-flex justify-space-between align-center">
                <div>
                  <p class="text-body-2 text-medium-emphasis mb-1">
                    Адрес доставки:
                  </p>
                  <p class="text-body-1">
                    {{ order.shippingAddress }}
                  </p>
                </div>
                <div class="text-right">
                  <p class="text-body-2 text-medium-emphasis mb-1">
                    Итого:
                  </p>
                  <p class="text-h6 font-weight-bold">
                    {{ formatPrice(order.total) }}
                  </p>
                </div>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import BaseButton from '../components/common/BaseButton.vue'

interface OrderItem {
  id: number
  product: {
    id: number
    name: string
    image: string | null
  }
  quantity: number
  price: number
}

interface Order {
  id: number
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'
  items: OrderItem[]
  total: number
  shippingAddress: string
  createdAt: string
}

const authStore = useAuthStore()
const loading = ref(true)
const orders = ref<Order[]>([])

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB'
  }).format(price)
}

const getStatusColor = (status: Order['status']) => {
  const colors = {
    pending: 'warning',
    processing: 'info',
    shipped: 'primary',
    delivered: 'success',
    cancelled: 'error'
  }
  return colors[status]
}

const getStatusText = (status: Order['status']) => {
  const texts = {
    pending: 'Ожидает оплаты',
    processing: 'В обработке',
    shipped: 'Отправлен',
    delivered: 'Доставлен',
    cancelled: 'Отменен'
  }
  return texts[status]
}

const fetchOrders = async () => {
  try {
    // Здесь будет запрос к API
    // const response = await axios.get('/api/orders')
    // orders.value = response.data

    // Временные данные для демонстрации
    orders.value = [
      {
        id: 1,
        status: 'delivered',
        items: [
          {
            id: 1,
            product: {
              id: 1,
              name: 'Товар 1',
              image: null
            },
            quantity: 2,
            price: 1000
          }
        ],
        total: 2000,
        shippingAddress: 'г. Москва, ул. Примерная, д. 1, кв. 1',
        createdAt: '2024-03-15T10:00:00Z'
      }
    ]
  } catch (error) {
    console.error('Failed to fetch orders:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchOrders()
})
</script> 