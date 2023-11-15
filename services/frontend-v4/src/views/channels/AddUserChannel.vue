<script setup>
import { Form, Field } from 'vee-validate';
import * as Yup from 'yup';
import { useRoute } from 'vue-router';
import { storeToRefs } from 'pinia';

import { useChannelsStore, useAlertStore } from '@/stores';
import { router } from '@/router';

const channelsStore = useChannelsStore();
const alertStore = useAlertStore();

let title = 'Добавить канал';
let channel = null;

async function onSubmit() {
    try {
        let message;
        channel = await channelsStore.register();
        message = 'Канал добавлен';
        await router.push('/channels');
        alertStore.success(message);
    } catch (error) {
        if (error===402){
            error = "Повторите попытку.";
        }
        alertStore.error(error);
    }
}
</script>

<template>
    <h1>{{title}}</h1>
    <template v-if="!(channel?.loading || channel?.error)">
        <Form @submit="onSubmit" :initial-values="channel" v-slot="{ errors, isSubmitting }">
            <div class="form-group alert alert-primary">Вам необходимо добавить бота в канал, а затем нажать на кнопку добавить.</div>
            <div class="form-group alert alert-warning">Важно: такой способ добавления работает только в течении суток! Если вы забыли добавить бота, то необходимо удалить его из канала и добавить заново.</div>
            <div class="form-group">
                <a class="btn btn-secondary me-1" href="https://t.me/chad_panel_bot?startchannel&admin=post_messages+edit_messages" target="_blank" >Добавить бота в канал</a>
                <button class="btn btn-primary" :disabled="isSubmitting">
                    <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
                    Сохранить
                </button>
                <router-link to="/channels" class="btn btn-link">Назад</router-link>
            </div>
        </Form>
    </template>
    <template v-if="channel?.loading">
        <div class="text-center m-5">
            <span class="spinner-border spinner-border-lg align-center"></span>
        </div>
    </template>
    <template v-if="channel?.error">
        <div class="text-center m-5">
            <div class="text-danger">Ошибка добавления канала: {{channel.error}}</div>
        </div>
    </template>
</template>
