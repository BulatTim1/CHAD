import { defineStore } from 'pinia';

import { fetchWrapper } from '../helpers';
import { useAuthStore } from './auth.store';

const baseUrl = `${import.meta.env.VITE_API_URL}`;

export const useChannelsStore = defineStore({
    id: 'channels',
    state: () => ({
        channels: {},
        channel: {}
    }),
    actions: {
        async register() {
            // const authStore = useAuthStore();
            const token = useAuthStore().token;
            await fetchWrapper.get(`${baseUrl}/channels/add`, token);
        },
        async getAll() {
            // const authStore = useAuthStore();
            const token = useAuthStore().token;
            this.channels = { loading: true };
            try {
                this.channels = await fetchWrapper.get(`${baseUrl}/admin/channels`, token);    
                if (this.channels === null)
                {
                    
                }
            } catch (error) {
                this.channels = { error };
            }
        },
        async getAllByUser() {
            // const authStore = useAuthStore();
            const token = useAuthStore().token;
            this.channels = { loading: true };
            try {
                this.channels = await fetchWrapper.get(`${baseUrl}/channels`, token);    
                if (this.channels === null)
                {
                    
                }
            } catch (error) {
                this.channels = { error };
            }
        },
        async getById(id) {
            // const authStore = useAuthStore();
            const token = useAuthStore().token;
            this.channel = { loading: true };
            try {
                this.channel = await fetchWrapper.get(`${baseUrl}/${id}`, token);
            } catch (error) {
                this.channel = { error };
            }
        },
        // async update(id, params) {
        //     await fetchWrapper.put(`${baseUrl}/${id}`, params);

        //     // update stored user if the logged in user updated their own record
        //     const authStore = useAuthStore();
        //     if (id === authStore.user.id) {
        //         // update local storage
        //         const user = { ...authStore.user, ...params };
        //         localStorage.setItem('user', JSON.stringify(user));

        //         // update auth user in pinia state
        //         authStore.user = user;
        //     }
        // },
        // async delete(id) {
        //     // add isDeleting prop to user being deleted
        //     this.channels.find(x => x.id === id).isDeleting = true;

        //     await fetchWrapper.delete(`${baseUrl}/${id}`);

        //     // remove user from list after deleted
        //     this.channels = this.channels.filter(x => x.id !== id);

        //     // auto logout if the logged in user deleted their own record
        //     const authStore = useAuthStore();
        //     if (id === authStore.user.id) {
        //         authStore.logout();
        //     }
        // }
    }
});
