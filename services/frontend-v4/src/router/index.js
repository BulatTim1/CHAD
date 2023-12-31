import { createRouter, createWebHistory } from 'vue-router';

import { useAuthStore, useAlertStore } from '../stores';
import { Home } from '../views';
import accountRoutes from './account.routes';
import adminRoutes from './admin.routes';
import channelsRoutes from './channels.routes';
import postsRoutes from './posts.routes';

export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    linkActiveClass: 'active',
    routes: [
        { path: '/', component: Home },
        { ...accountRoutes },
        { ...adminRoutes },
        { ...channelsRoutes },
        { ...postsRoutes },
        // catch all redirect to home page
        { path: '/:pathMatch(.*)*', redirect: '/' }
    ]
});

router.beforeEach(async (to) => {
    // clear alert on route change
    const alertStore = useAlertStore();
    alertStore.clear();

    // redirect to login page if not logged in and trying to access a restricted page 
    const publicPages = ['/'];
    // const adminPages = ;
    const authRequired = !publicPages.includes(to.path);
    const adminRequired = /\/admin?.+/.test(to.path);
    const authStore = useAuthStore();
    if (authRequired && !authStore.user || adminRequired && authStore.isAdmin !== true) {
        authStore.returnUrl = to.fullPath;
        return '/';
    }
});
