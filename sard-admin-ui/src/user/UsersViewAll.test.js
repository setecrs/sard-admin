import React from 'react';
import { render } from '@testing-library/react';
import UsersViewAll from './UsersViewAll';

describe('create new user', () => {
    test('has button', () => {
        const usersViewAll = UsersViewAll({
            users: ['user1', 'user2'],
            selectedUser: '',
            setSelectedUser: () => { }
        })
        const { getByText } = render(usersViewAll);
        const btn = getByText(/Create new user/i)
        expect(btn).not.toBeNull()
    })

    test.todo('create new user: /user/{u}')
})

