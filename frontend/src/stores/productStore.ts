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

interface PaginationInfo {
  count: number
  next: string | null
  previous: string | null
  page_size: number
  current_page: number
  total_pages: number
}

export const useProductStore = defineStore('product', () => {
  const products = ref<Product[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const pagination = ref<PaginationInfo>({
    count: 0,
    next: null,
    previous: null,
    page_size: 10,
    current_page: 1,
    total_pages: 0
  })

  const fetchProducts = async (params?: Record<string, any>) => {
    loading.value = true
    error.value = null
    try {
      const queryParams = { ...params };
      const response = await api.get('/productlist/', { params: queryParams })
      if (response.data.results) {
        products.value = response.data.results
        pagination.value = {
          count: response.data.count || 0,
          next: response.data.next,
          previous: response.data.previous,
          page_size: response.data.page_size || 10,
          current_page: response.data.current_page || 1,
          total_pages: response.data.total_pages || Math.ceil((response.data.count || 0) / (response.data.page_size || 10))
        }
      } else {
        products.value = response.data
        pagination.value = {
          count: Array.isArray(response.data) ? response.data.length : 0,
          next: null,
          previous: null,
          page_size: Array.isArray(response.data) ? response.data.length : 0,
          current_page: 1,
          total_pages: 1
        }
      }
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Ошибка при загрузке товаров'
      console.error('Error fetching products:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  const fetchNextPage = async () => {
    if (!hasNextPage.value) return
    loading.value = true
    error.value = null
    try {
      const response = await api.get(pagination.value.next!)
      products.value = [...products.value, ...response.data.results]
      pagination.value = {
        count: response.data.count || pagination.value.count,
        next: response.data.next,
        previous: response.data.previous,
        page_size: response.data.page_size || pagination.value.page_size,
        current_page: response.data.current_page || pagination.value.current_page + 1,
        total_pages: response.data.total_pages || pagination.value.total_pages
      }
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Ошибка при загрузке следующей страницы'
      console.error('Error fetching next page:', e)
    } finally {
      loading.value = false
    }
  }

  const fetchPreviousPage = async () => {
    if (!hasPreviousPage.value) return
    loading.value = true
    error.value = null
    try {
      const response = await api.get(pagination.value.previous!)
      products.value = response.data.results
      pagination.value = {
        count: response.data.count || pagination.value.count,
        next: response.data.next,
        previous: response.data.previous,
        page_size: response.data.page_size || pagination.value.page_size,
        current_page: response.data.current_page || pagination.value.current_page - 1,
        total_pages: response.data.total_pages || pagination.value.total_pages
      }
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Ошибка при загрузке предыдущей страницы'
      console.error('Error fetching previous page:', e)
    } finally {
      loading.value = false
    }
  }

  const fetchPage = async (page: number, params?: Record<string, any>) => {
    loading.value = true
    error.value = null
    try {
      const requestParams = { ...params, page };
      const response = await api.get('/productlist/', { params: requestParams })
      if (response.data.results) {
        products.value = response.data.results
        pagination.value = {
          count: response.data.count || 0,
          next: response.data.next,
          previous: response.data.previous,
          page_size: response.data.page_size || 10,
          current_page: page,
          total_pages: response.data.total_pages || Math.ceil((response.data.count || 0) / (response.data.page_size || 10))
        }
      }
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Ошибка при загрузке страницы'
      console.error('Error fetching page:', e)
    } finally {
      loading.value = false
    }
  }

  const hasNextPage = computed(() => pagination.value.next !== null)
  const hasPreviousPage = computed(() => pagination.value.previous !== null)

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
    pagination,
    hasNextPage,
    hasPreviousPage,
    fetchProducts,
    fetchNextPage,
    fetchPreviousPage,
    fetchPage,
    getProductById,
    getProductsBySearch,
    addProduct,
    updateProduct,
    deleteProduct
  }
}) 