import { render } from '@testing-library/react';
import { UsersList } from './UsersList';


test('UserView renders', () => {
    const userView = UsersList({
        users: [],
        selectedUser: 'user1',
        setSelectedUser: async () => { },
    })
    const { baseElement } = render(userView);
    expect(baseElement).not.toBeNull()
});

test('UserView has 2 users', () => {
    const userView = UsersList({
        users: ['user1', 'user2'],
        selectedUser: 'user1',
        setSelectedUser: async () => { },
    })
    const { baseElement } = render(userView);
    const ul = baseElement.querySelector('#user_list')
    expect(ul).not.toBeNull()
    expect(ul.childNodes).toHaveLength(2)
    expect(ul.childNodes[0].textContent).toBe('user1')
    expect(ul.childNodes[1].textContent).toBe('user2')
});
