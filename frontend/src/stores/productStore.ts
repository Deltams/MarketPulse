import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/config'

interface Product {
  id: number
  name: string
  description: string
  price: number
  image: string
  category: number
  brand: number
  seller: number
  stock: number
  created_at: string
  updated_at: string
}

export const useProductStore = defineStore('product', () => {
  const products = ref<Product[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchProducts = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/productlist/')
      products.value = response.data
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Ошибка при загрузке товаров'
      console.error('Error fetching products:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  const getProductById = (id: number) => {
    return products.value.find(product => product.id === id)
  }

  const getProductsBySearch = computed(() => {
    return (searchTerm: string) => {
      const term = searchTerm.toLowerCase()
      return products.value.filter(p => 
        p.name.toLowerCase().includes(term) ||
        p.description.toLowerCase().includes(term)
      )
    }
  })

  const addProduct = async (product: Omit<Product, 'id' | 'created_at' | 'updated_at'>) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/productlist/', product)
      products.value.push(response.data)
      return response.data
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Ошибка при добавлении товара'
      throw e
    } finally {
      loading.value = false
    }
  }

  const updateProduct = async (id: number, product: Partial<Product>) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.patch(`/productlist/${id}/`, product)
      const index = products.value.findIndex(p => p.id === id)
      if (index !== -1) {
        products.value[index] = response.data
      }
      return response.data
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Ошибка при обновлении товара'
      throw e
    } finally {
      loading.value = false
    }
  }

  const deleteProduct = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      await api.delete(`/productlist/${id}/`)
      products.value = products.value.filter(p => p.id !== id)
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Ошибка при удалении товара'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    products,
    loading,
    error,
    fetchProducts,
    getProductById,
    getProductsBySearch,
    addProduct,
    updateProduct,
    deleteProduct
  }
}) 