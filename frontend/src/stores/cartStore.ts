import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface CartItem {
  productId: number
  name: string
  price: number
  quantity: number
  imageUrl?: string
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const totalItems = computed(() => {
    return items.value.reduce((sum, item) => sum + item.quantity, 0)
  })

  const totalPrice = computed(() => {
    return items.value.reduce((sum, item) => sum + (item.price * item.quantity), 0)
  })

  // Actions
  const addToCart = (product: { id: number, name: string, price: number, imageUrl?: string }) => {
    const existingItem = items.value.find(item => item.productId === product.id)
    
    if (existingItem) {
      existingItem.quantity++
    } else {
      items.value.push({
        productId: product.id,
        name: product.name,
        price: product.price,
        quantity: 1,
        imageUrl: product.imageUrl
      })
    }

    // Сохраняем корзину в localStorage
    saveCart()
  }

  const removeFromCart = (productId: number) => {
    items.value = items.value.filter(item => item.productId !== productId)
    saveCart()
  }

  const updateQuantity = (productId: number, quantity: number) => {
    const item = items.value.find(item => item.productId === productId)
    if (item) {
      if (quantity <= 0) {
        removeFromCart(productId)
      } else {
        item.quantity = quantity
      }
      saveCart()
    }
  }

  const clearCart = () => {
    items.value = []
    saveCart()
  }

  // Сохранение корзины в localStorage
  const saveCart = () => {
    localStorage.setItem('cart', JSON.stringify(items.value))
  }

  // Загрузка корзины из localStorage
  const loadCart = () => {
    const savedCart = localStorage.getItem('cart')
    if (savedCart) {
      items.value = JSON.parse(savedCart)
    }
  }

  // Инициализация корзины при создании store
  loadCart()

  return {
    items,
    loading,
    error,
    totalItems,
    totalPrice,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart
  }
}) 