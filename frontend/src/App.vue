<template>
  <RouterView />
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useUserStore } from './stores/userStore'

const user = useUserStore()

onMounted(() => {
  user.initializeAuth()
})
</script>
