import { MockFetcher, Fetcher } from "./fetcher"

function chooseFetcher() {
    if (process.env.hasOwnProperty('REACT_APP_SARD_ADMIN_URL')) {
        // for integrations tests or development
        return Fetcher({ baseUrl: process.env.REACT_APP_SARD_ADMIN_URL || '' })
    } else {
        return MockFetcher()
    }
}

describe('User', () => {
    test('create user', async () => {
        const fetcher = chooseFetcher()
        fetcher.createUser({ user: 'someuser', auth_token: '' })
        const { users } = await fetcher.listUsers({ auth_token: '' })
        expect(users).toContain('someuser')
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
        await fetcher.setPassword({ user: 'user1', password: 'pass', auth_token: '' })
    })

    test('list workers: /workers/', async () => {
        const fetcher = chooseFetcher()
        const workers = await fetcher.listWorkers()
        workers.forEach(w => {
            expect(w).toHaveProperty('host_ip')
            expect(w).toHaveProperty('pod_ip')
            expect(w).toHaveProperty('image')
            expect(w).toHaveProperty('name')
            expect(w).toHaveProperty('node_name')
            expect(w).toHaveProperty('ready')
            expect(typeof w.host_ip).toBe('string')
            expect(typeof w.pod_ip).toBe('string')
            expect(typeof w.image).toBe('string')
            expect(typeof w.name).toBe('string')
            expect(typeof w.node_name).toBe('string')
            expect(typeof w.ready).toBe('boolean')
            if (w.evidence) {
                expect(typeof w.evidence).toBe('string')
            }
            if (w.processed) {
                expect(typeof w.processed).toBe('number')
            }
            if (w.found) {
                expect(typeof w.found).toBe('number')
            }
        })
    })
})
