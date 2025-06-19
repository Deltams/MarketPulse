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

export const useServiceStore = defineStore('service', () => {
  const services = ref<Service[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const activeServices = computed(() => {
    return services.value.filter(service => service.is_active)
  })

  const getServiceById = computed(() => {
    return (id: number) => services.value.find(service => service.id === id)
  })

  // Actions
  const fetchServices = async (params?: Record<string, any>) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.get('/servicelist/', { params })
      services.value = response.data.results || response.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при загрузке услуг'
      console.error('Error fetching services:', err)
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
    activeServices,
    getServiceById,
    fetchServices,
    fetchService,
    createService,
    updateService,
    deleteService
  }
}) 