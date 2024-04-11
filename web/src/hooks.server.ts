import {redirect} from "@sveltejs/kit";
import {jwtDecode} from "jwt-decode";

export async function handle({event, resolve}) {
    let {cookies, request, route, locals} = event
    const token = cookies.get('token')

    console.debug("Incoming request", route)
    if ((route && !route?.id?.startsWith('/login')) && !token) {
        console.debug("Redirect to login")
        return redirect(302, '/login')
    }
    if (token) {
        const user = jwtDecode(token)
        // @ts-ignore
        locals.user = user
        console.debug('Found user:', user)
    }
    return await resolve(event);
}
