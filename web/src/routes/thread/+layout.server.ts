import { messages } from "./database";

interface Thread {
    id: string;
    title: string;
}

export function load({params}) {
    let threads: Array<Thread> = []

    messages.forEach((value, key) => {
        threads.push({
            id: key,
            title: 'Thread ' + key
        })
    })

    return {
        threads: threads
    }
}