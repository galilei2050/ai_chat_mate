<script type="ts">
    import InputBar from "./InputBar.svelte";
    import Messages from "./Messages.svelte";

    export let data;

</script>

<div class="overflow-y-auto grow ">
    <div class="flex-grow block" id="messages">
        <Messages messages={data.messages}/>
    </div>
</div>

<div class="my-2" id="type_message">
    <InputBar/>
</div>