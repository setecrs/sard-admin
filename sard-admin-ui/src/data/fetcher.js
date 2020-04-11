import assert from 'assert'

export function Fetcher({ baseUrl }) {
    const helperNoJson = async (baseUrl, suffixUrl, ...args) => {
        const URL = baseUrl + suffixUrl
        const req = new Request(URL)
        const resp = await fetch(req, ...args)
        assert(resp.ok)
        return resp
    }
    const helper = async (baseUrl, suffixUrl, ...args) => {
        const resp = await helperNoJson(baseUrl, suffixUrl, ...args)
        const j = await resp.json()
        return j
    }
    return {
        listJobs: async () => {
            const j = await helper(baseUrl, '/jobs/')
            return j.jobs
        },
        listJobsHistory: async () => {
            const j = await helper(baseUrl, '/jobs/')
            return j.history
        },
        listGroups: async () => {
            const j = await helper(baseUrl, '/group/')
            return j.groups
        },
        listMembers: async (group) => {
            const j = await helper(baseUrl, `/group/${group}`)
            return j
        },
        createGroup: async (group) => {
            const URL = baseUrl + `/group/${group}`
            const req = new Request(URL)
            await fetch(req, {
                method: 'POST'
            })
        },
        groupPermissions: async (group) => {
            await helperNoJson(baseUrl, `/group/${group}/permissions`, {
                method: 'POST',
            })
        },
        listUsers: async () => {
            const j = await helper(baseUrl, '/user/')
            return j.users
        },
        listSubscriptions: async (user) => {
            const j = await helper(baseUrl, `/user/${user}`)
            return j.groups
        },
        createUser: async (user) => {
            const j = await helper(baseUrl, `/user/${user}`, {
                method: 'POST',
            })
            return j
        },
        addMember: async ({ group, user }) => {
            await helperNoJson(baseUrl, `/user/${user}/group/${group}`, {
                method: 'POST',
            })
        },
        fixHome: async (user) => {
            await helperNoJson(baseUrl, `/user/${user}/home`, {
                method: 'POST',
            })
        },
        userPermissions: async (user) => {
            await helperNoJson(baseUrl, `/user/${user}/permissions`, {
                method: 'POST',
            })
        },
        setPassword: async ({ user, password }) => {
            await helperNoJson(baseUrl, `/user/${user}/reset_password`, {
                method: 'POST',
                json: {
                    password,
                },
            })
        },
        login: async ({ user, password }) => {
            return await helper(baseUrl, `/auth/login`, {
                method: 'POST',
                json: { user, password },
            })
        },
        logout: async () => {
            await helperNoJson(baseUrl, `/auth/logout`, {
                method: 'POST',
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