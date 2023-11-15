import { defineStore } from 'pinia';

import { fetchWrapper } from '../helpers';
import { useAuthStore } from './auth.store';
import { useAlertStore } from './alert.store';
import { router } from '@/router';
import sanitizeHtml from 'sanitize-html';

import dateFormat from "dateformat";

const baseUrl = `${import.meta.env.VITE_API_URL}`;

export const usePostsStore = defineStore({
    id: 'posts',
    state: () => ({
        posts: [],
        post: {},
        loading: false
    }),
    actions: {
        async register(channel_id, post) {
            const token = useAuthStore().token;
            await fetchWrapper.post(`${baseUrl}/channels/${channel_id}/`, token, post);
            router.push(`/channels/${channel_id}`);
        },
        async getAll() {
            const token = useAuthStore().token;
            this.loading = true;
            try {
                const posts = await fetchWrapper.get(`${baseUrl}/admin/posts`, token);    
                if (posts === null)
                {
                    throw new Error("Ошибка");
                }
                for (const post in posts) {
                    // post.date = new Date(post.send_time*1000).toISOString().replace('Z', '');
                    // post.send_time = new Date(post.send_time * 1000);
                }
                this.posts = posts;
                this.loading = false;
            } catch (error) {
                const alertStore = useAlertStore();
                alertStore.error(error);
            }
        },
        async getAllByChannel(channel_id) {
            const token = useAuthStore().token;
            this.loading = true;
            try {
                const posts = await fetchWrapper.get(`${baseUrl}/channels/${channel_id}`, token);
                if (posts === null)
                {
                    throw new Error("Ошибка");
                }
                for (const post in posts) {
                    // post.date = new Date(post.send_time*1000).toISOString().replace('Z', '');
                    // post.value.send_time = new Date(post.send_time * 1000);
                }
                this.posts = posts;
                this.loading = false;
            } catch (error) {
                const alertStore = useAlertStore();
                alertStore.error(error);
            }
        },
        async getAllByChannelQalendar(channel_id) {
            const token = useAuthStore().token;
            this.loading = true;
            try {
                const posts = await fetchWrapper.get(`${baseUrl}/channels/${channel_id}`, token);
                if (posts === null)
                {
                    throw new Error("Ошибка");
                }
                const qposts = [];
                //   {
                //     title: "Ralph on holiday",
                //     with: "Rachel Greene",
                //     time: { start: "2023-11-13", end: "2023-11-14" },
                //     color: "green",
                //     isEditable: true,
                //     id: "5602b6f589fc"
                //   }
                posts.forEach(post => {
                    const date = new Date(post.send_time*1000);
                    const strDate = dateFormat(date, 'yyyy-mm-dd HH:MM');
                    // const date2 = new Date((post.send_time + 60 * 5)*1000);
                    // const strDate2 = dateFormat(date2, 'yyyy-mm-dd HH:MM');
                    const title = (post.text.length > 12) ? post.text.slice(0, 10) + '..' : post.text;
                    qposts.push(
                        {
                            id: post.id, 
                            title:  sanitizeHtml(title), 
                            time: { start: strDate, end: strDate},
                            description: sanitizeHtml(post.text) + "<br><a class=\"btn btn-primary\" href=\"" + channel_id + "/" + post.id + "\">Изменить</a>",
                            isEditable: false,
                            color: (post.media.length > 0) ? "yellow" : "blue",
                        });
                });
                console.log(qposts);
                this.posts = qposts;
                this.loading = false;
            } catch (error) {
                const alertStore = useAlertStore();
                alertStore.error(error);
            }
        },
        async getById(channel_id, id) {
            const token = useAuthStore().token;
            this.loading = true;
            try {
                const post = await fetchWrapper.get(`${baseUrl}/channels/${channel_id}/${id}`, token);
                if (post === null) {
                    throw new Error("Такого поста не сущесвует");
                }
                // post.send_time = new Date(post.send_time * 1000);
                // post.date = new Date(post.send_time*1000).toISOString().replace('Z', '');
                this.post = post;
                this.loading = false;
            } catch (error) {
                const alertStore = useAlertStore();
                alertStore.error(error);
            }
        },
        async update(channel_id, id, params) {
            const token = useAuthStore().token;
            await fetchWrapper.post(`${baseUrl}/channels/${channel_id}/${id}`, token, params);
            router.push(`/channels/${channel_id}`);
        },
        async delete(channel_id,id) {
            const token = useAuthStore().token;
            await fetchWrapper.delete(`${baseUrl}/channels/${channel_id}/${id}`, token);
            router.push('/channels/' + channel_id);
        }
    }
});
