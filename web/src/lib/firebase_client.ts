import {type FirebaseApp, getApps, initializeApp} from 'firebase/app';
import {type Auth, getAuth} from 'firebase/auth';
import {browser} from '$app/environment';
import {
    PUBLIC_FIREBASE_API_KEY,
    PUBLIC_FIREBASE_APP_ID,
    PUBLIC_ORIGIN,
    PUBLIC_PROJECT_ID,
    PUBLIC_FIREBASE_MEASUREMENT_ID
} from '$env/static/public';


export let firebaseApp: FirebaseApp;
export let firebaseAuth: Auth;

const firebaseConfig = {
    apiKey: PUBLIC_FIREBASE_API_KEY,
    authDomain: PUBLIC_ORIGIN,
    projectId: PUBLIC_PROJECT_ID,
    messagingSenderId: "677393736522",
    appId: PUBLIC_FIREBASE_APP_ID,
    measurementId: PUBLIC_FIREBASE_MEASUREMENT_ID
}

export const initializeFirebase = () => {
    if (!browser) {
        throw new Error("Can't use the Firebase client on the server.");
    }
    if (!firebaseApp) {
        let existingApps = getApps();
        if (existingApps.length > 0) {
            firebaseApp = existingApps[0];
        } else {
            firebaseApp = initializeApp(firebaseConfig);

            firebaseAuth = getAuth(firebaseApp);
            firebaseAuth.useDeviceLanguage();
        }
    }
}