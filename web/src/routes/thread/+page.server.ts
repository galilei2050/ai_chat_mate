import {messages, max_thread_id} from "./database";

export function load({params}) {
    return {
        last_thread_id: max_thread_id()
    }
}

export const actions = {
    default: async (event) => {
        messages.set((max_thread_id() + 1).toString(), [])
        return {
            last_thread_id: max_thread_id()
        }
    }
}