<template>
  <v-card
    class="product-card h-100"
    elevation="2"
    hover
    :to="`/products/${product.id}`"
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
        Продавец: {{ product.brand_name || product.brand?.name || 'Без бренда' }}
      </div>
      <div class="price">
        {{ formatPrice(product.price) }} ₽
      </div>
      <div class="text-body-2 text-grey mb-2">
        {{ product.description }}
      </div>
      <div class="product-title">
        {{ product.name }}
      </div>
    </v-card-text>
    <v-card-actions>
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

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

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

const emit = defineEmits(['add-to-cart', 'edit'])
const router = useRouter()
const authStore = useAuthStore()

const handleAddToCart = () => {
  if (!authStore.isAuthenticated) {
    router.push('/register')
    return
  }
  emit('add-to-cart', props.product)
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU').format(price)
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
  max-width: 320px;
  margin: 0 auto;
  will-change: transform;
  border: 2px solid transparent;
}
.product-card:hover {
  transform: translateY(-4px) scale(1.01);
  box-shadow: 0 8px 32px rgba(25, 118, 210, 0.25), 0 3px 8px rgba(0,0,0,0.10);
  border-color: #1976d2;
}
.product-card .v-img {
  height: 220px !important;
  width: 100% !important;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
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
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.product-card .brand {
  color: #6b7280;
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 8px;
  letter-spacing: 0.02em;
}
.product-card .price {
  color: #222;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 8px;
  letter-spacing: 0.01em;
}
.product-card .v-card-actions {
  padding: 8px 16px 16px;
}
.add-to-cart-btn {
  background: linear-gradient(90deg, #1976d2 0%, #42a5f5 100%);
  color: #fff !important;
  font-weight: 700;
  font-size: 1.1rem;
  height: 48px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.08);
  transition: background 0.2s, box-shadow 0.2s;
}
.add-to-cart-btn:hover {
  background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%);
  box-shadow: 0 4px 16px rgba(25, 118, 210, 0.16);
}
.product-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #222;
  margin-top: 8px;
  margin-bottom: 0;
  line-height: 1.3;
  word-break: break-word;
}
</style> 