<template>
  <div class="cart-view">
    <h1>Корзина</h1>

    <transition name="fade" mode="out-in">
      <div v-if="cartStore.items.length === 0" class="empty-cart">
        <p>Ваша корзина пуста</p>
        <router-link to="/products" class="btn-primary">
          Перейти к товарам
        </router-link>
      </div>

      <div v-else class="cart-content">
        <div class="cart-items">
          <transition-group name="list" tag="div">
            <div v-for="item in cartStore.items" :key="item.productId" class="cart-item">
              <div class="item-image">
                <img :src="item.imageUrl || '/placeholder.png'" :alt="item.name">
              </div>
              
              <div class="item-details">
                <h3>{{ item.name }}</h3>
                <p class="price">{{ formatPrice(item.price) }}</p>
              </div>

              <div class="item-quantity">
                <button 
                  @click="cartStore.updateQuantity(item.productId, item.quantity - 1)"
                  class="quantity-btn"
                >
                  -
                </button>
                <span class="quantity">{{ item.quantity }}</span>
                <button 
                  @click="cartStore.updateQuantity(item.productId, item.quantity + 1)"
                  class="quantity-btn"
                >
                  +
                </button>
              </div>

              <div class="item-total">
                {{ formatPrice(item.price * item.quantity) }}
              </div>

              <button 
                @click="cartStore.removeFromCart(item.productId)"
                class="remove-btn"
                title="Удалить товар"
              >
                ×
              </button>
            </div>
          </transition-group>
        </div>

        <div class="cart-summary">
          <div class="summary-row">
            <span>Товаров:</span>
            <span>{{ cartStore.totalItems }} шт.</span>
          </div>
          <div class="summary-row total">
            <span>Итого:</span>
            <span>{{ formatPrice(cartStore.totalPrice) }}</span>
          </div>
          <button 
            @click="proceedToCheckout"
            class="btn-primary checkout-btn"
          >
            Оформить заказ
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { useCartStore } from '@/stores/cartStore'
import { useRouter } from 'vue-router'

const cartStore = useCartStore()
const router = useRouter()

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB'
  }).format(price)
}

const proceedToCheckout = () => {
  // TODO: Implement checkout process
  router.push('/checkout')
}
</script>

<style scoped>
.cart-view {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.empty-cart {
  text-align: center;
  padding: 40px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-top: 20px;
}

.empty-cart p {
  margin-bottom: 20px;
  color: #666;
  font-size: 1.2rem;
}

.cart-content {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 20px;
  margin-top: 20px;
}

.cart-items {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.cart-item {
  display: grid;
  grid-template-columns: 100px 1fr auto auto auto;
  gap: 20px;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.cart-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 100px;
  height: 100px;
  overflow: hidden;
  border-radius: 4px;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-details h3 {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
}

.price {
  color: #666;
  margin: 0;
}

.item-quantity {
  display: flex;
  align-items: center;
  gap: 8px;
}

.quantity-btn {
  width: 30px;
  height: 30px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.quantity-btn:hover {
  background-color: #f8f9fa;
  transform: scale(1.1);
}

.quantity {
  min-width: 30px;
  text-align: center;
}

.item-total {
  font-weight: bold;
  color: #2c3e50;
}

.remove-btn {
  background: none;
  border: none;
  color: #dc3545;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0 8px;
  transition: transform 0.2s;
}

.remove-btn:hover {
  transform: scale(1.2);
}

.cart-summary {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 20px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  color: #666;
}

.summary-row.total {
  font-size: 1.2rem;
  font-weight: bold;
  color: #2c3e50;
  border-top: 1px solid #eee;
  padding-top: 12px;
  margin-top: 12px;
}

.checkout-btn {
  width: 100%;
  margin-top: 20px;
  padding: 12px;
  font-size: 1.1rem;
  transition: transform 0.2s, background-color 0.2s;
}

.checkout-btn:hover {
  transform: translateY(-2px);
  background-color: #45a049;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: transform 0.2s, background-color 0.2s;
}

.btn-primary:hover {
  transform: translateY(-1px);
  background-color: #45a049;
}

/* Анимации */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.list-move {
  transition: transform 0.5s ease;
}
</style> 