import {redirect} from "@sveltejs/kit";
import {jwtDecode} from "jwt-decode";

export async function handle({event, resolve}) {
    let {cookies, request, route, locals} = event
    const token = cookies.get('token')

    if ((route && !route?.id?.startsWith('/login')) && !token) {
        return redirect(302, '/login')
    }
    if (token) {
        const user = jwtDecode(token)
        // @ts-ignore
        locals.user = user
    }
    event.request.headers.set('authorization', 'bearer ' + token)
    return await resolve(event);
}
