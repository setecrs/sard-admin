import React from 'react'
import { UsersList } from './UsersList'
import { CreateName } from '../elements/CreateName'
import { UserDetails } from './UserDetails'
import { GenericPage } from '../elements/GenericPage'

export function UsersPage({ users, selectedUser, setSelectedUser, createUser, fixHome, addMember, groups, subscriptions}) {
    const elemCreate = <CreateName
        id='createUser'
        name='user'
        createFunc={createUser}
    />
    const elemList = <UsersList
        users={users}
        selectedUser={selectedUser}
        setSelectedUser={setSelectedUser}
    />
    const elemDetail = <UserDetails
        user={selectedUser}
        fixHome={fixHome}
        addMember={addMember}
        mygroups={subscriptions[selectedUser]||[]}
        allGroups={groups}
    />

    return <GenericPage
        elemCreate={elemCreate}
        elemList={elemList}
        elemDetail={elemDetail}
    />
}

