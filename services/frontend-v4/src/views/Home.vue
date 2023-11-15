<script setup>
import { storeToRefs } from 'pinia';

import { useAuthStore } from '../stores';

const authStore = useAuthStore();
const { user, isAdmin } = storeToRefs(authStore);
</script>

<template>
    <section v-if="user" id="hero" class="hero d-flex align-items-center">
        <div class="container">
        <div class="row">
            <div class="col-lg-6 d-flex flex-column justify-content-center">
            <h1 data-aos="fade-up">CHannel ADministrator</h1>
            <h2 data-aos="fade-up" data-aos-delay="400">Добро пожаловать, {{user.first_name}}!</h2>
            <div data-aos="fade-up" data-aos-delay="600">
                <div class="text-center text-lg-start" v-if="isAdmin">
                    <router-link to="/admin" class="btn-get-started scrollto d-inline-flex align-items-center justify-content-center align-self-center">
                        <span>В панель администратора</span>
                        <i class="bi bi-arrow-right"></i>
                    </router-link>
                </div>
                <div class="text-center text-lg-start" v-else>
                    <router-link to="/channels" class="btn-get-started scrollto d-inline-flex align-items-center justify-content-center align-self-center">
                        <span>В панель</span>
                        <i class="bi bi-arrow-right"></i>
                    </router-link>
                </div>
            </div>
            </div>
            <div class="col-lg-6 hero-img" data-aos="zoom-out" data-aos-delay="200">
            <img src="/assets/pic/dd4dafb78ab402593462a5b8dfddcbff.svg" class="img-fluid" alt="">
            </div>
        </div>
        </div>
        
    <!-- <div class="container" >
        <div class="user-info">
            <img v-if="user.photo_url" :src="`${user.photo_url}`" class="user-photo" />
            <h1>Добро пожаловать, {{user.first_name}}!</h1>
            <p>Вы можете добавлять каналы Telegram и отправлять сообщения в определенное время.</p>
            <p>В будущем мы добавим предложения для каждого канала, функции розыгрышей и интеграцию рекламы.</p>
        </div>
        <div v-if="isAdmin" class="admin-panel">
            <p><router-link to="/admin">Панель администратора</router-link></p>
        </div>
    </div> -->

    </section>
    <section v-else id="hero" class="hero d-flex align-items-center">
        <div class="container">
        <div class="row">
            <div class="col-lg-6 d-flex flex-column justify-content-center">
            <h1 data-aos="fade-up">CHannel ADministrator</h1>
            <h2 data-aos="fade-up" data-aos-delay="400">Система управления Telegram-каналом</h2>
            <div data-aos="fade-up" data-aos-delay="600">
                <div class="text-center text-lg-start">
                <a href="#values" class="btn-get-started scrollto d-inline-flex align-items-center justify-content-center align-self-center">
                    <span>Наши преимущества</span>
                    <i class="bi bi-arrow-right"></i>
                </a>
                </div>
            </div>
            </div>
            <div class="col-lg-6 hero-img" data-aos="zoom-out" data-aos-delay="200">
            <img src="/assets/pic/dd4dafb78ab402593462a5b8dfddcbff.svg" class="img-fluid" alt="">
            </div>
        </div>
        </div>
    </section>

    <section id="values" class="values">
        <div class="container" data-aos="fade-up">

            <header class="section-header">
                <h2>О проекте</h2>
                <h4 class="mt-4">Интуитивно понятный сервис для управления контентом в Telegram. Без лишних
        формальностей: войдите через Телеграм, добавьте каналы, планируйте посты с креативными картинками и
        проводите розыгрыши. Уникальные "предложки" для каналов придают индивидуальный стиль, делая контент
        максимально привлекательным.</h4>
            </header>
        </div>
    </section>

    <section id="values" class="values">
        <div class="container" data-aos="fade-up">

        <header class="section-header">
            <h2>Наши преимущества</h2>
            <p>Выберите нас из-за наших преимуществ</p>
        </header>

        <div class="row">

            <div class="col-lg-4" data-aos="fade-up" data-aos-delay="200">
            <div class="box">
                <img src="/assets/pic/creative_workspace_illustration.png" class="img-fluid" alt="">
                <h3>Гибкая авторизация через Telegram</h3>
                <p>Входите через Telegram в уже настроенную к работе с момента запуска платформу, обеспечивая высокий
    контроль и гибкие настройки безопасности.</p>
            </div>
            </div>

            <div class="col-lg-4 mt-4 mt-lg-0" data-aos="fade-up" data-aos-delay="400">
            <div class="box">
                <img src="/assets/pic/a36c73c3295a1cbe5d29d68958b54a78.svg" class="img-fluid" alt="">
                <h3>Интерактивные розыгрыши</h3>
                <p>Проводите розыгрыши с интерактивными элементами для привлечения аудитории, предлагая разнообразные призы
    и создавая интересные условия участия.</p>
            </div>
            </div>

            <div class="col-lg-4 mt-4 mt-lg-0" data-aos="fade-up" data-aos-delay="600">
            <div class="box">
                <img src="/assets/pic/3c27cea4d25780ab07f4c768382b526d.svg" class="img-fluid" alt="">
                <h3>Эффективный контент-менеджмент каналов</h3>
                <p>Пользователи могут легко управлять контентом, добавлять каналы и создавать отложенные посты с
        изображениями, что особенно полезно для администраторов каналов с большим трафиком.</p>
            </div>
            </div>
        </div>
        </div>
    </section>
        <!-- <p class="lead">Создавать каналы, заполнять их отложенными постами с картинками. Розыгрыши, индивидуальные предложки для
          каналов. Удобный интерфейс - просто войди! 🚀</p> -->


</template>

