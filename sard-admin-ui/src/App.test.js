import React from 'react';
import { render } from '@testing-library/react';
import App from './App';
import { MockFetcher } from './data/fetcher';
import { act } from 'react-dom/test-utils';

test('#navbar has Users and Groups', () => {
  let x
  act(() => {
    x = render(<App fetcher={MockFetcher()} />);
  })
  const { baseElement } = x
  expect(baseElement.querySelectorAll('#navbar')).toHaveLength(1)
  const ul = baseElement.querySelector("#navbar")
  expect(ul.childNodes).toHaveLength(2)
  expect(ul.childNodes[0].textContent).toBe("Users")
  expect(ul.childNodes[1].textContent).toBe("Groups")
});

test.todo('has list of running permissions')

test.todo('has login button')
test.todo('has logout button')
