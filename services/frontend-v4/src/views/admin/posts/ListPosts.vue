<script setup>
import { storeToRefs } from 'pinia';

import { useRoute } from 'vue-router';
import { usePostsStore } from '@/stores';

const postsStore = usePostsStore();
const { posts, loading } = storeToRefs(postsStore);
postsStore.getAll();
</script>

<template>
    <h1>Посты</h1>
    <div class="mb-2">
        <router-link to="/admin" class="me-2 btn btn-primary d-inline-flex align-items-center justify-content-center align-self-center">
            <i class="bi bi-arrow-left"></i>Назад
        </router-link>
    </div> 
    <table class="table table-striped">
        <thead>
            <tr>
                <th style="width: 10%">ID</th>
                <th style="width: 40%">Текст</th>
                <th style="width: 20%">Дата отправки</th>
                <th style="width: 30%"></th>
            </tr>
        </thead>
        <tbody>
            <template v-if="!loading">
                <tr v-for="post in posts">
                    <td>{{ post.id }}</td>
                    <td><div class="d-block text-break h-100">{{ post.text }}</div></td>
                    <td>{{ new Date(post.send_time * 1000).toLocaleString() }}</td>
                    <td class="d-flex h-100 flex-column text-wrap">
                        <router-link :to="`/channels/${post.channel}/${post.id}`" class="btn btn-sm btn-primary mr-1">Редактировать пост</router-link>
                        <button @click="postsStore.delete(post.channel, post.id)" class="d-inline-block btn btn-sm btn-danger" v-if="post.isDeleting">
                            <span>Удалить</span>
                        </button>
                    </td>
                </tr>
            </template>
            <tr v-if="loading">
                <td colspan="4" class="text-center">
                    <span class="spinner-border spinner-border-lg align-center"></span>
                </td>
            </tr>       
        </tbody>
    </table>
</template>
