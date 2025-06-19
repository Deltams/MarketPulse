<template>
  <v-tooltip location="top" :text="product.description" open-delay="200">
    <template #activator="{ props }">
      <v-card
        class="product-card h-100"
        elevation="2"
        hover
        :to="`/products/${product.id}`"
        v-bind="props"
      >
        <v-img
          :src="product.image"
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
          <div class="brand">
            Бренд: {{ getBrandName() }}
            <v-tooltip v-if="isBrandVerified()" location="top">
              <template #activator="{ props }">
                <v-icon
                  v-bind="props"
                  class="verified-icon"
                  color="primary"
                  size="18"
                  style="margin-left: 4px; vertical-align: middle; cursor: pointer;"
                >
                  mdi-shield-check
                </v-icon>
              </template>
              <span>Проверенный бренд</span>
            </v-tooltip>
          </div>
          <div class="price">
            {{ formatPrice(product.price) }} ₽
          </div>
          <div class="product-title">
            {{ product.name }}
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
            @click.stop="$emit('edit', product)"
          >
            Редактировать
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-tooltip>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cartStore'
import { useNotificationStore } from '@/stores/notificationStore'

const props = defineProps({
  product: {
    type: Object,
    required: true
  },
  isSeller: {
    type: Boolean,
    default: false
  }
})

console.log('ProductCard product:', props.product)

const emit = defineEmits(['edit'])
const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()
const notificationStore = useNotificationStore()

const handleAddToCart = (event: Event) => {
  event.preventDefault()
  event.stopPropagation()
  
  if (!authStore.isAuthenticated) {
    notificationStore.addNotification(
      'Для добавления товаров в корзину необходимо войти в систему',
      'warning',
      5000
    )
    return
  }

  cartStore.addToCart({
    id: props.product.id,
    name: props.product.name,
    price: props.product.price,
    imageUrl: props.product.image,
    type: 'product'
  })

  notificationStore.addNotification(
    `Товар "${props.product.name}" добавлен в корзину`,
    'success',
    3000
  )
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU').format(price)
}

const getBrandName = () => {
  if (props.product.brand_name) {
    return props.product.brand_name
  }
  return 'Без бренда'
}

const isBrandVerified = () => {
  return props.product.brand_is_verified || false
}
</script>

<style scoped>
.product-card {
  background: #fff !important;
  box-shadow: 0 4px 16px rgba(0,0,0,0.10), 0 1.5px 4px rgba(0,0,0,0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border-radius: 16px;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
  width: 100%;
  will-change: transform;
  border: 2px solid transparent;
  min-height: 380px;
}
.product-card:hover {
  transform: translateY(-4px) scale(1.01);
  box-shadow: 0 8px 32px rgba(25, 118, 210, 0.25), 0 3px 8px rgba(0,0,0,0.10);
  border-color: #1976d2;
}
.product-card .v-img {
  height: 200px !important;
  width: 100% !important;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  flex-shrink: 0;
}
.product-card .v-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  background: #fff;
}
.product-card .v-card-title {
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
  padding: 16px;
  font-size: 1.1rem;
  line-height: 1.4;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1;
  color: #fff;
  text-shadow: 0 2px 8px rgba(0,0,0,0.25);
}
.product-card .v-card-text {
  padding: 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 140px;
}
.product-card .brand {
  color: #6b7280;
  font-size: 0.85rem;
  font-weight: 500;
  margin-bottom: 6px;
  letter-spacing: 0.02em;
  display: flex;
  align-items: center;
  gap: 4px;
  justify-content: center;
  text-align: center;
}
.product-card .price {
  color: #222;
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 8px;
  letter-spacing: 0.01em;
}
.product-card .v-card-actions {
  padding: 6px 12px 12px;
  margin-top: auto;
}
.add-to-cart-btn {
  background: linear-gradient(90deg, #1976d2 0%, #42a5f5 100%);
  color: #fff !important;
  font-weight: 700;
  font-size: 0.9rem;
  height: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.08);
  transition: background 0.2s, box-shadow 0.2s;
}
.add-to-cart-btn:hover {
  background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%);
  box-shadow: 0 4px 16px rgba(25, 118, 210, 0.16);
}
.product-card .product-title {
  font-size: 1rem;
  font-weight: 600;
  color: #222;
  margin-top: 8px;
  margin-bottom: 0;
  line-height: 1.3;
  word-break: break-word;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
.verified-icon {
  margin-left: 4px;
  vertical-align: middle;
  cursor: pointer;
  transition: color 0.2s;
}
.verified-icon:hover {
  color: #0052CC;
}

@media (max-width: 768px) {
  .product-card {
    min-height: 380px;
  }
  
  .product-card .v-img {
    height: 180px !important;
  }
  
  .product-card .v-card-text {
    min-height: 120px;
    padding: 10px;
  }
  
  .product-card .price {
    font-size: 1.1rem;
  }
  
  .product-title {
    font-size: 0.85rem;
  }
}

@media (max-width: 480px) {
  .product-card {
    min-height: 340px;
  }
  
  .product-card .v-img {
    height: 160px !important;
  }
  
  .product-card .v-card-text {
    min-height: 100px;
    padding: 8px;
  }
  
  .product-card .price {
    font-size: 1rem;
  }
  
  .product-title {
    font-size: 0.8rem;
  }
}
</style> 