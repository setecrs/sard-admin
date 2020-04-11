import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Fetcher, { MockFetcher } from './data/fetcher';
import assert from 'assert'
// import * as serviceWorker from './serviceWorker';

const baseUrl = process.env.REACT_APP_BASE_URL || ''
let fetcher = Fetcher({baseUrl: baseUrl?baseUrl:''})
if (['test', 'development'].includes(process.env.NODE_ENV)) {
  if (! process.env.hasOwnProperty('REACT_APP_DONT_USE_MOCK')){
    fetcher = MockFetcher()
  }
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
