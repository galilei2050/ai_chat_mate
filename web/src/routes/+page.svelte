<script lang="ts">
</script>

<div class="h-screen flex">
    <div class="w-2/12 border-r border-r-gray-300">
        <div id="New chat button" class="m-4 flex">
            <button class="p-2 flex-grow bg-black text-white rounded-xl shadow-lg flex items-center justify-center">
                <span>
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M11.125 4.375C11.125 4.02982 10.8452 3.75 10.5 3.75C10.1548 3.75 9.875 4.02982 9.875 4.375V9.375H4.875C4.52982 9.375 4.25 9.65482 4.25 10C4.25 10.3452 4.52982 10.625 4.875 10.625H9.875V15.625C9.875 15.9702 10.1548 16.25 10.5 16.25C10.8452 16.25 11.125 15.9702 11.125 15.625V10.625H16.125C16.4702 10.625 16.75 10.3452 16.75 10C16.75 9.65482 16.4702 9.375 16.125 9.375H11.125V4.375Z"
                              fill="white"/>
                    </svg>
                </span>
                <span>New chat</span>
            </button>
        </div>
        <ul class="mx-6 my-8">
            <li class="my-6">
                <a href="/" class="hover:underline hover:font hover:decoration-double">
                    <div class="flex items-center">
                        <span>
                            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M18.25 0.5H1.75003C1.3522 0.5 0.97067 0.658035 0.689366 0.93934C0.408061 1.22064 0.250026 1.60218 0.250026 2V17C0.248331 17.2859 0.329157 17.5662 0.482808 17.8074C0.636459 18.0485 0.85641 18.2401 1.11628 18.3594C1.31486 18.4516 1.53109 18.4996 1.75003 18.5C2.10215 18.4992 2.4426 18.3736 2.71096 18.1456C2.71544 18.1427 2.71953 18.1392 2.72315 18.1353L5.7344 15.5H18.25C18.6479 15.5 19.0294 15.342 19.3107 15.0607C19.592 14.7794 19.75 14.3978 19.75 14V2C19.75 1.60218 19.592 1.22064 19.3107 0.93934C19.0294 0.658035 18.6479 0.5 18.25 0.5ZM18.25 14H5.7344C5.38117 13.9998 5.03922 14.1243 4.76878 14.3516L4.75753 14.3619L1.75003 17V2H18.25V14ZM6.25003 6.5C6.25003 6.30109 6.32904 6.11032 6.4697 5.96967C6.61035 5.82902 6.80111 5.75 7.00003 5.75H13C13.1989 5.75 13.3897 5.82902 13.5304 5.96967C13.671 6.11032 13.75 6.30109 13.75 6.5C13.75 6.69891 13.671 6.88968 13.5304 7.03033C13.3897 7.17098 13.1989 7.25 13 7.25H7.00003C6.80111 7.25 6.61035 7.17098 6.4697 7.03033C6.32904 6.88968 6.25003 6.69891 6.25003 6.5ZM6.25003 9.5C6.25003 9.30109 6.32904 9.11032 6.4697 8.96967C6.61035 8.82902 6.80111 8.75 7.00003 8.75H13C13.1989 8.75 13.3897 8.82902 13.5304 8.96967C13.671 9.11032 13.75 9.30109 13.75 9.5C13.75 9.69891 13.671 9.88968 13.5304 10.0303C13.3897 10.171 13.1989 10.25 13 10.25H7.00003C6.80111 10.25 6.61035 10.171 6.4697 10.0303C6.32904 9.88968 6.25003 9.69891 6.25003 9.5Z"  fill="#1C1C1C"/>
                            </svg>
                        </span>
                        <span class="ml-4">Thread 1</span>
                    </div>
                </a>
            </li>
            <li class="my-6">
                <a href="/" class="hover:underline hover:font hover:decoration-double">
                    <div class="flex items-center">
                        <span>
                            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M18.25 0.5H1.75003C1.3522 0.5 0.97067 0.658035 0.689366 0.93934C0.408061 1.22064 0.250026 1.60218 0.250026 2V17C0.248331 17.2859 0.329157 17.5662 0.482808 17.8074C0.636459 18.0485 0.85641 18.2401 1.11628 18.3594C1.31486 18.4516 1.53109 18.4996 1.75003 18.5C2.10215 18.4992 2.4426 18.3736 2.71096 18.1456C2.71544 18.1427 2.71953 18.1392 2.72315 18.1353L5.7344 15.5H18.25C18.6479 15.5 19.0294 15.342 19.3107 15.0607C19.592 14.7794 19.75 14.3978 19.75 14V2C19.75 1.60218 19.592 1.22064 19.3107 0.93934C19.0294 0.658035 18.6479 0.5 18.25 0.5ZM18.25 14H5.7344C5.38117 13.9998 5.03922 14.1243 4.76878 14.3516L4.75753 14.3619L1.75003 17V2H18.25V14ZM6.25003 6.5C6.25003 6.30109 6.32904 6.11032 6.4697 5.96967C6.61035 5.82902 6.80111 5.75 7.00003 5.75H13C13.1989 5.75 13.3897 5.82902 13.5304 5.96967C13.671 6.11032 13.75 6.30109 13.75 6.5C13.75 6.69891 13.671 6.88968 13.5304 7.03033C13.3897 7.17098 13.1989 7.25 13 7.25H7.00003C6.80111 7.25 6.61035 7.17098 6.4697 7.03033C6.32904 6.88968 6.25003 6.69891 6.25003 6.5ZM6.25003 9.5C6.25003 9.30109 6.32904 9.11032 6.4697 8.96967C6.61035 8.82902 6.80111 8.75 7.00003 8.75H13C13.1989 8.75 13.3897 8.82902 13.5304 8.96967C13.671 9.11032 13.75 9.30109 13.75 9.5C13.75 9.69891 13.671 9.88968 13.5304 10.0303C13.3897 10.171 13.1989 10.25 13 10.25H7.00003C6.80111 10.25 6.61035 10.171 6.4697 10.0303C6.32904 9.88968 6.25003 9.69891 6.25003 9.5Z" fill="#1C1C1C"/>
                            </svg>
                        </span>
                        <span class="ml-4">Thread 2</span>
                    </div>
                </a>
            </li>

        </ul>
    </div>

    <div class="w-10/12 flex flex-col mt-2 mb-2 ">
        <div class="overflow-y-auto grow ">
            <div id="messages" class="flex-grow block">
                <div class="py-4 px-20 w-8/12 mr-auto">
                    <string class="font-bold">AI:</string>
                    <p class="p-4 my-2 rounded-lg bg-neutral-200">Lorem ipsum dolor sit amet, consectetur adipiscing
                        elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                </div>

                <div class="py-4 px-20  w-8/12 ml-auto">
                    <string class="font-bold">User:</string>
                    <p class="p-4 my-2 text-white rounded-lg bg-neutral-500">Lorem ipsum dolor sit amet, consectetur
                        adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                </div>
                <div class="py-4 px-20 w-8/12 mr-auto">
                    <string class="font-bold">AI:</string>
                    <p class="p-4 my-2 rounded-lg bg-neutral-200">Lorem ipsum dolor sit amet, consectetur adipiscing
                        elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                </div>

                <div class="py-4 px-20  w-8/12 ml-auto">
                    <string class="font-bold">User:</string>
                    <p class="p-4 my-2 text-white rounded-lg bg-neutral-500">Lorem ipsum dolor sit amet, consectetur
                        adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                </div>
                <div class="py-4 px-20 w-8/12 mr-auto">
                    <string class="font-bold">AI:</string>
                    <p class="p-4 my-2 rounded-lg bg-neutral-200">Lorem ipsum dolor sit amet, consectetur adipiscing
                        elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                </div>

                <div class="py-4 px-20  w-8/12 ml-auto">
                    <string class="font-bold">User:</string>
                    <p class="p-4 my-2 text-white rounded-lg bg-neutral-500">Lorem ipsum dolor sit amet, consectetur
                        adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                </div>
                <div class="py-4 px-20 w-8/12 mr-auto">
                    <string class="font-bold">AI:</string>
                    <p class="p-4 my-2 rounded-lg bg-neutral-200">Lorem ipsum dolor sit amet, consectetur adipiscing
                        elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                </div>

                <div class="py-4 px-20  w-8/12 ml-auto">
                    <string class="font-bold">User:</string>
                    <p class="p-4 my-2 text-white rounded-lg bg-neutral-500">Lorem ipsum dolor sit amet, consectetur
                        adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                </div>
            </div>
        </div>
        <div id="type_message" class="my-2">
            <div class="mx-auto w-8/12 flex relative">
                <input type="text" class="rounded-xl py-4 pl-6 pr-12 bg-neutral-100 mr-1 w-full  overflow-hidden focus:outline-neutral-200 " placeholder="Type your message..."/>
                <button class="absolute right-4 h-full">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M17.4898 8.90625L4.36484 1.41485C4.1436 1.29074 3.88983 1.23689 3.63726 1.26043C3.38468 1.28398 3.14525 1.38382 2.95076 1.54668C2.75628 1.70954 2.61594 1.92772 2.54841 2.17224C2.48087 2.41676 2.48933 2.67603 2.57265 2.91563L4.99452 9.9836C4.99421 9.98619 4.99421 9.98882 4.99452 9.99141C4.99409 9.994 4.99409 9.99664 4.99452 9.99922L2.57265 17.0828C2.50592 17.2713 2.48538 17.473 2.51274 17.6711C2.5401 17.8691 2.61458 18.0577 2.72991 18.2211C2.84525 18.3844 2.99808 18.5177 3.17557 18.6097C3.35307 18.7017 3.55005 18.7498 3.74999 18.75C3.96692 18.7495 4.18004 18.6929 4.36874 18.5859L17.4867 11.082C17.6802 10.9736 17.8414 10.8157 17.9537 10.6245C18.066 10.4332 18.1254 10.2155 18.1258 9.99372C18.1262 9.77193 18.0676 9.55403 17.956 9.36237C17.8443 9.17072 17.6837 9.01222 17.4906 8.90313L17.4898 8.90625ZM3.74999 17.5V17.493L6.10468 10.625H10.625C10.7908 10.625 10.9497 10.5592 11.0669 10.4419C11.1841 10.3247 11.25 10.1658 11.25 10C11.25 9.83424 11.1841 9.67527 11.0669 9.55806C10.9497 9.44085 10.7908 9.375 10.625 9.375H6.11093L3.75468 2.50938L3.74999 2.5L16.875 9.98672L3.74999 17.5Z" fill="#1C1C1C" fill-opacity="0.4"/>
                    </svg>
                </button>
            </div>
        </div>
    </div>
</div>