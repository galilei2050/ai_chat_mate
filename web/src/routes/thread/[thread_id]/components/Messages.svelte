<script lang="ts">
    import * as marked from 'marked';

    export let messages: object[] = [];

</script>

{#if messages}
    {#each messages as message}
        {#if message.role === 'user'}
            <div class="py-4 px-20  w-8/12 ml-auto">
                <string class="font-bold">You:</string>
                <p class="p-4 my-2 rounded-lg bg-neutral-200">{@html marked.parse(message?.content)}</p>
            </div>
        {:else }
            <div class="py-4 px-20 w-8/12 mr-auto">
                <string class="font-bold">AI:</string>
                <p class="p-4 my-2 rounded-lg bg-neutral-200">{@html marked.parse(message?.content)}</p>
            </div>
        {/if}

    {/each}
{/if}