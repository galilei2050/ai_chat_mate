import {BACKEND_BASE_URL} from "$env/static/private"

export async function load({fetch, request, params}) {
    let url = `${BACKEND_BASE_URL}/api/thread/`
    const response: Response = await fetch(url,
        {
            headers: request.headers
        }
    )
    const threads = await response.json()
    return {
        threads: threads
    }
}
