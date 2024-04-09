import {initializeApp, type FirebaseApp} from 'firebase/app';
import {getAuth, type Auth} from 'firebase/auth';

import {browser} from '$app/environment';


export let firebaseApp: FirebaseApp;
export let firebaseAuth: Auth;

// const firebaseConfig = {
//     apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
//     appId: import.meta.env.VITE_FIREBASE_APP_ID,
//     authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
//     measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID,
// 	projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
// };

const firebaseConfig = {

}

export const initializeFirebase = () => {
    if (!browser) {
        throw new Error("Can't use the Firebase client on the server.");
    }
    if (!firebaseApp) {
        firebaseApp = initializeApp(firebaseConfig);
        firebaseAuth = getAuth(firebaseApp);
    }
};