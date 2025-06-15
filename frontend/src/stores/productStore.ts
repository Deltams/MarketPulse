import { defineStore } from 'pinia'
import axios from 'axios'

interface Product {
  id: number
  name: string
  description: string
  price: number
  imageUrl?: string
}

export const useProductStore = defineStore('product', {
  state: () => ({
    products: [] as Product[],
    loading: false,
    error: null as string | null
  }),

  actions: {
    async fetchProducts() {
      console.log('Fetching products...')
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('http://localhost:8000/api/v1/productlist/')
        console.log('Response:', response)
        console.log('Response data:', response.data)
        
        // Убедимся, что данные являются массивом
        const products = Array.isArray(response.data) ? response.data : []
        
        // Обновляем состояние
        this.products = products
        console.log('Products after update:', this.products)
      } catch (error) {
        console.error('Error fetching products:', error)
        this.error = 'Failed to load products'
        this.products = []
      } finally {
        this.loading = false
      }
    },

    async createProduct(productData: Omit<Product, 'id'>) {
      try {
        const response = await axios.post('http://localhost:8000/api/v1/productlist/', productData)
        this.products.push(response.data)
      } catch (error) {
        console.error('Error creating product:', error)
        throw error
      }
    },

    async updateProduct(id: number, productData: Partial<Product>) {
      try {
        const response = await axios.put(`http://localhost:8000/api/v1/productlist/${id}/`, productData)
        const index = this.products.findIndex(p => p.id === id)
        if (index !== -1) {
          this.products[index] = response.data
        }
      } catch (error) {
        console.error('Error updating product:', error)
        throw error
      }
    },

    async deleteProduct(id: number) {
      try {
        await axios.delete(`http://localhost:8000/api/v1/productlist/${id}/`)
        this.products = this.products.filter(p => p.id !== id)
      } catch (error) {
        console.error('Error deleting product:', error)
        throw error
      }
    }
  }
}) 