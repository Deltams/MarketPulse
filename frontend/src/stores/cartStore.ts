import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/config'

interface CartItem {
  id?: number
  productId?: number
  serviceId?: number
  name: string
  price: number
  quantity: number
  imageUrl?: string
  type: 'product' | 'service'
  product_name?: string
  service_name?: string
  product_price?: number
  service_price?: number
  product_image?: string
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
    return items.value.reduce((sum, item) => {
      const price = item.type === 'product' ? item.product_price || item.price : item.service_price || item.price
      return sum + (price * item.quantity)
    }, 0)
  })

  // Actions
  const addToCart = async (item: { id: number, name: string, price: number, imageUrl?: string, type: 'product' | 'service' }) => {
    if (!api.defaults.headers.common['Authorization']) {
      // If not authenticated, use localStorage
      const existingItem = items.value.find(cartItem => {
        if (item.type === 'product') {
          return cartItem.productId === item.id && cartItem.type === 'product'
        } else {
          return cartItem.serviceId === item.id && cartItem.type === 'service'
        }
      })
      
      if (existingItem) {
        existingItem.quantity++
      } else {
        const newItem: CartItem = {
          name: item.name,
          price: item.price,
          quantity: 1,
          type: item.type
        }
        
        if (item.type === 'product') {
          newItem.productId = item.id
          newItem.imageUrl = item.imageUrl
        } else {
          newItem.serviceId = item.id
        }
        
        items.value.push(newItem)
      }
      saveCart()
      return
    }

    try {
      loading.value = true
      const cartData = {
        item_type: item.type,
        quantity: 1
      }

      if (item.type === 'product') {
        cartData.product = item.id
      } else {
        cartData.service = item.id
      }

      const response = await api.post('/cart_items/', cartData)
      await fetchCartItems()
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при добавлении в корзину'
      console.error('Error adding to cart:', err)
    } finally {
      loading.value = false
    }
  }

  const removeFromCart = async (itemId: number, type: 'product' | 'service') => {
    if (!api.defaults.headers.common['Authorization']) {
      items.value = items.value.filter(item => {
        if (type === 'product') {
          return item.productId !== itemId
        } else {
          return item.serviceId !== itemId
        }
      })
      saveCart()
      return
    }

    try {
      loading.value = true
      const item = items.value.find(cartItem => {
        if (type === 'product') {
          return cartItem.productId === itemId
        } else {
          return cartItem.serviceId === itemId
        }
      })

      if (item?.id) {
        await api.delete(`/cart_items/${item.id}/`)
        await fetchCartItems()
      }
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при удалении из корзины'
      console.error('Error removing from cart:', err)
    } finally {
      loading.value = false
    }
  }

  const updateQuantity = async (itemId: number, quantity: number, type: 'product' | 'service') => {
    if (!api.defaults.headers.common['Authorization']) {
      const item = items.value.find(cartItem => {
        if (type === 'product') {
          return cartItem.productId === itemId
        } else {
          return cartItem.serviceId === itemId
        }
      })
      
      if (item) {
        if (quantity <= 0) {
          removeFromCart(itemId, type)
        } else {
          item.quantity = quantity
        }
        saveCart()
      }
      return
    }

    try {
      loading.value = true
      const item = items.value.find(cartItem => {
        if (type === 'product') {
          return cartItem.productId === itemId
        } else {
          return cartItem.serviceId === itemId
        }
      })

      if (item?.id) {
        if (quantity <= 0) {
          await removeFromCart(itemId, type)
        } else {
          await api.put(`/cart_items/${item.id}/`, { quantity })
          await fetchCartItems()
        }
      }
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при обновлении количества'
      console.error('Error updating quantity:', err)
    } finally {
      loading.value = false
    }
  }

  const clearCart = async () => {
    if (!api.defaults.headers.common['Authorization']) {
      items.value = []
      saveCart()
      return
    }

    try {
      loading.value = true
      for (const item of items.value) {
        if (item.id) {
          await api.delete(`/cart_items/${item.id}/`)
        }
      }
      items.value = []
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при очистке корзины'
      console.error('Error clearing cart:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchCartItems = async () => {
    if (!api.defaults.headers.common['Authorization']) {
      return
    }

    try {
      loading.value = true
      const response = await api.get('/cart_items/')
      items.value = response.data.map((item: any) => ({
        id: item.id,
        productId: item.product,
        serviceId: item.service,
        name: item.product_name || item.service_name || '',
        price: item.product_price || item.service_price || 0,
        quantity: item.quantity,
        type: item.item_type,
        imageUrl: item.product_image,
        product_name: item.product_name,
        service_name: item.service_name,
        product_price: item.product_price,
        service_price: item.service_price,
        product_image: item.product_image
      }))
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при загрузке корзины'
      console.error('Error fetching cart items:', err)
    } finally {
      loading.value = false
    }
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
    clearCart,
    fetchCartItems
  }
}) 