<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-6">Панель администратора</h1>

        <v-tabs v-model="activeTab" class="mb-6">
          <v-tab value="users">Пользователи</v-tab>
          <v-tab value="categories">Категории</v-tab>
          <v-tab value="orders">Заказы</v-tab>
        </v-tabs>

        <v-window v-model="activeTab">
          <!-- Пользователи -->
          <v-window-item value="users">
            <div class="d-flex justify-space-between align-center mb-4">
              <h2 class="text-h5">Управление пользователями</h2>
              <BaseButton
                color="primary"
                variant="elevated"
                prepend-icon="mdi-account-plus"
                @click="openUserDialog()"
              >
                Добавить пользователя
              </BaseButton>
            </div>

            <v-data-table
              :headers="userHeaders"
              :items="users"
              :loading="loading"
              class="elevation-1"
            >
              <template v-slot:item.role="{ item }">
                <v-chip
                  :color="getRoleColor(item.role)"
                  size="small"
                >
                  {{ getRoleText(item.role) }}
                </v-chip>
              </template>

              <template v-slot:item.actions="{ item }">
                <div class="d-flex gap-2">
                  <BaseButton
                    color="primary"
                    variant="text"
                    size="small"
                    @click="openUserDialog(item)"
                  >
                    Редактировать
                  </BaseButton>
                  <BaseButton
                    color="error"
                    variant="text"
                    size="small"
                    @click="confirmDeleteUser(item)"
                  >
                    Удалить
                  </BaseButton>
                </div>
              </template>
            </v-data-table>
          </v-window-item>

          <!-- Категории -->
          <v-window-item value="categories">
            <div class="d-flex justify-space-between align-center mb-4">
              <h2 class="text-h5">Управление категориями</h2>
              <BaseButton
                color="primary"
                variant="elevated"
                prepend-icon="mdi-folder-plus"
                @click="openCategoryDialog()"
              >
                Добавить категорию
              </BaseButton>
            </div>

            <v-data-table
              :headers="categoryHeaders"
              :items="categories"
              :loading="loading"
              class="elevation-1"
            >
              <template v-slot:item.actions="{ item }">
                <div class="d-flex gap-2">
                  <BaseButton
                    color="primary"
                    variant="text"
                    size="small"
                    @click="openCategoryDialog(item)"
                  >
                    Редактировать
                  </BaseButton>
                  <BaseButton
                    color="error"
                    variant="text"
                    size="small"
                    @click="confirmDeleteCategory(item)"
                  >
                    Удалить
                  </BaseButton>
                </div>
              </template>
            </v-data-table>
          </v-window-item>

          <!-- Заказы -->
          <v-window-item value="orders">
            <h2 class="text-h5 mb-4">Управление заказами</h2>

            <v-data-table
              :headers="orderHeaders"
              :items="orders"
              :loading="loading"
              class="elevation-1"
            >
              <template v-slot:item.status="{ item }">
                <v-chip
                  :color="getStatusColor(item.status)"
                  size="small"
                >
                  {{ getStatusText(item.status) }}
                </v-chip>
              </template>

              <template v-slot:item.actions="{ item }">
                <div class="d-flex gap-2">
                  <BaseButton
                    color="primary"
                    variant="text"
                    size="small"
                    @click="openOrderDialog(item)"
                  >
                    Просмотр
                  </BaseButton>
                  <BaseButton
                    v-if="item.status === 'pending'"
                    color="success"
                    variant="text"
                    size="small"
                    @click="updateOrderStatus(item, 'processing')"
                  >
                    Принять
                  </BaseButton>
                  <BaseButton
                    v-if="item.status === 'processing'"
                    color="info"
                    variant="text"
                    size="small"
                    @click="updateOrderStatus(item, 'shipped')"
                  >
                    Отправить
                  </BaseButton>
                </div>
              </template>
            </v-data-table>
          </v-window-item>
        </v-window>
      </v-col>
    </v-row>

    <!-- Диалоги -->
    <v-dialog
      v-model="userDialog"
      max-width="500px"
    >
      <v-card>
        <v-card-title class="text-h5">
          {{ editingUser ? 'Редактирование пользователя' : 'Добавление пользователя' }}
        </v-card-title>

        <v-card-text>
          <BaseForm
            ref="userForm"
            :loading="saving"
            @submit="handleUserSubmit"
            @cancel="userDialog = false"
          >
            <BaseInput
              v-model="userFormData.name"
              label="Имя"
              :rules="[v => !!v || 'Обязательное поле']"
            />

            <BaseInput
              v-model="userFormData.email"
              label="Email"
              type="email"
              :rules="[
                v => !!v || 'Обязательное поле',
                v => /.+@.+\..+/.test(v) || 'Некорректный email'
              ]"
            />

            <BaseInput
              v-if="!editingUser"
              v-model="userFormData.password"
              label="Пароль"
              type="password"
              :rules="[
                v => !!v || 'Обязательное поле',
                v => v.length >= 6 || 'Минимум 6 символов'
              ]"
            />

            <v-select
              v-model="userFormData.role"
              :items="roleOptions"
              label="Роль"
              :rules="[v => !!v || 'Обязательное поле']"
            ></v-select>
          </BaseForm>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="categoryDialog"
      max-width="500px"
    >
      <v-card>
        <v-card-title class="text-h5">
          {{ editingCategory ? 'Редактирование категории' : 'Добавление категории' }}
        </v-card-title>

        <v-card-text>
          <BaseForm
            ref="categoryForm"
            :loading="saving"
            @submit="handleCategorySubmit"
            @cancel="categoryDialog = false"
          >
            <BaseInput
              v-model="categoryFormData.name"
              label="Название"
              :rules="[v => !!v || 'Обязательное поле']"
            />
          </BaseForm>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Диалог подтверждения удаления -->
    <v-dialog
      v-model="deleteDialog"
      max-width="400px"
    >
      <v-card>
        <v-card-title class="text-h5">
          Подтверждение удаления
        </v-card-title>

        <v-card-text>
          Вы уверены, что хотите удалить этот элемент?
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <BaseButton
            color="grey"
            variant="text"
            @click="deleteDialog = false"
          >
            Отмена
          </BaseButton>
          <BaseButton
            color="error"
            variant="elevated"
            :loading="deleting"
            @click="handleDelete"
          >
            Удалить
          </BaseButton>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import BaseButton from '../components/common/BaseButton.vue'
