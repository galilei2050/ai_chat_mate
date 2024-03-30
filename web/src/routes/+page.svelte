<script lang="ts">
</script>

<div class="h-screen flex">

    <div class="w-2/12 bg-gray-200 border-gray-700 border-2 m-2 rounded-md">
        <button class="block mt-16 mx-4 py-2 px-8 bg-gray-600 text-white rounded-md shadow-lg font-bold">
            New Chat
        </button>
        <ul class="mx-4 mt-12">
            <li class="my-4">
                <a href="/" class="hover:underline hover:font-bold hover:decoration-double">
                    <div class="flex items-center">
                        <span class="icon-[charm--messages] size-6 mr-1"></span><span class="mx-1">Thread 1</span>
                    </div>
                </a>
            </li>
              <li class="my-4">
                <a href="/" class="hover:underline hover:font-bold hover:decoration-double">
                    <div class="flex items-center">
                        <span class="icon-[charm--messages] size-6 mr-1"></span><span class="ml-1">Thread 2</span>
                    </div>
                </a>
            </li>
        </ul>
    </div>

    <div class="w-10/12 bg-gray-50 overflow-y-auto border-gray-700 rounded-md border-2 flex flex-col mr-2 mt-2 mb-2">
        <div id="messages" class="flex-grow block">
            <div class="m-4 p-4 bg-white border-2 border-gray-500 rounded-md w-8/12 mr-auto">
                <string class="font-bold">AI:</string>
                <p> Some text </p>
            </div>

            <div class="m-4 p-4 bg-white border-2 border-gray-500 rounded-md w-8/12 ml-auto">
                <string class="font-bold">User:</string>
                <p> Some text </p>
            </div>
        </div>

        <div id="type_message" class="my-3">
            <div class="mx-auto border-gray-700 border-2 bg-white rounded-md w-8/12 flex px-4 py-2  ">
                <textarea class="mr-1 w-full p-2 rounded overflow-hidden focus:outline-gray-400 " rows="2" placeholder="Type your message..."> </textarea>
                <button class="ml-1"><span class="icon-[formkit--submit] min-w-8 text-black h-full"></span></button>
            </div>
        </div>
    </div>
</div>