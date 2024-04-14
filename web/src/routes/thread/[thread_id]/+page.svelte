<script lang="ts">
    import {afterUpdate} from 'svelte';
    import {enhance} from "$app/forms";
    import {get} from 'svelte/store';

    import InputBar from "./components/InputBar.svelte";
    import Messages from "./components/Messages.svelte";

    import current_thread_id from "../thread_store";

    let messagesContainer: HTMLDivElement | undefined;
    let submitButton: HTMLInputElement | undefined;

    export let data;
    let messages_count = 0;
    afterUpdate(async () => {
        const thread_uuid = data?.thread_id
        if (thread_uuid != get(current_thread_id)) {
            current_thread_id.set(data?.thread_id);
            console.log(`Set current thread to ${data?.thread_id}`)
        }
        if (data?.messages && data.messages.length !== messages_count) {
            messagesContainer?.scrollIntoView(false);
            messages_count = data.messages.length
        }
        setTimeout(clear_data, 3000)
    });

    let clear_data = () => {
        submitButton?.click()
    }

</script>

<div class="overflow-y-auto grow ">
    <div class="flex-grow block" id="messages" bind:this={messagesContainer}>
        <Messages messages={data?.messages}/>
    </div>
</div>

<div class="my-2" id="type_message">
    <InputBar/>
</div>

<form use:enhance method="POST" action="?/update">
    <input class="hidden" type="submit" bind:this={submitButton} >
</form>