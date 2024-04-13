
const bypass_headers = new Set<string>([
    'authorization', 'referer', 'origin', 'host'
])

export let copy_some_headers = (headers: Headers) => {
    let output: Record<string, string> = {}
    headers.forEach((value, key) => {
        if (value != null && bypass_headers.has(key.toLowerCase())) {
            output[key] = value
        }
    })
    return output
}