<script lang="ts">
    import ThreadsList from "./ThreadsList.svelte";
    import NewThreadButton from "./NewThreadButton.svelte";
    import {onMount} from "svelte";

    export let data;
        onMount(() => {
        console.log('Mounted Thread Layout');
    });

</script>

<div class="h-full flex">
    <div class="w-2/12 border-r border-r-gray-300">
        <NewThreadButton/>
        <ThreadsList threads={data.threads}/>
    </div>
    <div class="w-10/12 flex flex-col mt-2 mb-2 ">
        <slot/>
    </div>
</div>
