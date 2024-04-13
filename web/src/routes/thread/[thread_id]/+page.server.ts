import {BACKEND_BASE_URL} from "$env/static/private"
import {copy_some_headers} from "$lib/server/headers";


export async function load({fetch, params, request}) {
    /**
     * @type {{ role: string; content: string; }[]}
     */
    const url = `${BACKEND_BASE_URL}/api/thread/${params.thread_id}`
    const response: Response = await fetch(url, {
        headers: copy_some_headers(request.headers)
    })
    const messages = await response.json()
    return {
        thread_id: params.thread_id,
        messages: messages
    }
}

export const actions = {
    put: async ({fetch, params, request}) => {
        const thread_id = params.thread_id;
        const form_data = await request.formData()
        const message = form_data.get('message')
        const uuid = form_data.get('uuid')
        const url = `${BACKEND_BASE_URL}/api/thread/${thread_id}`
        const body = JSON.stringify({
            uuid: uuid,
            role: 'user',
            content: message
        })
        let headers = copy_some_headers(request.headers)
        headers['content-type'] = 'application/json'
        let result = await fetch(url, {
                method: 'POST',
                body: body,
                headers: headers
            }
        )
    },
    update: async (event) => {

    }
}
