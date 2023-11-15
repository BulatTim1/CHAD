<script setup>
import { storeToRefs } from 'pinia';

import { useRoute } from 'vue-router';
import { usePostsStore } from '@/stores';
import { Qalendar } from "qalendar";


const postsStore = usePostsStore();
const { posts, loading } = storeToRefs(postsStore);

const route = useRoute();
const channelId = route.params.channel_id;
postsStore.getAllByChannelQalendar(channelId);
</script>

<template>
    <h1>Посты</h1>
    <div class="mb-2">
        <router-link to="/channels/" class="me-2 btn btn-primary d-inline-flex align-items-center justify-content-center align-self-center">
            <i class="bi bi-arrow-left"></i>Назад
        </router-link>
        <router-link :to="`/channels/${channelId}/add`" class="btn btn-success d-inline-flex align-items-center justify-content-center align-self-center">Добавить пост</router-link>
    </div> 
    <Qalendar 
        :is-loading="loading"
        :events="posts">
    </Qalendar>
</template>

<style>
    @import "qalendar/dist/style.css";
    .is-event {
        height: auto!important;
    }
    .mode-is-week, .mode-is-day {
        height: fit-content!important;
    }
    .is-description {
        display: none;
    }
</style>