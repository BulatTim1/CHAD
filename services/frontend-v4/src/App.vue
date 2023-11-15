<script setup>
import { Nav, Alert } from './components';
import { useAuthStore } from './stores';

const authStore = useAuthStore();
</script>

<template>
    <!-- <div class="app-container" :class="authStore.user && 'bg-light'"> -->
        <Nav />
        <Alert class="container"/>
        <!-- <div class="container pt-4 pb-4 home main"> -->
            <router-view />
        <!-- </div> -->
    <!-- </div> -->
</template>

<style>
@import '@/assets/css/base.css';
</style>

