import React from 'react'
import { render, fireEvent, wait } from '@testing-library/react'
import { UserDetails } from './UserDetails'

test('list my groups: /user/{u}', async () => {
    const userDetails2 = <UserDetails
        addMember={async () => { }}
        allGroups={['notmine']}
        fixHome={async () => { }}
        fixPermissions={async () => { }}
        listSubscriptions={async () => { }}
        setPassword={async () => { }}
        mygroups={['mine']}
        user='user'
        key='myid'
    />
    const { baseElement, getAllByRole } = render(userDetails2)
    await wait(() => {
        expect(baseElement).toBeDefined()
    })
    const options = getAllByRole('option')
    expect(options).toHaveLength(2)
    expect(options[0].textContent).toBe('')
    expect(options[1].textContent).toBe('notmine')
    const li = getAllByRole('listitem')
    expect(li).toHaveLength(1)
    expect(li[0].textContent).toBe('mine')
})

test('add user to group: /user/{u}/group/{g}', async () => {
    let called = 0
    let called_user = ''
    let called_group = ''
    const userDetails = <UserDetails
        addMember={async ({ user, group }) => {
            called_user = user
            called_group = group
            called++
        }}
        allGroups={['notmine']}
        fixHome={async () => { }}
        fixPermissions={async () => { }}
        listSubscriptions={async () => { }}
        setPassword={async () => { }}
        mygroups={['mine']}
        user='user'
        key='myid'
    />
    const { getByRole } = render(userDetails)
    await wait(() => {
        const select = getByRole('combobox')
        fireEvent.change(select, { target: { value: 'notmine' } })
        fireEvent.click(getByRole('button', { name: /add group/i }))
        expect(called).toBe(1)
        expect(called_user).toBe('user')
        expect(called_group).toBe('notmine')
        fireEvent.click(getByRole('button', { name: /add group/i }))
        expect(called).toBe(2)
    })
})

test('fix home: /user/{u}/home', async () => {
    let called = 0
    let called_user = ''
    const userDetails = <UserDetails
        addMember={async () => { }}
        allGroups={['notmine']}
        fixHome={async ({ user }) => {
            called_user = user
            called++
        }}
        fixPermissions={async () => { }}
        listSubscriptions={async () => { }}
        setPassword={async () => { }}
        mygroups={['mine']}
        user='user'
        key='myid'
    />
    const { getByRole } = render(userDetails)
    await wait(() => {
        fireEvent.click(getByRole('button', { name: /fill home directory/i }))
        expect(called).toBe(1)
        expect(called_user).toBe('user')
    })
})

test('permissions: /user/{u}/permissions', async () => {
    let called = 0
    let called_user = ''
    const userDetails = <UserDetails
        addMember={async () => { }}
        allGroups={['notmine']}
        fixHome={async () => { }}
        fixPermissions={async ({ user }) => {
            called_user = user
            called++
        }}
        listSubscriptions={async () => { }}
        setPassword={async () => { }}
        mygroups={['mine']}
        user='user'
        key='myid'
    />
    const { getByRole } = render(userDetails)
    await wait(() => {
        fireEvent.click(getByRole('button', { name: /fix home directory permissions/i }))
        expect(called).toBe(1)
        expect(called_user).toBe('user')
    })
})
describe('set password: /user/{u}/reset_password', () => {
    let _user = ''
    let _password = ''
    let called = 0
    const spyPassword = async ({ user, password }: { user: string, password: string }) => {
        _user = user
        _password = password
        called++
    }
    const userDetails = <UserDetails
        addMember={async () => { }}
        allGroups={[]}
        fixHome={async () => { }}
        fixPermissions={async () => { }}
        listSubscriptions={async () => { }}
        mygroups={[]}
        user='user'
        key='myid'
        setPassword={spyPassword}
    />
    test('it renders', async () => {
        const { baseElement, getByRole, getByPlaceholderText } = render(userDetails)
        await wait(() => {
            expect(baseElement).toBeDefined()
        })
        const field1 = getByPlaceholderText('Password')
        const field2 = getByPlaceholderText(/retype password/i)
        const btn = getByRole('button', { name: /set password/i })
        expect(field1).toBeDefined()
        expect(field2).toBeDefined()
        expect(btn).toBeDefined()
        expect(_user).toBe('')
        expect(_password).toBe('')
    })
    test('fill field1, nothing changes', async () => {
        const { baseElement, getByPlaceholderText } = render(userDetails)
        await wait(() => {
            expect(baseElement).toBeDefined()
        })
        const field1 = getByPlaceholderText('Password')
        const field2 = getByPlaceholderText(/retype password/i)
        fireEvent.change(field1, { target: { value: 1234 } })
        fireEvent.change(field2, { target: { value: '' } })
        expect(_user).toBe('')
        expect(_password).toBe('')
    })
    test('fill field2, nothing changes', async () => {
        const { baseElement, getByPlaceholderText } = render(userDetails)
        await wait(() => {
            expect(baseElement).toBeDefined()
        })
        const field1 = getByPlaceholderText('Password')
        const field2 = getByPlaceholderText(/retype password/i)
        fireEvent.change(field1, { target: { value: '' } })
        fireEvent.change(field2, { target: { value: 1234 } })
        expect(_user).toBe('')
        expect(_password).toBe('')
    })
    test('press button, nothing changes', async () => {
        const { baseElement, getByRole, getByPlaceholderText } = render(userDetails)
        await wait(() => {
            expect(baseElement).toBeDefined()
        })
        const field1 = getByPlaceholderText('Password')
        const field2 = getByPlaceholderText(/retype password/i)
        const btn = getByRole('button', { name: /set password/i })
        fireEvent.change(field1, { target: { value: '' } })
        fireEvent.change(field2, { target: { value: '' } })
        fireEvent.click(btn)
        expect(_user).toBe('')
        expect(_password).toBe('')
    })
    test('press button, set password', async () => {
        const { baseElement, getByRole, getByPlaceholderText } = render(userDetails)
        await wait(() => {
            expect(baseElement).toBeDefined()
        })
        const field1 = getByPlaceholderText('Password')
        const field2 = getByPlaceholderText(/retype password/i)
        const btn = getByRole('button', { name: /set password/i })
        fireEvent.change(field1, { target: { value: 1234 } })
        fireEvent.change(field2, { target: { value: 1234 } })
        fireEvent.click(btn)
        expect(called).toBe(1)
        await wait(() => {
            expect(_password).toBe('1234')
            expect(_user).toBe('user')
        })
    })
})
