<script setup>
import { storeToRefs } from 'pinia';

import { useUsersStore } from '@/stores';
import { RouterLink } from 'vue-router';

const usersStore = useUsersStore();
const { users } = storeToRefs(usersStore);

usersStore.getAll();
</script>

<template>
    <h1>Пользователи</h1>
    <router-link to="/admin" class="btn btn-primary d-inline-flex align-items-center justify-content-center align-self-center">
        <i class="bi bi-arrow-left"></i><span>Назад</span>
    </router-link>
    <table class="table table-striped">
        <thead>
            <tr>
                <th style="width: 30%">ID</th>
                <th style="width: 40%">Имя пользователя</th>
                <th style="width: 30%">Ник пользователя</th>
                <!-- <th style="width: 10%"></th> -->
            </tr>
        </thead>
        <tbody>
            <template v-if="users.length">
                <tr v-for="user in users" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.first_name }}</td>
                    <td>{{ user.username }}</td>
                    <!-- <td style="white-space: nowrap">
                        <router-link :to="`/admin/users/edit/${user.id}`" class="btn btn-sm btn-primary mr-1">Edit</router-link>
                        <button @click="usersStore.delete(user.id)" class="btn btn-sm btn-danger btn-delete-user" :disabled="user.isDeleting">
                            <span v-if="user.isDeleting" class="spinner-border spinner-border-sm"></span>
                            <span v-else>Delete</span>
                        </button>
                    </td> -->
                </tr>
            </template>
            <tr v-if="users.loading">
                <td colspan="4" class="text-center">
                    <span class="spinner-border spinner-border-lg align-center"></span>
                </td>
            </tr>
            <tr v-if="users.error">
                <td colspan="4">
                    <div class="text-danger">Error loading users: {{users.error}}</div>
                </td>
            </tr>            
        </tbody>
    </table>
</template>
