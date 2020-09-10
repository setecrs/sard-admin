import React from 'react';
import { render, wait } from '@testing-library/react';
import { LaunchPage } from './LaunchPage';

test('GroupView renders', async () => {
  const { baseElement, getByText } = render(<LaunchPage
    addJob={()=>{}}
  />);
  await wait(() => {
    expect(baseElement).toBeDefined()
  })
  expect(getByText(/Launch IPED/)).toBeDefined()
})