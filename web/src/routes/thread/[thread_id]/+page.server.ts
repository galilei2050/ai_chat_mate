// @ts-ignore
import { messages } from '../database'
import { session } from "$lib/session";

export function load({params}) {
    /**
     * @type {{ role: string; content: string; }[]}
     */
    console.log(session?.accessToken)
    return {
        thread_id: params.thread_id,
        messages: messages.get(params.thread_id)
    }
}

export const actions = {
    default: async (event) => {
        const thread_id = event.params.thread_id;
        const form_data = await event.request.formData()
        messages.get(thread_id).push({
            role: 'user',
            content: form_data.get('message')
        })
    }
}