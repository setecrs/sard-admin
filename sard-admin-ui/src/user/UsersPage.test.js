import React from 'react';
import { render } from '@testing-library/react';
import { UsersPage } from './UsersPage';

describe('create new user', () => {
    test('has button', () => {
        const usersPage = UsersPage({
            users: ['user1', 'user2'],
            selectedUser: '',
            setSelectedUser: () => { },
            createUser: () => {}, 
            fixHome: () => {},
            addMember: () => {},
            groups:[],
            subscriptions:{},
        })
        const { getByText } = render(usersPage);
        const btn = getByText(/Create new user/i)
        expect(btn).not.toBeNull()
    })

    test.todo('create new user: /user/{u}')
})

