<script lang="ts">
    import {firebaseAuth, session, type User} from "$lib/session";
    import {signOut} from "firebase/auth";

    const logout = async () => {
        await signOut(firebaseAuth);
    }

    const getUserDisplayName = (user: User | null): string => {
        return user?.displayName || user?.email || 'Unknown user';
    }
</script>

<div class="flex items-center w-full mr-auto">
    {#if $session?.user}
        {#if $session.user.photoURL}
            <img src={$session.user.photoURL} alt="User Icon" class="rounded-full h-8 w-8"/>
        {/if}
        <p class="mx-2 overflow-clip">{getUserDisplayName($session?.user)}</p>
        <button class="mx-2" on:click={logout}>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                 class="lucide lucide-log-out">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                <polyline points="16 17 21 12 16 7"/>
                <line x1="21" x2="9" y1="12" y2="12"/>
            </svg>
        </button>
    {/if}
</div>