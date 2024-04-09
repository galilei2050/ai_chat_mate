<script lang="ts">
    import {onMount} from "svelte";
    import { GoogleAuthProvider, EmailAuthProvider } from "firebase/auth";

    onMount(() => {
        console.log('Mounted main');
    });
</script>

<div class="flex h-screen mx-auto items-center justify-center">
<p>
    Here will be login page
</p>
</div>