<script lang="ts">
    import "../app.css";
    import {initializeFirebase} from "$lib/firebase_client"
    import {onMount} from "svelte";
    import {initializeSessionChange} from "$lib/session";

    onMount(() => {
        console.log('Mounted Main Layout');
    });

    onMount(() => {
        initializeFirebase()
        initializeSessionChange()
    });

</script>

<slot/>