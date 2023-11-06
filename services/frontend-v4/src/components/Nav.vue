<script setup>
import { useAuthStore } from '../stores';
import { telegramLoginTemp } from 'vue3-telegram-login'
import { ref } from 'vue'

const isLoaded = ref(false)

function telegramLoadedCallbackFunc () {
  console.log('script is loaded')
  isLoaded.value = true
}

async function yourCallbackFunction (user) {
    console.log(user)
    const authStore = useAuthStore();
    await authStore.telegramLogin(user);
}
const authStore = useAuthStore();
</script>

<template>
    <nav v-show="authStore.user" class="navbar navbar-expand navbar-dark bg-dark">
        <div class="navbar-nav w-100 align-items-center">
            <router-link to="/" class="nav-item nav-link">Home</router-link>
            <router-link to="/users" class="nav-item nav-link">Users</router-link>
            <button @click="authStore.logout()" class="btn btn-link nav-item nav-link">Logout</button>
    <telegram-login-temp class="ml-auto d-flex"
        mode="callback"
        telegram-login="chad_panel_bot"
        @loaded='telegramLoadedCallbackFunc'
        @callback="yourCallbackFunction"
    />
        </div>
    </nav>
</template>