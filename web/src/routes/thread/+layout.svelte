<script lang="ts">
    import ThreadsList from "./ThreadsList.svelte";
    import NewThreadButton from "./NewThreadButton.svelte";

    export let data;
</script>

<div class="h-screen flex">
    <div class="w-2/12 border-r border-r-gray-300">
        <NewThreadButton/>
        <ThreadsList threads={data.threads}/>
    </div>
    <div class="w-10/12 flex flex-col mt-2 mb-2 ">
        <slot/>
    </div>
</div>
