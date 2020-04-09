export const initialState = {
    login: {
        user: null,
        token: null,
    },
    selectedUser: '',
    selectedGroup: '',
    users: [],
    groups: [],
    members: {},
    error: '',
}

export function reducer(state, action) {
    switch (action.type) {
        case 'select user':
            return { ...state, selectedUser: action.payload }
        case 'select group':
            return { ...state, selectedGroup: action.payload }
        case 'set users':
            return { ...state, users: action.payload }
        case 'set groups':
            return { ...state, groups: action.payload }
        case 'login':
            return { ...state, login: action.payload }
        case 'logout':
            return { ...state, logout: { user: null, token: null } }
        case 'set members':
            return {
                ...state,
                members: {
                    ...state.members,
                    [action.payload.group]: action.payload.users
                }
            }
        case 'error':
            return { ...state, error: action.payload }
        default:
            throw new Error(`unexpected action: ${action.type}`)
    }
}

export function Actions({ fetcher, dispatch }) {
    return {
        selectUser: (user) => {
            dispatch({ type: 'select user', payload: user })
        },
        listUsers: async () => {
            const users = await fetcher.listUsers()
            dispatch({ type: 'set users', payload: users })
        },
        listGroups: async () => {
            const groups = await fetcher.listGroups()
            dispatch({ type: 'set groups', payload: groups })
        },
        createUser: async (user) => {
            await fetcher.createUser(user)
            const users = await fetcher.listUsers()
            dispatch({ type: 'set users', payload: users })
            dispatch({ type: 'select user', payload: user })
        },
        createGroup: async (group) => {
            await fetcher.createGroup(group)
            const groups = await fetcher.listGroups()
            dispatch({ type: 'set groups', payload: groups })
            dispatch({ type: 'select group', payload: group })
        },
        addMember: async ({ group, user }) => {
            await fetcher.addMember({ group, user })
            const users = await fetcher.listMembers(group)
            dispatch({ type: 'set members', payload: { group, users } })
        },
        listMembers: async (group) => {
            const users = await fetcher.listMembers(group)
            dispatch({ type: 'set members', payload: { group, users } })
        },
        fixHome: async (user) => {
            await fetcher.fixHome(user)
        },
        userPermissions: async (user) => {
            await fetcher.userPermissions(user)
        },
        setPassword: async ({ user, password }) => {
            await fetcher.setPassword({ user, password })
        },
    }
}
