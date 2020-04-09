import React from 'react';
import { render } from '@testing-library/react';
import GroupView from './GroupView';

test('GroupView renders', () => {
  const { baseElement, getByText } = render(<GroupView />);
  expect(baseElement).not.toBeNull()
  expect(getByText(/Group/i)).not.toBeNull()
});

test.todo('list all groups: /group/')
test.todo('list members: /group/{g}')
test.todo('create new group: /group/{g}')
test.todo('group permissions: /group/{g}/permissions')
test.todo('add user to group: /user/{u}/group/{g}')