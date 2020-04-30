import React from 'react'
import { UsersList } from './UsersList'
import { CreateName } from '../elements/CreateName'
import { UserDetails } from './UserDetails'
import { GenericPage } from '../elements/GenericPage'
import PropTypes from 'prop-types'

export function UsersPage({
    users,
    allGroups,
    myGroups,
    selectedUser,
    setSelectedUser,
    createUser,
    fixHome,
    fixPermissions,
    addMember,
    listSubscriptions,
    setPassword,
}: {
    users: string[],
    allGroups: string[],
    myGroups: string[],
    selectedUser: string,
    setSelectedUser: (x: string) => void,
    createUser: ({ user }: { user: string }) => Promise<void>,
    fixHome: ({ user }: { user: string }) => Promise<void>,
    fixPermissions: ({ user }: { user: string }) => Promise<void>,
    addMember: ({ user, group }: { user: string, group: string }) => Promise<void>,
    listSubscriptions: ({ user }: { user: string }) => Promise<void>,
    setPassword: ({user, password}: {user: string, password: string}) => Promise<void>,
}) {
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
        allGroups={allGroups}
        mygroups={myGroups}
        fixHome={fixHome}
        fixPermissions={fixPermissions}
        addMember={addMember}
        listSubscriptions={listSubscriptions}
        setPassword={setPassword}
    />

    return <GenericPage
        elemCreate={elemCreate}
        elemList={elemList}
        elemDetail={elemDetail}
    />
}

UsersPage.propTypes = {
    users: PropTypes.arrayOf(PropTypes.string).isRequired,
    allGroups: PropTypes.arrayOf(PropTypes.string).isRequired,
    myGroups: PropTypes.arrayOf(PropTypes.string).isRequired,
    selectedUser: PropTypes.string.isRequired,
    setSelectedUser: PropTypes.func.isRequired,
    createUser: PropTypes.func.isRequired,
    fixHome: PropTypes.func.isRequired,
    addMember: PropTypes.func.isRequired,
    listSubscriptions: PropTypes.func.isRequired,
}