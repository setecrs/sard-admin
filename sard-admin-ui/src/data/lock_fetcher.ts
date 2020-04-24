export type LockFetcherType = {
    getLocks: () => Promise<string[]>
}

export function LockFetcher({ lockURL }:{ lockURL:string }): LockFetcherType {
    return {
        getLocks: async () => {
            const resp = await fetch(lockURL)
            return getLocksCore(resp)
        }
    }
}

export function MockLockFetcher(): ReturnType<typeof LockFetcher> {
    return {
        getLocks: async () => {
            return [
                "/operacoes/ipl_180001/item01-M190005/item01-M190005.dd",
                "/operacoes/ipl_180001/item01-M190005/item01-M190008.dd",
            ]
        }
    }
}

export async function getLocksCore(resp: Response) {
    if (!resp.ok) {
        const text = await resp.text()
        throw new Error(text)
    }
    const text = await resp.text()
    const lines = text.split('\n')
    return lines.map(x => x.split(' ')[0]).filter(x => !!x)
}