<script lang="ts">
    import {onMount} from "svelte";
    import {firebaseAuth} from "$lib/firebase_client";
    import {GoogleAuthProvider, signInWithRedirect} from "firebase/auth";
    import {session, type SessionState} from "$lib/session";
    import {GOOGLE_CLIENT_ID} from "$env/static/public"

    let email = '';
    let password = '';

    onMount(() => {
        console.log('Mounted main');
    });
</script>


<svelte:head>
    <script src="https://accounts.google.com/gsi/client"></script>
</svelte:head>

<div class="flex flex-col h-screen mx-auto items-center justify-center">
    <div id="google_btn" class="max-h-12">
    </div>
    <p class="py-6">
        OR
    </p>
    <div class="flex-col flex">
        <input class="rounded-xl py-3 px-6 bg-neutral-100 mr-1 overflow-hidden focus:outline-neutral-200 mb-4"
               type="email" bind:value={email} placeholder="Email"/>
        <input class="rounded-xl py-3 px-6 bg-neutral-100 mr-1 overflow-hidden focus:outline-neutral-200 mb-6"
               type="password" bind:value={password} placeholder="Password"/>
        <button class="rounded-xl py-3 px-6 bg-black text-white shadow-lg"
                on:click={login}>Continue with email
        </button>
    </div>
</div>