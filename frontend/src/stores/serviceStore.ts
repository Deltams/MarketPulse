import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/config'

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

interface PaginationInfo {
  count: number
  next: string | null
  previous: string | null
  page_size: number
  current_page: number
  total_pages: number
}

export const useServiceStore = defineStore('service', () => {
  const services = ref<Service[]>([])
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

  // Getters
  const activeServices = computed(() => {
    return services.value.filter(service => service.is_active)
  })

  const getServiceById = computed(() => {
    return (id: number) => services.value.find(service => service.id === id)
  })

  const hasNextPage = computed(() => pagination.value.next !== null)
  const hasPreviousPage = computed(() => pagination.value.previous !== null)

  // Actions
  const fetchServices = async (params?: Record<string, any>) => {
    loading.value = true
    error.value = null
    
    try {
      const queryParams = { ...params };
      const response = await api.get('/servicelist/', { params: queryParams })
      
      if (response.data.results) {
        // Пагинированный ответ
        services.value = response.data.results
        pagination.value = {
          count: response.data.count || 0,
          next: response.data.next,
          previous: response.data.previous,
          page_size: response.data.page_size || 10,
          current_page: response.data.current_page || 1,
          total_pages: response.data.total_pages || Math.ceil((response.data.count || 0) / (response.data.page_size || 10))
        }
      } else {
        // Непагинированный ответ
        services.value = response.data
        pagination.value = {
          count: response.data.length || 0,
          next: null,
          previous: null,
          page_size: response.data.length || 0,
          current_page: 1,
          total_pages: 1
        }
      }
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при загрузке услуг'
      console.error('Error fetching services:', err)
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
      services.value = [...services.value, ...response.data.results]
      pagination.value = {
        count: response.data.count || pagination.value.count,
        next: response.data.next,
        previous: response.data.previous,
        page_size: response.data.page_size || pagination.value.page_size,
        current_page: response.data.current_page || pagination.value.current_page + 1,
        total_pages: response.data.total_pages || pagination.value.total_pages
      }
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при загрузке следующей страницы'
      console.error('Error fetching next page:', err)
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
      services.value = response.data.results
      pagination.value = {
        count: response.data.count || pagination.value.count,
        next: response.data.next,
        previous: response.data.previous,
        page_size: response.data.page_size || pagination.value.page_size,
        current_page: response.data.current_page || pagination.value.current_page - 1,
        total_pages: response.data.total_pages || pagination.value.total_pages
      }
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при загрузке предыдущей страницы'
      console.error('Error fetching previous page:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchPage = async (page: number, params?: Record<string, any>) => {
    loading.value = true
    error.value = null
    
    try {
      const requestParams = { ...params, page };
      const response = await api.get('/servicelist/', { params: requestParams })
      
      if (response.data.results) {
        services.value = response.data.results
        pagination.value = {
          count: response.data.count || 0,
          next: response.data.next,
          previous: response.data.previous,
          page_size: response.data.page_size || 10,
          current_page: page,
          total_pages: response.data.total_pages || Math.ceil((response.data.count || 0) / (response.data.page_size || 10))
        }
      }
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при загрузке страницы'
      console.error('Error fetching page:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchService = async (id: number) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.get(`/servicelist/${id}/`)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при загрузке услуги'
      console.error('Error fetching service:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createService = async (serviceData: Partial<Service>) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.post('/servicelist/', serviceData)
      services.value.push(response.data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при создании услуги'
      console.error('Error creating service:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateService = async (id: number, serviceData: Partial<Service>) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.put(`/servicelist/${id}/`, serviceData)
      const index = services.value.findIndex(service => service.id === id)
      if (index !== -1) {
        services.value[index] = response.data
      }
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при обновлении услуги'
      console.error('Error updating service:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteService = async (id: number) => {
    loading.value = true
    error.value = null
    
    try {
      await api.delete(`/servicelist/${id}/`)
      services.value = services.value.filter(service => service.id !== id)
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при удалении услуги'
      console.error('Error deleting service:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    services,
    loading,
    error,
    pagination,
    activeServices,
    getServiceById,
    hasNextPage,
    hasPreviousPage,
    fetchServices,
    fetchNextPage,
    fetchPreviousPage,
    fetchPage,
    fetchService,
    createService,
    updateService,
    deleteService
  }
}) 