<script lang="ts">
    import "../app.css";
    import {onMount} from "svelte";
    import {initializeFirebase, initializeSessionChange} from "$lib/session";

    onMount(() => {
        console.log('Mounted Main Layout');
    });

    onMount(() => {
        initializeFirebase()
        initializeSessionChange()
    });

</script>

<slot/>