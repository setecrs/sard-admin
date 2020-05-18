import React from 'react';
import { render, wait } from '@testing-library/react';
import {ProcessingPage} from './ProcessingPage';
import { MockFetcher } from '../data/fetcher';
import { MockCardFetcher } from '../data/card_fetcher';
import { MockLockFetcher } from '../data/lock_fetcher';

test('it renders', async () => {
  const { baseElement, debug} = render(<ProcessingPage
    fetcher={MockFetcher()} 
    card_fetcher={MockCardFetcher()}
    lockFetcher={MockLockFetcher()}
    />)
  await wait(() =>
    expect(baseElement).toBeDefined()
  )
});

test('it accepts empty lock list', async () => {
  const { baseElement, getAllByText} = render(<ProcessingPage
    fetcher={MockFetcher()} 
    card_fetcher={MockCardFetcher()}
    lockFetcher={{
      getLocks: async () => {return []}
    }}
    />)
  await wait(() =>
    expect(baseElement).toBeDefined()
  )
  expect(() =>{
    getAllByText(/Error/i)
  }).toThrow()
});

