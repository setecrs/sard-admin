import React from 'react'
import { render, fireEvent } from '@testing-library/react';
import { UsersList } from './UsersList';


test('UserList renders', () => {
    const userList = <UsersList
        users={[]}
        selectedUser={'user1'}
        setSelectedUser={async () => { }}
    />
    const { baseElement } = render(userList);
    expect(baseElement).not.toBeNull()
});

test('UserList has 2 users, sorted', () => {
    const userList = <UsersList
        users={['user2', 'user1']}
        selectedUser={'user1'}
        setSelectedUser={async () => { }}
    />
    const { baseElement } = render(userList);
    const ul = baseElement.querySelector('#user_list')
    expect(ul).toBeDefined()
    expect(ul.childNodes).toHaveLength(2)
    expect(ul.childNodes[0].textContent).toBe('user1')
    expect(ul.childNodes[1].textContent).toBe('user2')
});

test('UserList uses a filter', () => {
    const userList = <UsersList
        users={['alpha', 'beta']}
        selectedUser={'user1'}
        setSelectedUser={async () => { }}
    />
    const { baseElement, getByPlaceholderText } = render(userList);
    const ul = baseElement.querySelector('#user_list')
    expect(ul).toBeDefined()
    expect(ul.childNodes).toHaveLength(2)
    expect(ul.childNodes[0].textContent).toBe('alpha')
    expect(ul.childNodes[1].textContent).toBe('beta')

    const filter = getByPlaceholderText('Filter')

    fireEvent.change(filter, { target: { value: 'et' } })
    expect(ul.childNodes).toHaveLength(1)
    expect(ul.childNodes[0].textContent).toBe('beta')

    fireEvent.change(filter, { target: { value: 'lph' } })
    expect(ul.childNodes).toHaveLength(1)
    expect(ul.childNodes[0].textContent).toBe('alpha')

    fireEvent.change(filter, { target: { value: '' } })
    expect(ul.childNodes).toHaveLength(2)
    expect(ul.childNodes[0].textContent).toBe('alpha')
    expect(ul.childNodes[1].textContent).toBe('beta')
});