import BaseForm from '../components/common/BaseForm.vue'
import BaseInput from '../components/common/BaseInput.vue'

// Интерфейсы
interface User {
  id: number
  name: string
  email: string
  role: 'buyer' | 'seller' | 'admin'
}

interface Category {
  id: number
  name: string
}

interface Order {
  id: number
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'
  total: number
  createdAt: string
}

// Состояние
const authStore = useAuthStore()
const activeTab = ref('users')
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)

// Пользователи
const users = ref<User[]>([])
const userDialog = ref(false)
const editingUser = ref<User | null>(null)
const userFormData = ref({
  name: '',
  email: '',
  password: '',
  role: 'buyer' as User['role']
})

// Категории
const categories = ref<Category[]>([])
const categoryDialog = ref(false)
const editingCategory = ref<Category | null>(null)
const categoryFormData = ref({
  name: ''
})

// Заказы
const orders = ref<Order[]>([])

// Диалог удаления
const deleteDialog = ref(false)
const itemToDelete = ref<{ type: 'user' | 'category', id: number } | null>(null)

// Заголовки таблиц
const userHeaders = [
  { title: 'ID', key: 'id' },
  { title: 'Имя', key: 'name' },
  { title: 'Email', key: 'email' },
  { title: 'Роль', key: 'role' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const categoryHeaders = [
  { title: 'ID', key: 'id' },
  { title: 'Название', key: 'name' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const orderHeaders = [
  { title: 'ID', key: 'id' },
  { title: 'Статус', key: 'status' },
  { title: 'Сумма', key: 'total' },
  { title: 'Дата', key: 'createdAt' },
  { title: 'Действия', key: 'actions', sortable: false }
]

// Опции для селекта ролей
const roleOptions = [
  { title: 'Покупатель', value: 'buyer' },
  { title: 'Продавец', value: 'seller' },
  { title: 'Администратор', value: 'admin' }
]

// Вспомогательные функции
const getRoleColor = (role: User['role']) => {
  const colors = {
    buyer: 'primary',
    seller: 'success',
    admin: 'error'
  }
  return colors[role]
}

const getRoleText = (role: User['role']) => {
  const texts = {
    buyer: 'Покупатель',
    seller: 'Продавец',
    admin: 'Администратор'
  }
  return texts[role]
}

const getStatusColor = (status: Order['status']) => {
  const colors = {
    pending: 'warning',
    processing: 'info',
    shipped: 'primary',
    delivered: 'success',
    cancelled: 'error'
  }
  return colors[status]
}

const getStatusText = (status: Order['status']) => {
  const texts = {
    pending: 'Ожидает оплаты',
    processing: 'В обработке',
    shipped: 'Отправлен',
    delivered: 'Доставлен',
    cancelled: 'Отменен'
  }
  return texts[status]
}

// Методы для работы с пользователями
const openUserDialog = (user?: User) => {
  editingUser.value = user || null
  if (user) {
    userFormData.value = {
      name: user.name,
      email: user.email,
      password: '',
      role: user.role
    }
  } else {
    userFormData.value = {
      name: '',
      email: '',
      password: '',
      role: 'buyer'
    }
  }
  userDialog.value = true
}

const handleUserSubmit = async () => {
  saving.value = true
  try {
    if (editingUser.value?.id) {
      // Здесь будет запрос к API для обновления
      // await axios.put(`/api/admin/users/${editingUser.value.id}`, userFormData.value)
      console.log('Updating user:', userFormData.value)
    } else {
      // Здесь будет запрос к API для создания
      // await axios.post('/api/admin/users', userFormData.value)
      console.log('Creating user:', userFormData.value)
    }
    userDialog.value = false
    fetchUsers()
  } catch (error) {
    console.error('Failed to save user:', error)
  } finally {
    saving.value = false
  }
}

const confirmDeleteUser = (user: User) => {
  itemToDelete.value = { type: 'user', id: user.id }
  deleteDialog.value = true
}

// Методы для работы с категориями
const openCategoryDialog = (category?: Category) => {
  editingCategory.value = category || null
  categoryFormData.value = {
    name: category?.name || ''
  }
  categoryDialog.value = true
}

const handleCategorySubmit = async () => {
  saving.value = true
  try {
    if (editingCategory.value?.id) {
      // Здесь будет запрос к API для обновления
      // await axios.put(`/api/admin/categories/${editingCategory.value.id}`, categoryFormData.value)
      console.log('Updating category:', categoryFormData.value)
    } else {
      // Здесь будет запрос к API для создания
      // await axios.post('/api/admin/categories', categoryFormData.value)
      console.log('Creating category:', categoryFormData.value)
    }
    categoryDialog.value = false
    fetchCategories()
  } catch (error) {
    console.error('Failed to save category:', error)
  } finally {
    saving.value = false
  }
}

const confirmDeleteCategory = (category: Category) => {
  itemToDelete.value = { type: 'category', id: category.id }
  deleteDialog.value = true
}

// Методы для работы с заказами
const openOrderDialog = (order: Order) => {
  // Здесь будет открытие диалога с деталями заказа
  console.log('Opening order:', order)
}

const updateOrderStatus = async (order: Order, status: Order['status']) => {
  try {
    // Здесь будет запрос к API для обновления статуса
    // await axios.put(`/api/admin/orders/${order.id}/status`, { status })
    console.log('Updating order status:', { orderId: order.id, status })
    fetchOrders()
  } catch (error) {
    console.error('Failed to update order status:', error)
  }
}

// Общие методы
const handleDelete = async () => {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    if (itemToDelete.value.type === 'user') {
      // Здесь будет запрос к API для удаления пользователя
      // await axios.delete(`/api/admin/users/${itemToDelete.value.id}`)
      console.log('Deleting user:', itemToDelete.value.id)
      fetchUsers()
    } else {
      // Здесь будет запрос к API для удаления категории
      // await axios.delete(`/api/admin/categories/${itemToDelete.value.id}`)
      console.log('Deleting category:', itemToDelete.value.id)
      fetchCategories()
    }
    deleteDialog.value = false
  } catch (error) {
    console.error('Failed to delete item:', error)
  } finally {
    deleting.value = false
  }
}

// Методы загрузки данных
const fetchUsers = async () => {
  loading.value = true
  try {
    // Здесь будет запрос к API
    // const response = await axios.get('/api/admin/users')
    // users.value = response.data

    // Временные данные для демонстрации
    users.value = [
      {
        id: 1,
        name: 'Пользователь 1',
        email: 'user1@example.com',
        role: 'buyer'
      }
    ]
  } catch (error) {
    console.error('Failed to fetch users:', error)
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  loading.value = true
  try {
    // Здесь будет запрос к API
    // const response = await axios.get('/api/admin/categories')
    // categories.value = response.data

    // Временные данные для демонстрации
    categories.value = [
      {
        id: 1,
        name: 'Категория 1'
      }
    ]
  } catch (error) {
    console.error('Failed to fetch categories:', error)
  } finally {
    loading.value = false
  }
}

const fetchOrders = async () => {
  loading.value = true
  try {
    // Здесь будет запрос к API
    // const response = await axios.get('/api/admin/orders')
    // orders.value = response.data

    // Временные данные для демонстрации
    orders.value = [
      {
        id: 1,
        status: 'pending',
        total: 1000,
        createdAt: '2024-03-15T10:00:00Z'
      }
    ]
  } catch (error) {
    console.error('Failed to fetch orders:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUsers()
  fetchCategories()
  fetchOrders()
})
</script> 