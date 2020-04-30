import React from 'react';
import { render, wait } from '@testing-library/react';
import { UsersPage } from './UsersPage';

describe('create new user', () => {
    test('has button', async () => {
        const usersPage = <UsersPage
            users={['user1', 'user2']}
            allGroups={[]}
            myGroups={[]}
            selectedUser={''}
            setSelectedUser={() => { }}
            createUser={async () => { }}
            fixHome={async () => { }}
            fixPermissions={async () => { }}
            addMember={async () => { }}
            listSubscriptions={async () => { }}
        />
        const { getByText } = render(usersPage);
        await wait(() => {
            const btn = getByText(/Create new user/i)
            expect(btn).not.toBeNull()
        })
    })
})

