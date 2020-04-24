import { getLocksCore } from './lock_fetcher'

describe('locker', () => {
    it('returns [] with empty response', async () => {
        const got = await getLocksCore(new Response(' \n    '))
        expect(got).toHaveLength(0)
    })
    it('returns results', async () => {
        const got = await getLocksCore(new Response(' leading space \nokresult  extra  '))
        expect(got).toHaveLength(1)
        expect(got[0]).toEqual('okresult')
    })
})