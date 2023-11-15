import { Layout } from '../views/account';

export default {
    path: '/account',
    component: Layout,
    children: [
        { path: '', redirect: 'home' },
    ]
};
