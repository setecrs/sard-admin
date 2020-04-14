import React from 'react';
import { render, wait } from '@testing-library/react';
import App from './App';
import { MockFetcher } from './data/fetcher';

test('#navbar has Users and Groups', async () => {
  const { baseElement } = render(<App fetcher={MockFetcher()} />)
  await wait(() =>
    expect(baseElement.querySelectorAll('#navbar')).toHaveLength(1)
  )
  const ul = baseElement.querySelector("#navbar")
  expect(ul.childNodes).toHaveLength(3)
  expect(ul.childNodes[0].textContent).toBe("Users")
  expect(ul.childNodes[1].textContent).toBe("Groups")
  expect(ul.childNodes[2].textContent).toBe("Login")
});

test.todo('has list of running permissions')

test.todo('has login button')
test.todo('has logout button')
