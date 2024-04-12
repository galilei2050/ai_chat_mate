import adapter from '@sveltejs/adapter-node';
import {vitePreprocess} from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    // Consult https://kit.svelte.dev/docs/integrations#preprocessors
    // for more information about preprocessors
    preprocess: vitePreprocess(),
    env: {
        publicPrefix: "",
        privatePrefix: '',
    },
    kit: {
        csp: {
            directives: {
                'img-src': [
                    'self',
                    'https://lh2.googleusercontent.com',
                    'https://lh3.googleusercontent.com',
                ],
                'default-src': [
                    "self",
                ],
                'worker-src': [
                    'self',
                ],
                'style-src': [
                    'self',
                    'unsafe-inline',
                    'https://accounts.google.com'
                ],
                'script-src': [
                    "self",
                    "https://apis.google.com",
                    "https://accounts.google.com"
                ],
                'frame-src': [
                    'self',
                    'https://chat.baskakov.us',
                    "https://accounts.google.com"
                ],
                'connect-src': [
                    'self',
                    "https://accounts.google.com/",
                    "https://identitytoolkit.googleapis.com"
                ],
            }
        },
        // adapter-auto only supports some environments, see https://kit.svelte.dev/docs/adapter-auto for a list.
        // If your environment is not supported or you settled on a specific environment, switch out the adapter.
        // See https://kit.svelte.dev/docs/adapters for more information about adapters.
        adapter: adapter({
            out: 'build',
            precompress: true,
        })
    }
};

export default config;
