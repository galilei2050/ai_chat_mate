import {BACKEND_BASE_URL} from "$env/static/private"

interface Thread {
    id: string;
    title: string;
}

export async function load({fetch, params}) {
    let url = `${BACKEND_BASE_URL}/api/thread/`
    const response: Response = await fetch(url)
    const threads = await response.json()
    return {
        threads: threads
    }
}
