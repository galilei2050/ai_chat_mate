<script lang="ts">
    import {redirect_to_last_thread} from '$lib/redirect_to_last_thread';
    import {onMount} from 'svelte';

    export let data: object | null = null;

    onMount(() => {
        redirect_to_last_thread(data);
    });

</script>
