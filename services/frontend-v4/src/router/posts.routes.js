import { Layout, AddEditPost, ListPosts } from '@/views/posts';

export default {
    path: '/channels',
    component: Layout,
    children: [
        { path: ':channel_id', component: ListPosts },
        { path: ':channel_id/add', component: AddEditPost },
        { path: ':channel_id/:post_id', component: AddEditPost },
    ]
};
