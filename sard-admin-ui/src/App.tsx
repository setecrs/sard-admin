import React, { useState, Fragment, useEffect, useReducer } from 'react';
import PropTypes from 'prop-types'

import NavList from './elements/NavList';
import { UsersPage } from './user/UsersPage';
import { GroupPage } from './group/GroupPage'
import { LoginPage } from './login/LoginPage'
import { initialState, reducer } from './data/state'
import { Actions } from './data/actions'
import { FetcherReturn } from './data/fetcher';
import { Errors } from './elements/Errors'

function App({ fetcher }: { fetcher: FetcherReturn }) {
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

  const usersPage = <UsersPage
    users={state.users}
    allGroups={state.groups}
    myGroups={state.subscriptions[state.selectedUser] || []}
    selectedUser={state.selectedUser}
    setSelectedUser={actions.selectUser}
    createUser={async ({ user }: { user: string }) =>
      actions.createUser({ user, auth_token: state.auth_token })}
    fixHome={async ({ user }: { user: string }) =>
      actions.fixHome({ user, auth_token: state.auth_token })}
    fixPermissions={async ({ user }: { user: string }) =>
      actions.userPermissions({ user, auth_token: state.auth_token })}
    addMember={async ({ user, group }: { user: string, group: string }) =>
      actions.addMember({ user, group, auth_token: state.auth_token })}
    listSubscriptions={async ({ user }: { user: string }) =>
      actions.listSubscriptions({ user, auth_token: state.auth_token })}
  />

  const groupPage = <GroupPage
    groups={state.groups}
    allUsers={state.users}
    myUsers={state.members[state.selectedGroup] || []}
    selectedGroup={state.selectedGroup}
    setSelectedGroup={actions.selectGroup}
    addMember={async ({ user, group }: { user: string, group: string }) =>
      actions.addMember({ user, group, auth_token: state.auth_token })}
    fixPermissions={async ({ group }: { group: string }) =>
      actions.groupPermissions({ group, auth_token: state.auth_token })}
    listMembers={async ({ group }: { group: string }) =>
      actions.listMembers({ group, auth_token: state.auth_token })}
    createGroup={async ({ group }: { group: string }) =>
      actions.createGroup({ group, auth_token: state.auth_token })}
  />

  const loginPage = <LoginPage
    login={actions.login}
    logout={async () =>
      actions.logout({ auth_token: state.auth_token })}
    isLogged={!!state.auth_token}
  />

  const tabs = [
    { title: "Users", element: usersPage },
    { title: "Groups", element: groupPage },
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
            <Errors errors={state.errors} />
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
