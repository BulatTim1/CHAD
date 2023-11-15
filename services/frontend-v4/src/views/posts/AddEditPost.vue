<script setup>
import { ref, watch, onMounted, computed, nextTick } from 'vue'
import { Form, Field } from 'vee-validate';
import * as Yup from 'yup';
import { useRoute } from 'vue-router';
import { storeToRefs } from 'pinia';

import { usePostsStore, useAlertStore } from '@/stores';
import sanitizeHtml from 'sanitize-html';

const postsStore = usePostsStore();
const alertStore = useAlertStore();
const route = useRoute();
const channelId = route.params.channel_id;
const postId = route.params.post_id;
const d = new Date(); 
d.setSeconds(0,0);

const { post, loading } = storeToRefs(postsStore);

let title = 'Добавить пост';
let editing = false;
let newMedia = ref([]);

let allMedia = computed(() => {
  return [...newMedia.value];
});

const convertToUnix = (x) => {
    return Date.parse(x)/1000
};

if (postId) {
    // edit mode
    title = 'Редактировать пост';
    editing = true;
    postsStore.getById(channelId, postId);
    watch(loading, (n, o) => {
        if (!n) {
            newMedia.value = [...newMedia.value, ...post.value.media];
            post.value.date = new Date(post.value.send_time * 1000);
        }
    })
    // if (!loading && post === null) {
    //     await router.push(`/channels/${channelId}`);
    // }
} else {
    post.value = {'text': '', 'send_time': convertToUnix(d), 'date': d, 'media': []};
}

const dateValue = computed(() => {
    console.log(post.value.date.toISOString());
    return post.value.date.toISOString().substring(0, 19);
});

const schema = Yup.object().shape({
    text: Yup.string().trim().transform((value, originalValue) => { return sanitizeHtml(value) })
        .required('Введите текст'),
    date: Yup.date().required('Введите время отправления')
});

async function uploadFiles(file) {
  const reader = new FileReader();
  reader.addEventListener('load', async () => {
    newMedia.value = [...newMedia.value, {"file": reader.result, "type": "photo"}];
    await nextTick();
  });
  reader.readAsDataURL(file);
}

function onFileChanged($event) {
    const files = $event.target.files;
    if (!files) return;
    // newMedia.value = [];
    [...files].forEach( uploadFiles );
    console.log(newMedia.value);
}

async function onSubmit(values) {
    try {
        let message;
        console.log(values);
        values.send_time = convertToUnix(values.date);
        delete values.date;
        delete values.files;
        console.log(values);
        if (newMedia.value.length > 0) {
            values.media = newMedia.value;
        }
        if (postId) {
            await postsStore.update(channelId, post.value.id, values)
            message = 'Пост обновлен';
        } else {
            await postsStore.register(channelId, values);
            message = 'Пост добавлен';
        }
        alertStore.success(message);
    } catch (error) {
        alertStore.error(error);
    }
}

function deleteImage($event) {
    const image = $event.target.src;
    newMedia.value = newMedia.value.filter(m => m.file !== image);
}
</script>

<template>
    <h1>{{title}}</h1>
    <template v-if="!loading">
        <Form @submit="onSubmit" :validation-schema="schema" :initial-values="post" v-slot="{ errors, isSubmitting }">
            <div class="form-row">
                <div class="form-group col">
                    <label>Текст поста</label>
                    <Field name="text" type="textarea" class="form-control" :class="{ 'is-invalid': errors.text }"/>
                    <div class="invalid-feedback">{{ errors.text }}</div>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group col">
                    <label>Дата и время отправки</label>
                    <Field name="date" step="1" type="datetime-local" class="form-control" :class="{ 'is-invalid': errors.date }" :value="dateValue"/>
                    <div class="invalid-feedback">{{ errors.date }}</div>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group col">
                    <label>Медиа</label>
                    <h4>Нажмите на картинку, чтобы удалить</h4>
                    <div id="preview" class="row mb-2">
                    <!-- show already uploaded media and new media -->
                        <div @click="deleteImage($event, m)"  v-for="m in allMedia" :key="m.file" class="col-sm-3 mb-2">
                            <img :src="m.file" class="img-thumbnail" style="width: 300px; height: 300px; object-fit: cover;"/>
                        </div>
                    </div>
                    <Field name="files" type="file" @change="onFileChanged($event)" accept="image/jpg, image/jpeg, image/png" capture class="form-control" :class="{ 'is-invalid': errors.files }" multiple/>
                    <div class="invalid-feedback">{{ errors.media }}</div>
                </div>
            </div>
            <div class="form-group d-flex mt-5">
                <button class="btn btn-primary" :disabled="isSubmitting">
                    <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
                    Добавить
                </button>
                <router-link :to="`/channels/${channelId}`" class="btn btn-link">Отменить</router-link>
                <button @click="postsStore.delete(channelId, post.id)" class="ms-auto d-inline-block btn btn-sm btn-danger">
                    <span>Удалить</span>
                </button>
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