<script setup>
import { storeToRefs } from 'pinia';

import { useChannelsStore } from '@/stores';

const channelsStore = useChannelsStore();
const { channels } = storeToRefs(channelsStore);

channelsStore.getAll();
</script>

<template>
    <h1>Каналы</h1>
    <!-- <router-link to="/channels/add" class="btn btn-sm btn-success mb-2">Добавить канал</router-link> -->
    <router-link to="/admin" class="btn btn-primary d-inline-flex align-items-center justify-content-center align-self-center">
        <i class="bi bi-arrow-left"></i><span>Назад</span>
    </router-link>
    <table class="table table-striped">
        <thead>
            <tr>
                <th style="width: 30%">ID</th>
                <th style="width: 40%">Название канала</th>
                <th style="width: 10%">Бот в канале?</th>
                <th style="width: 20%"></th>
            </tr>
        </thead>
        <tbody>
            <template v-if="channels.length">
                <tr v-for="channel in channels" :key="channel.id">
                    <td>{{ channel.id }}</td>
                    <td>{{ channel.title }}</td>
                    <td>{{ (channel.joined) ? "Да" : "Нет" }}</td>
                    <td style="white-space: nowrap">
                        <router-link :to="`/channels/${channel.id}`" class="btn btn-sm btn-primary mr-1">Посмотреть посты</router-link>
                        <!--<button @click="channelsStore.delete(channel.id)" class="btn btn-sm btn-danger btn-delete-user" :disabled="user.isDeleting">
                            <span v-if="channel.isDeleting" class="spinner-border spinner-border-sm"></span>
                            <span v-else>Delete</span>
                        </button> -->
                    </td>
                </tr>
            </template>
            <tr v-if="channels.loading">
                <td colspan="4" class="text-center">
                    <span class="spinner-border spinner-border-lg align-center"></span>
                </td>
            </tr>
            <tr v-if="channels.error">
                <td colspan="4">
                    <div class="text-danger">Error loading users: {{users.error}}</div>
                </td>
            </tr>            
        </tbody>
    </table>
</template>
