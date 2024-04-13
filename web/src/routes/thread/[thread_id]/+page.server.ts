import {BACKEND_BASE_URL} from "$env/static/private"


export async function load({fetch, params}) {
    /**
     * @type {{ role: string; content: string; }[]}
     */
    const url = `${BACKEND_BASE_URL}/api/thread/${params.thread_id}/`
    const response: Response = await fetch(url)
    const messages = await response.json()
    return {
        thread_id: params.thread_id,
        messages: messages
    }
}

export const actions = {
    default: async ({fetch, params, request}) => {
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
        await fetch(url, {
                method: 'POST',
                body: body
            }
        )
    }
}
