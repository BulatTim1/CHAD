import { Layout, ListUserChannels, AddUserChannel } from '@/views/channels';

export default {
    path: '/channels',
    component: Layout,
    children: [
        { path: '', component: ListUserChannels },
        { path: 'add', component: AddUserChannel },
    ]
};
