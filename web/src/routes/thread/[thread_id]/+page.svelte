<script lang="ts">
    import InputBar from "./InputBar.svelte";
    import Messages from "./Messages.svelte";
    import {afterUpdate} from 'svelte';
    import current_thread_id from "../store";

    let messagesContainer: HTMLDivElement | undefined;

    export let data;

    afterUpdate(async () => {
        messagesContainer?.scrollIntoView(false);
        current_thread_id.set(data.thread_id);
    });
</script>

<div class="overflow-y-auto grow ">
    <div class="flex-grow block" id="messages" bind:this={messagesContainer}>
        <Messages messages={data.messages}/>
    </div>
</div>

<div class="my-2" id="type_message">
    <InputBar/>
</div>