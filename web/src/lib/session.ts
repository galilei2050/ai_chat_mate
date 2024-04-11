import {writable, type Writable} from 'svelte/store';
import {browser} from '$app/environment';
import {goto} from "$app/navigation";

import Cookies from "js-cookie"
import {type FirebaseApp, getApps, initializeApp} from 'firebase/app';
import {type Auth, browserLocalPersistence, getAuth, onAuthStateChanged} from 'firebase/auth';

import {
    PUBLIC_FIREBASE_API_KEY,
    PUBLIC_FIREBASE_APP_ID,
    PUBLIC_FIREBASE_MEASUREMENT_ID,
    PUBLIC_ORIGIN,
    PUBLIC_PROJECT_ID
} from '$env/static/public';

export let firebaseApp: FirebaseApp, firebaseAuth: Auth;

export type User = {
    email?: string | null;
    displayName?: string | null;
    photoURL?: string | null;
    uid?: string | null;
};

export type SessionState = {
    user: User | null;
    accessToken?: string | null;
};

export const session = <Writable<SessionState>>writable();

export const initializeFirebase = () => {
    if (!browser) {
        throw new Error("Can't use the Firebase client on the server.");
    }
    const firebaseConfig = {
        apiKey: PUBLIC_FIREBASE_API_KEY,
        authDomain: PUBLIC_ORIGIN,
        projectId: PUBLIC_PROJECT_ID,
        appId: PUBLIC_FIREBASE_APP_ID,
        measurementId: PUBLIC_FIREBASE_MEASUREMENT_ID
    }
    if (!firebaseApp) {
        let existingApps = getApps();
        if (existingApps.length > 0) {
            firebaseApp = existingApps[0];
        } else {
            firebaseApp = initializeApp(firebaseConfig);
            firebaseAuth = getAuth(firebaseApp);
            firebaseAuth.setPersistence(browserLocalPersistence)
            firebaseAuth.useDeviceLanguage();
        }
    }
}

export const initializeSessionChange = () => {
    if (!browser) {
        return
    }
    onAuthStateChanged(firebaseAuth, (user) => {
        if (user) {
            console.log(`User logged in: ${user.email} from ${user.providerId}`)
            session.set({
                user: {
                    email: user.email,
                    displayName: user.displayName,
                    photoURL: user.photoURL,
                    uid: user.uid
                }
            })
        } else {
            console.log('User logged out')
            Cookies.remove('token')
            session.set({user: null})
            goto('/login')

        }
    })
}