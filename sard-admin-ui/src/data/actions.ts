import { FetcherReturn } from "./fetcher"

export function Actions({ fetcher, dispatch }: { fetcher: FetcherReturn, dispatch: ({ type, payload }: { type: string, payload?: any }) => void }) {
    return {
        selectUser: (user: string) => {
            dispatch({ type: 'select user', payload: user })
        },
        selectGroup: (group: string) => {
            dispatch({ type: 'select group', payload: group })
        },
        listUsers: async ({ auth_token }: { auth_token: string }) => {
            try {
                const { users } = await fetcher.listUsers({ auth_token })
                dispatch({ type: 'set users', payload: users })
            } catch (e) {
                console.error(e)
                dispatch({ type: 'error', payload: e })
            }
        },
        listGroups: async ({ auth_token }: { auth_token: string }) => {
            try {
                const { groups } = await fetcher.listGroups({ auth_token })
                dispatch({ type: 'set groups', payload: groups })
            } catch (e) {
                console.error(e)
                dispatch({ type: 'error', payload: e })
            }
        },
        createUser: async ({ user, auth_token }: { user: string, auth_token: string }) => {
            try {
                await fetcher.createUser({ user, auth_token })
                const { users } = await fetcher.listUsers({ auth_token })
                dispatch({ type: 'set users', payload: users })
                dispatch({ type: 'select user', payload: user })
            } catch (e) {
                console.error(e)
                dispatch({ type: 'error', payload: e })
            }
        },
        createGroup: async ({ group, auth_token }: { group: string, auth_token: string }) => {
            try {
                await fetcher.createGroup({ group, auth_token })
                const { groups } = await fetcher.listGroups({ auth_token })
                dispatch({ type: 'set groups', payload: groups })
                dispatch({ type: 'select group', payload: group })
            } catch (e) {
                console.error(e)
                dispatch({ type: 'error', payload: e })
            }
        },
        addMember: async ({ group, user, auth_token }: { user: string, group: string, auth_token: string }) => {
            try {
                await fetcher.addMember({ group, user, auth_token })
                const lm = fetcher.listMembers({ group, auth_token })
                const ls = fetcher.listSubscriptions({ user, auth_token })
                const payload_lm = await lm
                dispatch({ type: 'set members', payload: payload_lm, })
                const payload_ls = await ls
                dispatch({ type: 'set subscriptions', payload: payload_ls, })
            } catch (e) {
                console.error(e)
                dispatch({ type: 'error', payload: e })
            }
        },
        iped: async (params: Parameters<FetcherReturn["iped"]>[0]) => {
            try {
                await fetcher.iped(params)
            } catch (e) {
                console.error(e)
                dispatch({ type: 'error', payload: e })
            }
        },
        listMembers: async ({ group, auth_token }: { group: string, auth_token: string }) => {
            try {
                const payload = await fetcher.listMembers({ group, auth_token })
                dispatch({ type: 'set members', payload })
            } catch (e) {
                console.error(e)
                dispatch({ type: 'error', payload: e })
            }
        },
        listSubscriptions: async ({ user, auth_token }: { user: string, auth_token: string }) => {
            try {
                const payload = await fetcher.listSubscriptions({ user, auth_token })
                dispatch({ type: 'set subscriptions', payload })
            } catch (e) {
                console.error(e)
                dispatch({ type: 'error', payload: e })
            }
        },
        fixHome: async ({ user, auth_token }: { user: string, auth_token: string }) => {
            try {
                await fetcher.fixHome({ user, auth_token })
            } catch (e) {
                console.error(e)
                dispatch({ type: 'error', payload: e })
            }
        },
        userPermissions: async ({ user, auth_token }: { user: string, auth_token: string }) => {
            try {
                await fetcher.userPermissions({ user, auth_token })
            } catch (e) {
                console.error(e)
                dispatch({ type: 'error', payload: e })
            }
        },
        groupPermissions: async ({ group, auth_token }: { group: string, auth_token: string }) => {
            try {
                await fetcher.groupPermissions({ group, auth_token })
            } catch (e) {
                console.error(e)
                dispatch({ type: 'error', payload: e })
            }
        },
        setPassword: async ({ user, password, auth_token }: { user: string, password: string, auth_token: string }) => {
            try {
                await fetcher.setPassword({ user, password, auth_token })
            } catch (e) {
                console.error(e)
                dispatch({ type: 'error', payload: e })
            }
        },
        login: async ({ user, password }: { user: string, password: string }) => {
            try {
                const { auth_token } = await fetcher.login({ user, password })
                dispatch({
                    type: 'login', payload: {
                        login: user,
                        auth_token,
                    }
                })
            } catch (e) {
                console.error(e)
                dispatch({ type: 'error', payload: e })
            }
        },
        logout: async ({ auth_token }: { auth_token: string }) => {
            try {
                await fetcher.logout({ auth_token })
                dispatch({ type: 'logout' })
            } catch (e) {
                console.error(e)
                dispatch({ type: 'error', payload: e })
            }
        },
    }
}
