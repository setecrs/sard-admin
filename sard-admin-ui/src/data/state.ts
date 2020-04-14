import assert from 'assert'

export interface InitialStateType {
    login: string,
    selectedUser: string,
    selectedGroup: string,
    users: string[],
    groups: string[],
    members: any,
    subscriptions: any,
    errors: any[],
    auth_token: string
}



export const initialState: InitialStateType = {
    login: '',
    selectedUser: '',
    selectedGroup: '',
    users: [],
    groups: [],
    members: {},
    subscriptions: {},
    errors: [],
    auth_token: ''
}

export function reducer(state: InitialStateType, action: any): InitialStateType {
    switch (action.type) {
        case 'select user':
            const user: string = action.payload
            assert(typeof (user) === 'string', JSON.stringify(user))
            return { ...state, selectedUser: user }
        case 'select group':
            const group: string = action.payload
            assert(typeof (group) === 'string', JSON.stringify(group))
            return { ...state, selectedGroup: group }
        case 'set users':
            const users: string[] = action.payload
            assert(Array.isArray(users), JSON.stringify(users))
            return { ...state, users }
        case 'set groups':
            const groups: string[] = action.payload
            assert(Array.isArray(groups), JSON.stringify(groups))
            return { ...state, groups }
        case 'login':
            const { login, auth_token }: { login: string, auth_token: string } = action.payload
            assert(typeof (login) === 'string', JSON.stringify(login))
            assert(typeof (auth_token) === 'string', JSON.stringify(auth_token))
            return { ...state, login, auth_token }
        case 'logout':
            return { ...state, auth_token: '', login: '' }
        case 'set members':
            return {
                ...state,
                members: {
                    ...(state.members || {}),
                    [action.payload.group]: action.payload.users
                },
            }
        case 'set subscriptions':
            return {
                ...state,
                subscriptions: {
                    ...(state.subscriptions || {}),
                    [action.payload.user]: action.payload.groups
                },
            }
        case 'error':
            const error: Error = action.payload
            return { ...state, errors: [...state.errors, error] }
        default:
            throw new Error(`unexpected action: ${action.type}`)
    }
}

