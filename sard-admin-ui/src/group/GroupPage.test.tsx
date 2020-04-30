import React from 'react';
import { render, wait } from '@testing-library/react';
import { GroupPage } from './GroupPage';

test('GroupView renders', async () => {
  const { baseElement, getByText } = render(<GroupPage
    groups={['group1']}
    addMember={async () => { }}
    allUsers={['b1', 'b2']}
    createGroup={async () => { }}
    fixPermissions={async () => { }}
    listMembers={async () => { }}
    myUsers={[]}
    selectedGroup={''}
    setSelectedGroup={() => { }}
  />);
  await wait(() => {
    expect(baseElement).toBeDefined()
  })
  expect(getByText(/group1/)).toBeDefined()
})