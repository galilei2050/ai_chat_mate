import { writable, type Writable } from 'svelte/store';
import {browser} from '$app/environment';
import {firebaseAuth} from "$lib/firebase_client";
import {onAuthStateChanged} from "firebase/auth"

type User = {
	email?: string | null;
	displayName?: string | null;
	photoURL?: string | null;
	uid?: string | null;
};

export type SessionState = {
	user: User | null;
};

export const session = <Writable<SessionState>>writable();

export const initializeSessionChange = () => {
	if (!browser) {
		return
	}
	onAuthStateChanged(firebaseAuth, (user) => {
		if (user) {
			console.log(`User logged in: ${user.email} from ${user.providerId}`)
			session.set({user: {
				email: user.email,
				displayName: user.displayName,
				photoURL: user.photoURL,
				uid: user.uid
			}})
		} else {
			console.log('User logged out')
			session.set({user: null})
		}
	})
}