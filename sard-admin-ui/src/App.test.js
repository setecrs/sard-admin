import React from 'react';
import { render } from '@testing-library/react';
import App from './App';

test('#navbar has Users and Groups', () => {
  const { baseElement } = render(<App />);
  expect(baseElement.querySelectorAll('#navbar')).toHaveLength(1)
  const ul = baseElement.querySelector("#navbar")
  expect(ul.childNodes).toHaveLength(2)
  expect(ul.childNodes[0].textContent).toBe("Users")
  expect(ul.childNodes[1].textContent).toBe("Groups")
});
