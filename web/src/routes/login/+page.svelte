<script lang="ts">
    import {onMount} from "svelte";
    import {goto} from "$app/navigation";
    import {browser} from "$app/environment";

    import {firebaseAuth} from "$lib/session";

    import {
        createUserWithEmailAndPassword,
        GoogleAuthProvider,
        signInWithCredential,
        signInWithEmailAndPassword,
        type UserCredential
    } from "firebase/auth";

    import {PUBLIC_GOOGLE_CLIENT_ID} from "$env/static/public"

    let email = '';
    let password = '';
    let googleButton: HTMLDivElement | null;
    let googleButtonInitialized = false;

    let processCredentials = async (credentails: UserCredential) => {;
        const accessToken = await credentails.user.getIdToken(false)
        fetch('/login', {
            method: "POST",
            headers: [
                ["authorization", "bearer " + accessToken],
            ],
            body: JSON.stringify({
                accessToken: accessToken
            })
        }).then((value: Response) => {
            console.log('Authentication finished successfully')
            goto('/')
        }).catch((reason) => {
            console.error(`Failed to set cookies through backend ${reason}`)
        })
    }

    export function handleGoogleSignIn(response: any) {
        const idToken = response.credential;
        const credential = GoogleAuthProvider.credential(idToken);
        signInWithCredential(firebaseAuth, credential)
            .then(processCredentials)
            .catch((error) => {
                const errorCode = error.code;
                const errorMessage = error.message;
                console.warn(`Error ${errorCode} while sign in with google: ${errorMessage}`);
            });
    }

    let authWithEmail = () => {
        signInWithEmailAndPassword(firebaseAuth, email, password)
            .then(processCredentials)
            .catch((error) => {
                const errorCode = error.code;
                const errorMessage = error.message;
                console.warn(`Error ${errorCode} while sign in with email: ${errorMessage}`);
                if (errorCode === 'auth/invalid-credential') {
                    createUserWithEmailAndPassword(firebaseAuth, email, password)
                        .then(processCredentials)
                        .catch((error) => {
                            const errorCode = error.code;
                            const errorMessage = error.message;
                            console.warn(`Error ${errorCode} while creating user with email: ${errorMessage}`);
                        });
                }
            });
    }

    let setupGoogleButton = async () => {
        if (window.google && googleButton != null && browser) {
            console.log('Google API loaded');
            window.google.accounts.id.initialize({
                client_id: PUBLIC_GOOGLE_CLIENT_ID,
                callback: handleGoogleSignIn
            });

            google.accounts.id.renderButton(googleButton, {
                    theme: "outline",
                    size: "large",
                    type: "standard",
                    text: "continue_with",
                    shape: "square",
                    width: 250,
                }
            );
            googleButtonInitialized = true;
            setTimeout(() => {
                google.accounts.id.prompt()
            }, 500);
        } else {
            console.log('Google API is not loaded.');
            setTimeout(() => {
                setupGoogleButton()
            }, 500);
        }
    }
    onMount(() => {
        console.log('Mounted main');
    });

    onMount(() => {
        setupGoogleButton()
    });

</script>

<svelte:head>
    <link href="https://accounts.google.com/gsi/style" rel="stylesheet"/>
    <script async defer src="https://accounts.google.com/gsi/client"></script>
</svelte:head>

<div class="flex flex-col h-screen mx-auto items-center justify-center">
    <div class:hidden={!googleButtonInitialized}>
        <form on:submit={authWithEmail} class="flex-col flex">
            <input
                    class="rounded-xl py-3 px-6 bg-neutral-100 mr-1 overflow-hidden focus:outline-neutral-200 mb-4"
                    name="email"
                    type="email"
                    bind:value={email}
                    placeholder="Email"
                    autocomplete="username"
            />
            <input
                    class="rounded-xl py-3 px-6 bg-neutral-100 mr-1 overflow-hidden focus:outline-neutral-200 mb-6"
                    name="password"
                    type="password"
                    bind:value={password}
                    placeholder="Password"
                    autocomplete="current-password"
            />
            <button
                    class="rounded-xl py-3 px-6 bg-black text-white shadow-lg"
                    type="submit"
            >
                Continue with email
            </button>
        </form>
    </div>
    <p class="py-6 text-xs">
        OR
    </p>
    <div bind:this={googleButton} id="google_btn"/>
</div>