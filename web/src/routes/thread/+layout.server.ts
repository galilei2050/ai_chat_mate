import { messages } from "./database";

interface Thread {
    id: string;
    title: string;
}

export async function load({params}) {
    return {
            threads: await fetch(
            '/api/thread'
        )
    }
}