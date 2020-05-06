export class UnauthorizedError extends Error {
    constructor(message?: string) {
        super(message)
        this.name = 'Unauthorized'
    }
}

interface helper {
    baseUrl: string,
    suffixUrl: string,
    auth_token?: string,
    options?: {
        headers?: Headers,
        method?: string,
        json?: any,
        body?: string,
    }
}

type Job = {
    name: string,
    running: boolean,
    start: Date,
    end: Date,
    output: string,
}

export type Worker = {
    name: string,
    pod_ip: string,
    host_ip: string,
    node_name: string,
    ready: boolean,
    image: string,
    evidence?: string,
    processed?: number,
    found?: number,
}

export type FetcherReturn = {
    listWorkers: () => Promise<Worker[]>,
    listJobs: ({ auth_token }: { auth_token: string }) =>
        Promise<{ [key: string]: Job }>,
    listJobsHistory: ({ auth_token }: { auth_token: string }) =>
        Promise<Job[]>,
    listGroups: ({ auth_token }: { auth_token: string }) =>
        Promise<{
            groups: string[]
        }>,
    listMembers: ({ group, auth_token }: { group: string, auth_token: string }) =>
        Promise<{
            group: string,
            users: string[],
        }>,
    createGroup: ({ group, auth_token }: { group: string, auth_token: string }) =>
        Promise<void>,
    groupPermissions: ({ group, auth_token }: { group: string, auth_token: string }) =>
        Promise<void>,
    listUsers: ({ auth_token }: { auth_token: string }) =>
        Promise<{
            users: string[]
        }>,
    listSubscriptions: ({ user, auth_token }: { user: string, auth_token: string }) =>
        Promise<{
            user: string,
            groups: string[],
        }>,
    createUser: ({ user, auth_token }: { user: string, auth_token: string }) =>
        Promise<{
            password: string,
        }>,
    addMember: ({ group, user, auth_token }: { group: string, user: string, auth_token: string }) =>
        Promise<void>,
    fixHome: ({ user, auth_token }: { user: string, auth_token: string }) =>
        Promise<void>,
    userPermissions: ({ user, auth_token }: { user: string, auth_token: string }) =>
        Promise<void>,
    setPassword: ({ user, password, auth_token }: { user: string, password: string, auth_token: string }) =>
        Promise<void>,
    login: ({ user, password }: { user: string, password: string }) =>
        Promise<{
            auth_token: string
        }>,
    logout: ({ auth_token }: { auth_token: string }) =>
        Promise<void>,
    folders_count: ({ imagepath }: { imagepath: string }) => Promise<number>,
    folders_rename: ({ imagepath }: { imagepath: string }) => Promise<boolean>,
}

export function Fetcher({ baseUrl }: { baseUrl: string }): FetcherReturn {
    const helperNoJson = async ({ baseUrl, suffixUrl, auth_token, options }: helper) => {
        if (auth_token) {
            options = options || {}
            if (!options.headers) {
                options.headers = new Headers()
                options.headers.set('Authorization', `Bearer ${auth_token}`)
            }
        }
        const URL = baseUrl + suffixUrl
        const req = new Request(URL)
        const resp = await fetch(req, options)
        if (resp.status === 401) {
            throw new UnauthorizedError()
        }
        if (!resp.ok) {
            const text = await resp.text()
            throw new Error(text)
        }
        return resp
    }
    const helper = async ({ baseUrl, suffixUrl, auth_token, options }: helper) => {
        const resp = await helperNoJson({ baseUrl, suffixUrl, auth_token, options })
        if (resp.status === 401) {
            throw new UnauthorizedError()
        }
        if (!resp.ok) {
            const text = await resp.text()
            throw new Error(text)
        }
        const j = await resp.json()
        return j
    }
    return {
        listWorkers: async () => {
            const j = await helper({ baseUrl, suffixUrl: '/workers/' })
            return j
        },
        listJobs: async ({ auth_token }: { auth_token: string }) => {
            const j = await helper({ baseUrl, auth_token, suffixUrl: '/jobs/' })
            return j.jobs
        },
        listJobsHistory: async ({ auth_token }: { auth_token: string }) => {
            const j = await helper({ baseUrl, auth_token, suffixUrl: '/jobs/' })
            return j.history
        },
        listGroups: async ({ auth_token }: { auth_token: string }) => {
            const { groups }: { groups: string[] } = await helper({ baseUrl, auth_token, suffixUrl: '/group/' })
            return { groups }
        },
        listMembers: async ({ group, auth_token }: { group: string, auth_token: string }) => {
            const j = await helper({ baseUrl, auth_token, suffixUrl: `/group/${group}` })
            return j
        },
        createGroup: async ({ group, auth_token }) => {
            await helperNoJson({
                baseUrl, auth_token, suffixUrl: `/group/${group}`, options: {
                    method: 'POST',
                }
            })
        },
        groupPermissions: async ({ group, auth_token }) => {
            await helperNoJson({
                baseUrl, auth_token, suffixUrl: `/group/${group}/permissions`, options: {
                    method: 'POST',
                }
            })
        },
        listUsers: async ({ auth_token }) => {
            const j = await helper({ baseUrl, auth_token, suffixUrl: '/user/' })
            return j
        },
        listSubscriptions: async ({ user, auth_token }) => {
            const j = await helper({ baseUrl, auth_token, suffixUrl: `/user/${user}` })
            return j
        },
        createUser: async ({ user, auth_token }) => {
            const j = await helper({
                baseUrl, auth_token, suffixUrl: `/user/${user}`, options: {
                    method: 'POST',
                }
            })
            return j
        },
        addMember: async ({ group, user, auth_token }) => {
            await helperNoJson({
                baseUrl, auth_token, suffixUrl: `/user/${user}/group/${group}`, options: {
                    method: 'POST',
                }
            })
        },
        fixHome: async ({ user, auth_token }) => {
            await helperNoJson({
                baseUrl, auth_token, suffixUrl: `/user/${user}/home`, options: {
                    method: 'POST',
                }
            })
        },
        userPermissions: async ({ user, auth_token }) => {
            await helperNoJson({
                baseUrl, auth_token, suffixUrl: `/user/${user}/permissions`, options: {
                    method: 'POST',
                }
            })
        },
        setPassword: async ({ user, password, auth_token }) => {
            await helperNoJson({
                baseUrl, auth_token, suffixUrl: `/user/${user}/reset_password`, options: {
                    method: 'POST',
                    json: {
                        password,
                    },
                }
            })
        },
        login: async ({ user, password }) => {
            const { auth_token } = await helper({
                baseUrl, suffixUrl: `/auth/login`, options: {
                    method: 'POST',
                    headers: new Headers({ 'Content-Type': 'application/json' }),
                    body: JSON.stringify({ user, password }),
                }
            })
            return { auth_token }
        },
        logout: async ({ auth_token }) => {
            await helperNoJson({
                baseUrl, auth_token, suffixUrl: `/auth/logout`, options: {
                    method: 'POST',
                }
            })
        },
        folders_count: async ({ imagepath }) => {
            const j = await helper({
                baseUrl, auth_token: undefined, suffixUrl: `/folders/count`, options: {
                    method: 'POST',
                    headers: new Headers({ 'Content-Type': 'application/json' }),
                    body: JSON.stringify({ imagepath }),
                }
            })
            return j.result
        },
        folders_rename: async ({ imagepath }) => {
            const j = await helper({
                baseUrl, auth_token: undefined, suffixUrl: `/folders/rename`, options: {
                    method: 'POST',
                    headers: new Headers({ 'Content-Type': 'application/json' }),
                    body: JSON.stringify({ imagepath }),
                }
            })
            return j.result
        }
    }
}

