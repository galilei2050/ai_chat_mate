<script lang="ts">
    import { enhance } from "$app/forms";
</script>

<form class="flex" id="New chat button" method="POST" action="/thread" use:enhance>
    <button class="p-2 flex-grow bg-black text-white rounded-xl shadow-lg flex items-center justify-center">
        <span>
            <svg fill="none" height="20" viewBox="0 0 20 20" width="20" xmlns="http://www.w3.org/2000/svg">
                <path d="M11.125 4.375C11.125 4.02982 10.8452 3.75 10.5 3.75C10.1548 3.75 9.875 4.02982 9.875 4.375V9.375H4.875C4.52982 9.375 4.25 9.65482 4.25 10C4.25 10.3452 4.52982 10.625 4.875 10.625H9.875V15.625C9.875 15.9702 10.1548 16.25 10.5 16.25C10.8452 16.25 11.125 15.9702 11.125 15.625V10.625H16.125C16.4702 10.625 16.75 10.3452 16.75 10C16.75 9.65482 16.4702 9.375 16.125 9.375H11.125V4.375Z"
                      fill="white"/>
            </svg>
        </span>
        <span>New chat</span>
    </button>
</form>