import React, { useState, Fragment, useEffect, useReducer } from 'react';
import PropTypes from 'prop-types'

import NavList from './elements/NavList';
import { UsersPage } from './user/UsersPage';
import { GroupPage } from './group/GroupPage'
import { LoginPage } from './login/LoginPage'
import { initialState, reducer } from './data/state'
import { Actions } from './data/actions'

function App({ fetcher }) {
  const [state, dispatch] = useReducer(reducer, initialState)
  const actions = Actions({ fetcher, dispatch })

  useEffect(() => {
    const f = async () => {
      const x = actions.listUsers({ auth_token: state.auth_token })
      const y = actions.listGroups({ auth_token: state.auth_token })
      try {
        await x
      } catch (e) {
        dispatch({ type: 'error', payload: e })
      }
      try {
        await y
      } catch (e) {
        dispatch({ type: 'error', payload: e })
      }
    }
    f()
  }, [])

  const [navActive, setNavActive] = useState(0)

  const addAuth = (auth_token, fn) => (props) => {
    props = {
      ...(props || {}),
      auth_token,
    }
    return fn(props)
  }

  const usersPage = <UsersPage
    users={state.users}
    groups={state.users}
    selectedUser={state.selectedUser}
    subscriptions={state.subscriptions[state.selectedUser] || []}
    setSelectedUser={actions.selectUser}
    createUser={addAuth(state.auth_token, actions.createUser)}
    fixHome={addAuth(state.auth_token, actions.fixHome)}
    addMember={addAuth(state.auth_token, actions.addMember)}
    listSubscriptions={addAuth(state.auth_token, actions.listSubscriptions)}
  />

  const groupPage = <GroupPage
    groups={state.groups}
    selectedGroup={state.selectedGroup}
    setSelectedGroup={actions.selectGroup}
    createGroup={addAuth(state.auth_token, actions.createGroup)}
  />

  const loginPage = <LoginPage
    login={actions.login}
    logout={addAuth(actions.logout)}
    isLogged={!!state.auth_token}
  />

  const tabs = [
    { title: "Users", element: usersPage },
    // { title: "Groups", element: groupPage },
    { title: <Fragment>{state.auth_token ? state.login : 'Login'}</Fragment>, element: loginPage },
  ]

  const navBar = NavList({
    id: "navbar",
    elements: tabs.map(x => x.title),
    selectedIdx: navActive,
    setSelectedIdx: setNavActive,
  })

  return (
    <div className="App">
      <div className="container">
        <div className="row">
          <div className="col-12">
            {navBar}
          </div>
        </div>
        <div className="row">
          <div className="col-12">
            <ul>
              {state.errors.map((x, i) =>
                <li key={i}>
                  {x.toString()}
                </li>
              )}
            </ul>
          </div>
        </div>
        <div className="row">
          <div className="col">
            {tabs.map((tab, i) => (
              (navActive === i) ? (
                <Fragment key={i}>{tab.element}</Fragment>
              ) : ""
            ))}
          </div>
          <Fragment>
            {(state.error) ? JSON.stringify(state.error) : ''}
          </Fragment>
        </div>
      </div>
    </div >
  );
}

App.propTypes = {
  fetcher: PropTypes.shape({
    listUsers: PropTypes.func.isRequired,
    createUser: PropTypes.func.isRequired,
    createGroup: PropTypes.func.isRequired,
    addMember: PropTypes.func.isRequired,
    listMembers: PropTypes.func.isRequired,
    fixHome: PropTypes.func.isRequired,
    userPermissions: PropTypes.func.isRequired,
    setPassword: PropTypes.func.isRequired,
  }).isRequired,
}
export default App;
