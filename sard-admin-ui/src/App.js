import React, { useState, Fragment, useEffect } from 'react';

import UsersList from './UsersList'
import NavList from './NavList';

function App() {
  const [navActive, setNavActive] = useState(0)
  const [users, setUsers] = useState([])
  const [selectedUser, setSelectedUser] = useState('')

  const usersView = <div className="container">
    <div className="row border-bottom border-gray my-3 p-3">
      <div className="col text-right">
        <button className="btn btn-success">
          Create new user
        </button>
      </div>
    </div>
    <div className="row my-3 p-3">
      <div className="col-md-3">
        {UsersList({ users, selectedUser, setSelectedUser })}
      </div>
    </div>
  </div>


  const fetchUsers = () => {
    setUsers(['template1', 'template2', 'template3'])
  }

  useEffect(() => {
    fetchUsers()
  }, [])

  const groupView = <div>
    Group
  </div>

  const tabs = [
    { title: "Users", element: usersView },
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
        </div>
      </div>
    </div >
  );
}

export default App;
