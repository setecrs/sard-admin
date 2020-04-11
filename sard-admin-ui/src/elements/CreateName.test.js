import React from 'react';
import { render } from '@testing-library/react';
import { CreateName } from './CreateName';

test('Create name renders', () => {
  const { baseElement, getByText } = render(<CreateName id='asdf' name='name' createFunc={() =>{}}/>)
  expect(baseElement).not.toBeNull()
  expect(getByText(/Create new name/)).not.toBeNull()
});