export function MockFetcher(): FetcherReturn {
    const users: string[] = ['u1', 'u2']
    const groups: string[] = ['g1', 'g2', 'g3']
    const members: { [key: string]: string[] } = { g1: ['u1', 'u2'], g2: ['u2'] }
    const subscriptions: { [key: string]: string[] } = { u1: ['g1'], u2: ['g1', 'g2'] }
    const jobs: { [key: string]: Job } = {}
    const jobsHistory: Job[] = []
    const workers: Worker[] = [
        {
            host_ip: '1.2.3.4',
            pod_ip: '5.6.7.8',
            image: 'asfd/worker:1234',
            name: 'ipedworker-298347',
            node_name: 'sardcloudXX',
            ready: false,
            evidence: '/ops/A/B/imagem.dd',
            processed: 91084.0,
            found: 92494.0,
        },
        {
            host_ip: '1.2.3.5',
            pod_ip: '5.6.7.9',
            image: 'asfd/worker:987',
            name: 'ipedworker-oiewur',
            node_name: 'sardcloudYY',
            ready: false,
            evidence: '/operacoes/ipl_180001/item01-M190005/item01-M190005.dd',
            processed: 1000.0,
            found: 4000.0,
        },
        {
            host_ip: '1.2.3.6',
            pod_ip: '5.6.7.10',
            image: 'asfd/worker:987',
            name: 'ipedworker-obir',
            node_name: 'sardcloudZZ',
            ready: true,
        },
    ]
    let restart_counter = 0
    return {
        listWorkers: async () => workers,
        listJobs: async () => jobs,
        listJobsHistory: async () => jobsHistory,
        listUsers: async () => {
            return { users: [...users] }
        },
        listGroups: async () => {
            return { groups: [...groups] }
        },
        createUser: async ({ user }) => {
            users.push(user)
            return { password: user }
        },
        createGroup: async ({ group }) => {
            groups.push(group)
        },
        addMember: async ({ group, user }) => {
            members[group] = [...(members[group] || []), user]
            subscriptions[user] = [...(subscriptions[user] || []), group]
        },
        listMembers: async ({ group }) => {
            return {
                group,
                users: [...(members[group] || [])]
            }
        },
        fixHome: async () => { },
        userPermissions: async () => { },
        groupPermissions: async () => { },
        setPassword: async () => { },
        listSubscriptions: async ({ user }) => {
            return {
                user,
                groups: [...(subscriptions[user] || [])]
            }
        },
        login: async ({ user }) => ({
            auth_token: user,
        }),
        logout: async () => { },
        folders_count: async () => restart_counter,
        folders_rename: async () => {
            restart_counter++
            return restart_counter % 2 == 0
        }
    }
}

export default Fetcher