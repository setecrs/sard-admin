import { MockFetcher, Fetcher } from "./fetcher"

function chooseFetcher() {
    if (process.env.hasOwnProperty('REACT_APP_SARD_ADMIN_URL')) {
        // for integrations tests or development
        return Fetcher({ baseUrl: process.env.REACT_APP_SARD_ADMIN_URL||'' })
    } else {
        return MockFetcher()
    }
}

describe('User', () => {
    test('create user', async () => {
        const fetcher = chooseFetcher()
        expect(await fetcher.listUsers({ auth_token: '' })).toEqual({ users: [] })
        fetcher.createUser({ user: 'user1', auth_token: '' })
        expect(await fetcher.listUsers({ auth_token: '' })).toEqual({ users: ['user1'] })
    })

    test('add user to group: /user/{u}/group/{g}', async () => {
        const fetcher = chooseFetcher()
        await fetcher.createUser({ user: 'user1', auth_token: '' })
        await fetcher.createGroup({ group: 'g', auth_token: '' })
        expect(await fetcher.listMembers({ group: 'g', auth_token: '' })).toEqual({ group: 'g', users: [] })
        await fetcher.addMember({ group: 'g', user: 'user1', auth_token: '' })
        expect(await fetcher.listMembers({ group: 'g', auth_token: '' })).toEqual({ group: 'g', users: ['user1'] })
    })

    test('fix home: /user/{u}/home', async () => {
        const fetcher = chooseFetcher()
        await fetcher.createUser({ user: 'user1', auth_token: '' })
        await fetcher.fixHome({ user: 'user1', auth_token: '' })
    })

    test('permissions: /user/{u}/permissions', async () => {
        const fetcher = chooseFetcher()
        await fetcher.createUser({ user: 'user1', auth_token: '' })
        await fetcher.userPermissions({ user: 'user1', auth_token: '' })
    })

    test('set password: /user/{u}/reset_password', async () => {
        const fetcher = chooseFetcher()
        await fetcher.createUser({ user: 'user1', auth_token: '' })
        await fetcher.setPassword({ user: 'user1', password: 'pass' , auth_token: ''})
    })
})
