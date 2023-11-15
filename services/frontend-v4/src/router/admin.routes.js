import { Layout, ListUsers, ListChannels, ListPosts, Panel } from '@/views/admin';

export default {
    path: '/admin',
    component: Layout,
    children: [
        { path: '', component: Panel },
        { path: 'users', component: ListUsers },
        { path: 'channels', component: ListChannels },
        { path: 'posts', component: ListPosts }
    ]
};
