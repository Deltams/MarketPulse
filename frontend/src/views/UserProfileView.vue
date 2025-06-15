<template>
  <div class="profile">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else>
      <div class="profile-container">
        <h1>User Profile</h1>
        
        <div class="profile-section">
          <h2>Personal Information</h2>
          <div class="info-grid">
            <div class="info-item">
              <label>Username</label>
              <div>{{ profile.username }}</div>
            </div>
            <div class="info-item">
              <label>Email</label>
              <div>{{ profile.email }}</div>
            </div>
            <div class="info-item">
              <label>First Name</label>
              <div>{{ profile.first_name }}</div>
            </div>
            <div class="info-item">
              <label>Last Name</label>
              <div>{{ profile.last_name }}</div>
            </div>
          </div>
        </div>

        <div class="profile-section">
          <h2>Account Actions</h2>
          <div class="actions">
            <button class="action-button" @click="handleLogout">
              Logout
            </button>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api/config';

interface UserProfile {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

const router = useRouter();
const profile = ref<UserProfile | null>(null);
const loading = ref(true);
const error = ref('');

const fetchProfile = async () => {
  try {
    const response = await api.get('/userprofilelist/');
    profile.value = response.data;
  } catch (err) {
    error.value = 'Failed to load profile';
    console.error('Error fetching profile:', err);
  } finally {
    loading.value = false;
  }
};

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

onMounted(() => {
  fetchProfile();
});
</script>

<style scoped>
.profile {
  padding: 2rem;
}

.profile-container {
  max-width: 800px;
  margin: 0 auto;
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #2c3e50;
  margin: 0 0 2rem 0;
}

.profile-section {
  margin-bottom: 2rem;
}

h2 {
  color: #2c3e50;
  margin: 0 0 1rem 0;
  font-size: 1.25rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  color: #666;
  font-size: 0.9rem;
}

.actions {
  display: flex;
  gap: 1rem;
}

.action-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.action-button:hover {
  background-color: #c82333;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #dc3545;
  text-align: center;
  padding: 1rem;
}
</style>