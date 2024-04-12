<script lang="ts">
    import {onMount} from 'svelte';
    import {goto} from "$app/navigation";

    export let data: { last_thread_id: number }  | null = null;
    onMount(() => {
        console.log('Mounted Thread');
    });

    onMount(() => {
        const last_thread_id: number | undefined = data?.last_thread_id
        if (last_thread_id) {
            goto(`/thread/${last_thread_id}`);
        } else {
            goto('/thread');
        }
    });

</script>
