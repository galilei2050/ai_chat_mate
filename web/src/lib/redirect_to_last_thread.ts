import {goto} from '$app/navigation';
import {browser} from '$app/environment'; // import browser from $app/env

interface ThreadData {
    last_thread_id: number;
}

export async function redirect_to_last_thread(data: ThreadData | null) {
    if (!browser) return;
    const last_thread_id: number | undefined = data?.last_thread_id
    if (last_thread_id) {
        goto(`/thread/${last_thread_id}`);
    } else {
        goto('/thread');
    }
}