import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Fetcher, { MockFetcher } from './data/fetcher';
import { CardFetcher, MockCardFetcher } from './data/card_fetcher'
import { LockFetcher, MockLockFetcher } from './data/lock_fetcher'
// import * as serviceWorker from './serviceWorker';

const baseUrl = process.env.REACT_APP_BASE_URL || ''
const graphqlURL = process.env.REACT_APP_GRAPHQL_URL || ''
const lockURL = process.env.REACT_APP_LOCK_URL || ''

let fetcher = Fetcher({ baseUrl })
let cardFetcher = CardFetcher({ graphqlURL })
let lockFetcher = LockFetcher({ lockURL })

if (['test', 'development'].includes(process.env.NODE_ENV)) {
  if (!process.env.hasOwnProperty('REACT_APP_DONT_USE_MOCK')) {
    fetcher = MockFetcher()
    cardFetcher = MockCardFetcher()
    lockFetcher = MockLockFetcher()
  }
}


ReactDOM.render(
  <React.StrictMode>
    <App fetcher={fetcher} cardFetcher={cardFetcher} lockFetcher={lockFetcher} />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
// serviceWorker.unregister();
