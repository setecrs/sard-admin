import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Fetcher, { MockFetcher } from './data/fetcher';
import assert from 'assert'
// import * as serviceWorker from './serviceWorker';

let fetcher = {}
if (process.env.hasOwnProperty('REACT_APP_SARD_ADMIN_URL')){
  fetcher = Fetcher({baseUrl: process.env.REACT_APP_SARD_ADMIN_URL})
} else {
  assert (['test', 'development'].includes(process.env.NODE_ENV))
  fetcher = MockFetcher()
}
ReactDOM.render(
  <React.StrictMode>
    <App fetcher={fetcher}/>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
// serviceWorker.unregister();
