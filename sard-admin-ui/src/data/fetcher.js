export class UnauthorizedError extends Error {
    constructor(message) {
        super(message)
        this.name = 'Unauthorized'
    }
}

export function Fetcher({ baseUrl }) {
    const helperNoJson = async ({ baseUrl, suffixUrl, auth_token, options }) => {
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
    const helper = async ({ baseUrl, suffixUrl, auth_token, headers }) => {
        const resp = await helperNoJson({ baseUrl, suffixUrl, auth_token, headers })
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
        auth_token: '',
        listJobs: async ({ auth_token }) => {
            const j = await helper({ baseUrl, auth_token, suffixUrl: '/jobs/' })
            return j.jobs
        },
        listJobsHistory: async ({ auth_token }) => {
            const j = await helper({ baseUrl, auth_token, suffixUrl: '/jobs/' })
            return j.history
        },
        listGroups: async ({ auth_token }) => {
            const j = await helper({ baseUrl, auth_token, suffixUrl: '/group/' })
            return j.groups
        },
        listMembers: async ({ group, auth_token }) => {
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
            return j.users
        },
        listSubscriptions: async ({ user, auth_token }) => {
            const j = await helper({ baseUrl, auth_token, suffixUrl: `/user/${user}` })
            return j.groups
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
            return await helper({
                baseUrl, suffixUrl: `/auth/login`, options: {
                    method: 'POST',
                    json: { user, password },
                }
            })
        },
        logout: async ({ auth_token }) => {
            await helperNoJson({
                baseUrl, auth_token, suffixUrl: `/auth/logout`, options: {
                    method: 'POST',
                }
            })
        },
    }
}

export function MockFetcher() {
    const users = []
    const groups = []
    const members = {}
    return {
        listUsers: () => {
            return [...users]
        },
        listGroups: () => {
            return [...groups]
        },
        createUser: (user) => {
            users.push(user)
        },
        createGroup: (group) => {
            groups.push(group)
        },
        addMember: ({ group, user }) => {
            members[group] = [...(members[group] || []), user]
        },
        listMembers: (group) => {
            return [...(members[group] || [])]
        },
        listJobs: () => ([]),
        listJobsHistory: () => ([]),
        fixHome: (user) => { },
        userPermissions: (user) => { },
        groupPermissions: (user) => { },
        setPassword: ({ user, password }) => { },
    }
}

export default Fetcher