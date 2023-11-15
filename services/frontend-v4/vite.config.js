import { fileURLToPath, URL } from 'url';

import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import dns from 'dns'

dns.setDefaultResultOrder('verbatim')
const prod = process.env.VITE_STATUS === 'PROD' ? true : false;
// function crossOriginIsolationMiddleware(_, response, next) {
//     response.setHeader("Cross-Origin-Opener-Policy", "same-origin");
//     response.setHeader("Cross-Origin-Embedder-Policy", "require-corp");
//     next();
// }

// https://vitejs.dev/config/
export default defineConfig({
    server: {
        host: true,
        port: 80,
        strictPort: true,
        watch: {
            usePolling: prod,
        },
    },
    plugins: [vue(),
        // {
        //     name: "configure-response-headers",
        //     configureServer: (server) => {
        //         server.middlewares.use((_req, res, next) => {
        //             res.setHeader("Access-Control-Allow-Credentials", "true");
        //             res.setHeader("Access-Control-Allow-Origin", "http://bulattim.tplinkdns.com https://oauth.telegram.org");
        //             res.setHeader("Vary", "Accept-Encoding, Origin");
        //             res.setHeader("Content-Security-Policy", "frame-ancestors http://bulattim.tplinkdns.com https://oauth.telegram.org");
        //             // console.log(res);
        //             next();
        //         });
        //     },
        // },
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    }
});
