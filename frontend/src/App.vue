<template>
  <RouterView />
</template>

<script setup>
<<<<<<< HEAD
import { RouterView } from 'vue-router'
||||||| 7e20b35
import Header from './components/layout/Header.vue'
import Footer from './components/layout/Footer.vue'
=======
import { onMounted } from 'vue'
import Header from './components/layout/Header.vue'
import Footer from './components/layout/Footer.vue'
import { useUserStore } from './stores/userStore'

const user = useUserStore()

onMounted(() => {
  user.initializeAuth()
})
>>>>>>> develop
</script>
