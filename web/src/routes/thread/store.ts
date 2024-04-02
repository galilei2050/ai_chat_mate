import { writable } from 'svelte/store';

const current_thread_id = writable<string>("");

export default current_thread_id;