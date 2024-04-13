import {BACKEND_BASE_URL} from "$env/static/private"
import {copy_some_headers} from "$lib/server/headers";

export async function load({params}) {
    return {
        last_thread_id: null
    }
}

export const actions = {
    default: async ({fetch, request}) => {
        const url = `${BACKEND_BASE_URL}/api/thread/`
        const response: Response = await fetch(url, {
            method: 'POST',
            headers: copy_some_headers(request.headers)
        })
    }
}