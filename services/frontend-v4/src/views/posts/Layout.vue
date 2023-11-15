<script setup>
import { useAuthStore } from '@/stores';
import { router } from '@/router';

// redirect home if already logged in
const authStore = useAuthStore();
if (!authStore.user) {
    router.push('/');
}
</script>

<template>
    <section id="hero" class="hero d-flex align-items-center">
    <div class="container">
        <router-view class="d-flex flex-column justify-content-center" />
    </div>
    </section>
</template>

<style scoped>
#hero{
    height: auto!important;
    min-height: 100vh;
    padding-top: 20vh;
}
</style>
