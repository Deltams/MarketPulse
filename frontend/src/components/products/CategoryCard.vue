<template>
  <v-card
    class="category-card h-100"
    elevation="2"
    hover
    :to="`/category/${category.id}`"
    style="background: #fff !important;"
  >
    <v-img
      :src="category.image"
      height="200"
      cover
      class="align-end"
    />
    <v-card-text>
      <div class="category-title">
        {{ category.name }}
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
const props = defineProps({
  category: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.category-card {
  background: #fff !important;
  box-shadow: 0 4px 16px rgba(0,0,0,0.10), 0 1.5px 4px rgba(0,0,0,0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s;
  border-radius: 16px;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
  max-width: 320px;
  margin: 0 auto;
  will-change: transform;
  border: 2px solid transparent;
  background-color: #fff;
}
.category-card:hover {
  transform: translateY(-4px) scale(1.01);
  box-shadow: 0 8px 32px rgba(25, 118, 210, 0.25), 0 3px 8px rgba(0,0,0,0.10);
  border-color: #1976d2;
}
.category-card .v-img {
  height: 200px !important;
  width: 100% !important;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
}
.category-title {
  color: #222;
  font-size: 1.2rem;
  font-weight: 600;
  text-align: center;
  margin-top: 12px;
  margin-bottom: 0;
  line-height: 1.3;
  word-break: break-word;
  border-radius: 0;
  box-shadow: none;
  padding: 8px 0;
  background: none;
}
</style> 