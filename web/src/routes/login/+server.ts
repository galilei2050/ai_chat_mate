import {redirect, type  RequestHandler} from '@sveltejs/kit'
import {dev} from '$app/environment'


export const POST: RequestHandler = async ({request, cookies}) => {
    const data: { accessToken: string } = await request.json()
    cookies.set(
        "token",
        data.accessToken,
        {
            httpOnly: !dev,
            secure: !dev,
            sameSite: dev ? "lax" : "none",
            path: '/'
        }
    )

    throw redirect(302, '/')
}