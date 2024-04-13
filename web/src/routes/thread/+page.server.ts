import {BACKEND_BASE_URL} from "$env/static/private"

export async function load({params}) {
    return {
        last_thread_id: null
    }
}

export const actions = {
    default: async (event) => {
        await fetch(`${BACKEND_BASE_URL}/api/thread/`)
    }
}