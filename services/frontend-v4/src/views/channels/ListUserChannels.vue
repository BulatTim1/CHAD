<script setup>
import { storeToRefs } from 'pinia';

import { useChannelsStore } from '@/stores';

const channelsStore = useChannelsStore();
const { channels } = storeToRefs(channelsStore);

channelsStore.getAllByUser();
</script>

<template>
    <h1>Каналы</h1>
    <!-- <router-link to="/channels/add" class="btn btn-sm btn-success mb-2">Добавить канал</router-link> -->
    <div class="form-group alert alert-primary">Вам необходимо добавить бота <a href="https://t.me/chad_panel_bot" target="_blank">@chad_panel_bot</a> в канал с правами адмиинистратора. Это можно сделать, нажав на кнопку снизу, или начав диалог с ботом в Telegram.</div>
    <!-- <div class="form-group alert alert-warning">Важно: такой способ добавления работает только в течении суток! Если вы забыли добавить бота, то необходимо удалить его из канала и добавить заново.</div> -->
    <div class="form-group">
        <a class="btn btn-secondary me-1" href="https://t.me/chad_panel_bot?startchannel&admin=post_messages+edit_messages" target="_blank" >Добавить бота в канал</a>
    </div>
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
                    <!-- <div class="text-danger">Error loading users: {{users.error}}</div> -->
                </td>
            </tr>            
        </tbody>
    </table>
</template>
