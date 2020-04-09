import { MockFetcher, Fetcher } from "./fetcher"

test('fetch and MockFecher have same signatures', () => {
    const fetcher = Fetcher({ baseUrl: '' })
    const mockFetcher = MockFetcher()
    for (const fn_name in fetcher) {
        if (fetcher.hasOwnProperty(fn_name)) {
            const fn = fetcher[fn_name];
            expect(fn).toBeInstanceOf(Function)
            expect(mockFetcher).toHaveProperty(fn_name)
            const fnm = mockFetcher[fn_name];
            expect(fnm).toBeInstanceOf(Function)
            expect(fn.length).toEqual(fnm.length)
        }
    }
})

function chooseFetcher() {
    if (process.env.hasOwnProperty('REACT_APP_SARD_ADMIN_URL')) {
        // for integrations tests or development
        return Fetcher({ baseUrl: process.env.REACT_APP_SARD_ADMIN_URL })
    } else {
        return MockFetcher()
    }
}

describe('User', () => {
    test('create user', () => {
        const fetcher = chooseFetcher()
        expect(fetcher.listUsers()).toEqual([])
        fetcher.createUser('user1')
        expect(fetcher.listUsers()).toEqual(['user1'])
    })

    test('add user to group: /user/{u}/group/{g}', () => {
        const fetcher = chooseFetcher()
        fetcher.createUser('user1')
        fetcher.createGroup('g')
        expect(fetcher.listMembers('g')).toEqual([])
        fetcher.addMember({ group: 'g', user: 'user1' })
        expect(fetcher.listMembers('g')).toEqual(['user1'])
    })

    test('fix home: /user/{u}/home', () => {
        const fetcher = chooseFetcher()
        fetcher.createUser('user1')
        fetcher.fixHome('user1')
    })

    test('permissions: /user/{u}/permissions', () => {
        const fetcher = chooseFetcher()
        fetcher.createUser('user1')
        fetcher.userPermissions('user1')
    })

    test('set password: /user/{u}/reset_password', () => {
        const fetcher = chooseFetcher()
        fetcher.createUser('user1')
        fetcher.setPassword({ user: 'user1', password: 'pass' })
    })
})
