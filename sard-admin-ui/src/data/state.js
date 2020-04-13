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
    subscriptions: {},
    errors: [],
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
            const subscriptions = {}
            for (const user in state.subscriptions) {
                subscriptions[user] = state.subscriptions[user].filter(g => g !== action.payload.group)
            }
            for (const user of action.payload.users) {
                subscriptions[user] = [...(subscriptions[user] || []), action.payload.group]
            }
            return {
                ...state,
                members: {
                    ...state.members,
                    [action.payload.group]: action.payload.users
                },
                subscriptions,
            }
        case 'error':
            return { ...state, errors: [...state.errors, action.payload] }
        default:
            throw new Error(`unexpected action: ${action.type}`)
    }
}

export function Actions({ fetcher, dispatch }) {
    return {
        selectUser: (user) => {
            dispatch({ type: 'select user', payload: user })
        },
        selectGroup: (group) => {
            dispatch({ type: 'select group', payload: group })
        },
        listUsers: async ({ auth_token }) => {
            try {
                const users = await fetcher.listUsers({ auth_token })
                dispatch({ type: 'set users', payload: users })
            } catch (e) {
                dispatch({ type: 'error', payload: e })
            }
        },
        listGroups: async ({ auth_token }) => {
            try {
                const groups = await fetcher.listGroups({ auth_token })
                dispatch({ type: 'set groups', payload: groups })
            } catch (e) {
                dispatch({ type: 'error', payload: e })
            }
        },
        createUser: async ({ user, auth_token }) => {
            try {
                await fetcher.createUser({ user, auth_token })
                const users = await fetcher.listUsers({ auth_token })
                dispatch({ type: 'set users', payload: users })
                dispatch({ type: 'select user', payload: user })
            } catch (e) {
                dispatch({ type: 'error', payload: e })
            }
        },
        createGroup: async ({ group, auth_token }) => {
            try {
                await fetcher.createGroup({ group, auth_token })
                const groups = await fetcher.listGroups({ auth_token })
                dispatch({ type: 'set groups', payload: groups })
                dispatch({ type: 'select group', payload: group })
            } catch (e) {
                dispatch({ type: 'error', payload: e })
            }
        },
        addMember: async ({ group, user, auth_token }) => {
            try {
                await fetcher.addMember({ group, user, auth_token })
                const users = await fetcher.listMembers({ group, auth_token })
                dispatch({ type: 'set members', payload: { group, users } })
            } catch (e) {
                dispatch({ type: 'error', payload: e })
            }
        },
        listMembers: async ({ group, auth_token }) => {
            try {
                const users = await fetcher.listMembers({ group, auth_token })
                dispatch({ type: 'set members', payload: { group, users } })
            } catch (e) {
                dispatch({ type: 'error', payload: e })
            }
        },
        fixHome: async ({ user, auth_token }) => {
            try {
                await fetcher.fixHome({ user, auth_token })
            } catch (e) {
                dispatch({ type: 'error', payload: e })
            }
        },
        userPermissions: async ({ user, auth_token }) => {
            try {
                await fetcher.userPermissions({ user, auth_token })
            } catch (e) {
                dispatch({ type: 'error', payload: e })
            }
        },
        setPassword: async ({ user, password, auth_token }) => {
            try {
                await fetcher.setPassword({ user, password, auth_token })
            } catch (e) {
                dispatch({ type: 'error', payload: e })
            }
        },
        login: async ({ user, password }) => {
            try {
                const resp = await fetcher.login({ user, password })
                fetcher.auth_token = resp.auth_token
                dispatch({ type: 'login', payload: resp })
            } catch (e) {
                dispatch({ type: 'error', payload: e })
            }
        },
        logout: async ({ auth_token }) => {
            try {
                await fetcher.logout({ auth_token })
                fetcher.auth_token = ''
                dispatch({ type: 'logout' })
            } catch (e) {
                dispatch({ type: 'error', payload: e })
            }
        },
    }
}
