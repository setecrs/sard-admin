export function Fetcher({baseUrl}) {
    return {
        listUsers: async () => {
            const URL = baseUrl + '/user/'
            const req = new Request(URL)
            const resp = await fetch(req)
            const j = await resp.json()
            return j.users
        },
        listGroups: async () => {
            const URL = baseUrl + '/group/'
            const req = new Request(URL)
            const resp = await fetch(req)
            const j = await resp.json()
            return j.groups
        },
        createUser: (user) => {
        },
        createGroup: (group) => {
        },
        addMember: ({group, user}) => {
        },
        listMembers: (group) => {
        },
        fixHome: (user) => {

        },
        userPermissions: (user) => {

        },
        setPassword: ({user, password}) => {

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
        addMember: ({group, user}) => {
            members[group] = [...members[group]||[], user]
        },
        listMembers: (group) => {
            return [...members[group]||[]]
        },
        fixHome: (user) => {},
        userPermissions: (user) => {},
        setPassword: ({user, password}) => {},
    }
}

export default Fetcher