<script lang="ts">
    import {afterUpdate, onMount} from 'svelte';
    import {enhance} from "$app/forms";

    import InputBar from "./components/InputBar.svelte";
    import Messages from "./components/Messages.svelte";

    import current_thread_id from "../thread_store";

    let messagesContainer: HTMLDivElement | undefined;
    let submitButton: HTMLInputElement | undefined;

    export let data;

    afterUpdate(async () => {
        messagesContainer?.scrollIntoView(false);
        current_thread_id.set(data?.thread_id);
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