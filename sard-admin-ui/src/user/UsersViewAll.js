import React from 'react'
import UsersList from './UsersList'
import { CreateUser } from './CreateUser'

function UsersViewAll({ users, selectedUser, setSelectedUser, createUser }) {
    return <div className="container">
        <CreateUser createUser={createUser} />
        <div className="row my-3 p-3">
            <div className="col-md-3">
                {UsersList({ users, selectedUser, setSelectedUser })}
            </div>
        </div>
    </div>
}

export default UsersViewAll