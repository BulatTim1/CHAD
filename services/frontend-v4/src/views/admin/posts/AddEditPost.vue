<script setup>
import { Form, Field } from 'vee-validate';
import * as Yup from 'yup';
import { useRoute } from 'vue-router';
import { storeToRefs } from 'pinia';

import { usePostsStore, useAlertStore } from '@/stores';
import { router } from '@/router';

const postsStore = usePostsStore();
const alertStore = useAlertStore();
const route = useRoute();
const channelId = route.params.channel_id;
const postId = route.params.post_id;


let title = 'Добавить пост';
let post = null;
if (postId) {
    // edit mode
    title = 'Редактировать пост';
    ({ post } = storeToRefs(postsStore));
    postsStore.getById(channelId, postId);
    // if (post === null) {
    //     await router.push(`/channels/${channelId}`);
    // }
}

const convertToUnix = (x) => {
    return Date.parse(x)/1000
};

const schema = Yup.object().shape({
    text: Yup.string()
        .required('Введите текст'),
    send_time: Yup.date().default(() => new Date())
        .required('Введите время отправления')
        
});

async function onSubmit(values) {
    try {
        let message;
        values.send_time = convertToUnix(values.send_time);
        console.log(values);
        if (post) {
            await postsStore.update(post.value.id, values)
            message = 'Пост обновлен';
        } else {
            await postsStore.register(channelId, values);
            message = 'Пост добавлен';
        }
        await router.go(-1)
        alertStore.success(message);
    } catch (error) {
        alertStore.error(error);
    }
}
</script>

<template>
    <h1>{{title}}</h1>
    <template v-if="!(post?.loading || post?.error)">
        <Form @submit="onSubmit" :validation-schema="schema" :initial-values="post" v-slot="{ errors, isSubmitting }">
            <div class="form-row">
                <div class="form-group col">
                    <label>Текст поста</label>
                    <Field name="text" type="textarea" class="form-control" :class="{ 'is-invalid': errors.text }" />
                    <div class="invalid-feedback">{{ errors.text }}</div>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group col">
                    <label>Дата и время отправки</label>
                    <Field name="send_time" type="datetime-local" class="form-control" :class="{ 'is-invalid': errors.send_time }" />
                    <div class="invalid-feedback">{{ errors.send_time }}</div>
                </div>
            </div>
            <div class="form-group">
                <button class="btn btn-primary" :disabled="isSubmitting">
                    <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
                    Добавить
                </button>
                <router-link :to="`/channels/${channelId}`" class="btn btn-link">Отменить</router-link>
            </div>
        </Form>
    </template>
    <template v-if="post?.loading">
        <div class="text-center m-5">
            <span class="spinner-border spinner-border-lg align-center"></span>
        </div>
    </template>
    <template v-if="post?.error">
        <div class="text-center m-5">
            <div class="text-danger">Error loading post: {{post.error}}</div>
        </div>
    </template>
</template>