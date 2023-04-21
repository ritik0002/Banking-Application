
<script setup>
import Home from './components/home.vue';
import Navbar from './components/navbar.vue';

import {RouterView} from 'vue-router';
import Footer from './components/footer.vue';
</script>

<template>
  <Navbar />
  

  <RouterView></RouterView>
  
  <Footer />

</template>


<style>

</style>