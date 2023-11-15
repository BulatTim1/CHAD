<script setup>
import { useAuthStore } from '../stores';
import { telegramLoginTemp } from 'vue3-telegram-login'
import { ref } from 'vue'

const isLoaded = ref(false)

function telegramLoadedCallbackFunc () {
  console.log('script is loaded')
  isLoaded.value = true
}

async function onTelegramAuth (user) {
    const authStore = useAuthStore();
    await authStore.telegramLogin(user);
}
const authStore = useAuthStore();
//:userpic="`${true}`"


const mobileClick = (e) => {
        document.querySelector('#navbar').classList.toggle('navbar-mobile')
        this.classList.toggle('bi-list')
        this.classList.toggle('bi-x')
};

</script>


<template>
    <header id="header" class="header fixed-top">
    <div class="container-fluid container-xl d-flex align-items-center justify-content-between">
        <router-link to="/" class="logo d-flex align-items-center"><span>CHAD</span></router-link>
        
    <nav  v-if="authStore.user" id="navbar" class="navbar">
        <ul>
          <li><router-link to="/" class="nav-link scrollto">Главная</router-link></li>
          <li v-if="authStore.isAdmin"><router-link to="/admin" class="nav-item nav-link">Админ. панель</router-link></li>
          <li><router-link to="/channels" class="nav-item nav-link">Каналы</router-link></li>
          <li><a class="btn btn-link nav-item nav-link" @click="authStore.logout()">Выйти</a></li>
        </ul>
        <i @click="mobileClick" class="bi bi-list mobile-nav-toggle"></i>
    </nav>
    <nav v-else class="navbar" id="navbar">
        <ul>
          <li><a class="nav-link scrollto active" href="/">Главная</a></li>
          <li><telegram-login-temp class="nav-link scrollto ms-4"
                    mode="callback"
                    telegram-login="chad_panel_bot"
                    request-access="write"
                    @loaded='telegramLoadedCallbackFunc'
                    @callback="onTelegramAuth"
                /></li>
        </ul>
        <i @click="mobileClick" class="bi bi-list mobile-nav-toggle"></i>
    </nav>
    </div>
  </header>
</template>