import React from 'react';
import { render } from '@testing-library/react';
import GroupView from './GroupView';

test('GroupView renders', () => {
  const { baseElement, getByText } = render(<GroupView />);
  expect(baseElement).not.toBeNull()
  expect(getByText(/Group/i)).not.toBeNull()
});
