import React, { useState, Fragment, useEffect, useReducer } from 'react';
import PropTypes from 'prop-types'

import NavList from './elements/NavList';
import { UsersPage } from './user/UsersPage';
import { GroupPage } from './group/GroupPage'
import { initialState, reducer, Actions } from './data/state'

function App({ fetcher }) {
  const [state, dispatch] = useReducer(reducer, initialState)
  const actions = Actions({ fetcher, dispatch })

  useEffect(() => {
    const f = async () => {
      const x = actions.listUsers()
      const y = actions.listGroups()
      try {
        await x
      } catch (e) {
        console.error('error on useEffect', e)
        dispatch({ type: 'error', payload: e })
      }
      try {
        await y
      } catch (e) {
        console.error('error on useEffect', e)
        dispatch({ type: 'error', payload: e })
      }
    }
    f()
  }, [])

  const [navActive, setNavActive] = useState(0)

  const usersPage = UsersPage({
    users: state.users,
    selectedUser: state.selectedUser,
    setSelectedUser: actions.selectUser,
    createUser: actions.createUser,
    fixHome: actions.fixHome,
    addMember: actions.addMember,
    groups: state.groups,
    subscriptions: state.subscriptions,
  })

  const groupView = GroupPage({
    groups: state.groups,
    selectedGroup: state.selectedGroup,
    setSelectedGroup: actions.selectGroup,
    createGroup: actions.createGroup,
  })

  const tabs = [
    { title: "Users", element: usersPage },
    { title: "Groups", element: groupView },
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
