<script lang="ts">
    import {onMount} from "svelte";
    import {firebaseAuth} from "$lib/firebase_client";
    import {
        createUserWithEmailAndPassword,
        GoogleAuthProvider,
        signInWithCredential,
        signInWithEmailAndPassword,
        type UserCredential
    } from "firebase/auth";

    import {session, type SessionState} from "$lib/session";
    import {PUBLIC_GOOGLE_CLIENT_ID} from "$env/static/public"

    let email = '';
    let password = '';
    let googleButton: HTMLDivElement | null;

    let processCredentials = (credentails: UserCredential) => {
        const user = credentails.user;
        const sessionState: SessionState = {
            user: user,
            accessToken: credentails.credential.accessToken
        }
        session.set(sessionState);
    }

    export function handleGoogleSignIn(response: any) {
        const idToken = response.credential;
        const credential = GoogleAuthProvider.credential(idToken);

        GoogleAuthProvider.credentialFromResult(response.credential);
        signInWithCredential(firebaseAuth, credential)
            .then(processCredentials)
            .catch((error) => {
                const errorCode = error.code;
                const errorMessage = error.message;
                console.error(`Error ${errorCode} while sign in with google: ${errorMessage}`);
            });
    }

    let authWithEmail = () => {
        signInWithEmailAndPassword(firebaseAuth, email, password)
            .then(processCredentials)
            .catch((error) => {
                const errorCode = error.code;
                const errorMessage = error.message;
                console.warn(`Error ${errorCode} while sing in with email: ${errorMessage}`);
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

    onMount(() => {
        console.log('Mounted main');
    });

    onMount(() => {
        if (window.google && googleButton != null) {
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
                }
            );
            google.accounts.id.prompt();
        } else {
            console.log('Google API not loaded');
        }
    });

</script>

<svelte:head>
    <script src="https://accounts.google.com/gsi/client"></script>
</svelte:head>

<div class="flex flex-col h-screen mx-auto items-center justify-center">
    <div class="max-h-12">
        <div id="google_btn" bind:this={googleButton}>
        </div>
    </div>
    <p class="py-6">
        OR
    </p>
    <div>
        <form on:submit={authWithEmail} class="flex-col flex">
            <input
                    class="rounded-xl py-3 px-6 bg-neutral-100 mr-1 overflow-hidden focus:outline-neutral-200 mb-4"
                    type="email"
                    bind:value={email}
                    placeholder="Email"
                    autocomplete="username"
            />
            <input
                    class="rounded-xl py-3 px-6 bg-neutral-100 mr-1 overflow-hidden focus:outline-neutral-200 mb-6"
                    type="password"
                    bind:value={password}
                    placeholder="Password"
                    autocomplete="current-password"
            />
            <button
                    class="rounded-xl py-3 px-6 bg-black text-white shadow-lg"
                    on:click={authWithEmail}>
                Continue with email
            </button>
        </form>
    </div>
</div>