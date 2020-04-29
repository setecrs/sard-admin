import React from 'react'
import { render, fireEvent } from '@testing-library/react'
import { UserDetails } from './UserDetails'

describe('list my groups: /user/{u}', () => {
    test('show list of groups', async () => {
        const userDetails = <UserDetails
            addMember={async () => { }}
            allGroups={['notmine']}
            fixHome={async () => { }}
            fixPermissions={async () => { }}
            listSubscriptions={async () => { }}
            mygroups={['mine']}
            user='user'
            key='myid'
        />
        const { getAllByRole } = render(userDetails)
        const options = getAllByRole('option')
        expect(options).toHaveLength(2)
        expect(options[0].textContent).toBe('')
        expect(options[1].textContent).toBe('notmine')
        const li = getAllByRole('listitem')
        expect(li).toHaveLength(1)
        expect(li[0].textContent).toBe('mine')
    })
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
        mygroups={['mine']}
        user='user'
        key='myid'
    />
    const { getByRole } = render(userDetails)
    const select = getByRole('combobox')
    fireEvent.change(select, { target: { value: 'notmine' } })
    fireEvent.click(getByRole('button', { name: /add group/i }))
    expect(called).toBe(1)
    expect(called_user).toBe('user')
    expect(called_group).toBe('notmine')
    fireEvent.click(getByRole('button', { name: /add group/i }))
    expect(called).toBe(2)
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
        mygroups={['mine']}
        user='user'
        key='myid'
    />
    const { getByRole } = render(userDetails)
    fireEvent.click(getByRole('button', { name: /fill home directory/i }))
    expect(called).toBe(1)
    expect(called_user).toBe('user')
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
        mygroups={['mine']}
        user='user'
        key='myid'
    />
    const { getByRole } = render(userDetails)
    fireEvent.click(getByRole('button', { name: /fix home directory permissions/i }))
    expect(called).toBe(1)
    expect(called_user).toBe('user')
})
test.skip('set password: /user/{u}/reset_password', async () => {
    const userDetails = <UserDetails
        addMember={async () => { }}
        allGroups={['notmine']}
        fixHome={async () => { }}
        fixPermissions={async () => { }}
        listSubscriptions={async () => { }}
        mygroups={['mine']}
        user='user'
        key='myid'
    />
    const { getByRole } = render(userDetails)

    expect(getByRole('button', { name: /change password/i })).toBeDefined()
})
