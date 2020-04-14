import React from 'react';
import { render, wait } from '@testing-library/react';
import { GroupPage } from './GroupPage';

test('GroupView renders', async () => {
  const { baseElement, getByText } = render(GroupPage({
    groups: ['group1'],
    addMember: async () => { },
    allUsers: ['b1', 'b2'],
    createGroup: async () => { },
    fixPermissions: async () => { },
    listMembers: async () => { },
    myUsers: [],
    selectedGroup: '',
    setSelectedGroup: () => { },
  }));
  await wait(() => {
    expect(baseElement).toBeDefined()
  })
  expect(getByText(/group1/)).toBeDefined()
});

test.todo('list all groups: /group/')
test.todo('list members: /group/{g}')
test.todo('create new group: /group/{g}')
test.todo('group permissions: /group/{g}/permissions')
test.todo('add user to group: /user/{u}/group/{g}')