<script type="ts">
    import InputBar from "./InputBar.svelte";
    import Messages from "./Messages.svelte";
    import {afterUpdate} from 'svelte';
    import current_thread_id from "../store";

    export let data;

    afterUpdate(async () => {
        current_thread_id.set(data.thread_id);
    });
</script>

<div class="overflow-y-auto grow ">
    <div class="flex-grow block" id="messages">
        <Messages messages={data.messages}/>
    </div>
</div>

<div class="my-2" id="type_message">
    <InputBar/>
</div>