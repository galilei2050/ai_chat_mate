import {BACKEND_BASE_URL} from "$env/static/private"
import {copy_some_headers} from "$lib/server/headers";

export async function load({fetch, request, params}) {
    let url = `${BACKEND_BASE_URL}/api/thread/`
    const response: Response = await fetch(url, {
        headers: copy_some_headers(request.headers)
    })
    const threads = await response.json()
    return {
        threads: threads
    }
}