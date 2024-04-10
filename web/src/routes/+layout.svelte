<script lang="ts">
    import "../app.css";
    import {initializeFirebase} from "$lib/firebase_client"
    import {onMount} from "svelte";
    import {initializeSessionChange, session} from "$lib/session";
    import {goto} from "$app/navigation";

    onMount(() => {
        console.log('Mounted Main Layout');
    });

    onMount(() => {
        initializeFirebase()
        initializeSessionChange()
    });

    onMount(() => {
        session.subscribe((value) => {
            if (!value?.user) {
                console.log('redirecting to /login');
                goto('/login')
            } else {
                console.log('redirecting to /thread');
                goto('/thread')
            }
        });
    });
</script>

<slot/>