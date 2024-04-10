<script lang="ts">
    import ThreadsList from "./ThreadsList.svelte";
    import NewThreadButton from "./NewThreadButton.svelte";
    import User from "$lib/components/User.svelte";
    import {onMount} from "svelte";

    export let data;
        onMount(() => {
        console.log('Mounted Thread Layout');
    });

</script>

<div class="h-screen flex">
    <div class="w-2/12 border-r border-r-gray-300">
        <div class="flex flex-col h-full">
        <div class="mx-4 mt-4 mb-2">
            <NewThreadButton/>
        </div>
        <div class="mx-6 my-2 grow">
            <ThreadsList threads={data.threads}/>
        </div>
        <div class="mx-4 my-6">
            <User></User>
        </div>
        </div>
    </div>

    <div class="w-10/12 flex flex-col mt-2 mb-2 ">
        <slot/>
    </div>
</div>
