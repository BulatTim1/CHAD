import { defineStore } from 'pinia';
import { Buffer } from 'buffer';

import { fetchWrapper } from '../helpers';
import { router } from '../router';
import { useAlertStore } from './alert.store';


const baseUrl = import.meta.env.VITE_API_URL;

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        // initialize state from local storage to enable user to stay logged in
        user: JSON.parse(localStorage.getItem('user')),
        isAdmin: (localStorage.getItem('isAdmin') === 'true'),
        token: localStorage.getItem('token'),
        returnUrl: null
    }),
    actions: {
        async telegramLogin(user) {
            try {
                const token = Buffer.from(JSON.stringify(user)).toString("base64");
                const authed = await fetchWrapper.get(`${baseUrl}/admin`, token);    
                if (authed === true){
                    // update pinia state
                    this.user = user;
                    this.token = token;
                    this.isAdmin = authed;
                    localStorage.setItem('isAdmin', authed);
                    localStorage.setItem('user', JSON.stringify(user));
                    localStorage.setItem('token', token);
                    // redirect to previous url or default to home page
                    router.push(this.returnUrl || '/');
                } else if (authed === false){
                    // update pinia state
                    this.user = user;
                    this.token = token;
                    this.isAdmin = authed;
                    localStorage.setItem('isAdmin', authed);
                    localStorage.setItem('user', JSON.stringify(user));
                    localStorage.setItem('token', token);
                    // redirect to previous url or default to home page
                    router.push(this.returnUrl || '/');
                } else {
                    const alertStore = useAlertStore();
                    alertStore.error(authed.error);    
                }
            } catch (error) {
                const alertStore = useAlertStore();
                console.log(user, error);
                alertStore.error(error);                
            }
        },
        logout() {
            this.user = null;
            localStorage.removeItem('user');
            localStorage.removeItem('token');
            localStorage.removeItem('isAdmin');
            router.push('/');
        }
    }
});
