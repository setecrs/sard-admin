import { render } from '@testing-library/react'
import User from './User'
describe('list my groups: /user/{u}', () => {
    test.skip('show list of groups', () => {
        const userView = User()
        const { getByTestId } = render(userView)
        const groupList = getByTestId('mygroups')
        
    })
})
test.todo('add user to group: /user/{u}/group/{g}')
test.todo('fix home: /user/{u}/home')
test.todo('permissions: /user/{u}/permissions')
test.todo('set password: /user/{u}/reset_password')
