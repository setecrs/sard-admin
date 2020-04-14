import React from 'react'
import { UsersList } from './UsersList'
import { CreateName } from '../elements/CreateName'
import { UserDetails } from './UserDetails'
import { GenericPage } from '../elements/GenericPage'
import PropTypes from 'prop-types'

export function UsersPage({
    users,
    groups,
    selectedUser,
    setSelectedUser,
    createUser,
    fixHome,
    addMember,
    subscriptions,
    listSubscriptions,
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
        allGroups={groups}
        mygroups={subscriptions}
        fixHome={fixHome}
        addMember={addMember}
        listSubscriptions={listSubscriptions}
    />

    return <GenericPage
        elemCreate={elemCreate}
        elemList={elemList}
        elemDetail={elemDetail}
    />
}

UsersPage.propTypes = {
    users: PropTypes.arrayOf(PropTypes.string).isRequired,
    groups: PropTypes.arrayOf(PropTypes.string).isRequired,
    selectedUser: PropTypes.string.isRequired,
    setSelectedUser: PropTypes.func.isRequired,
    createUser: PropTypes.func.isRequired,
    fixHome: PropTypes.func.isRequired,
    addMember: PropTypes.func.isRequired,
    subscriptions: PropTypes.arrayOf(PropTypes.string).isRequired,
    listSubscriptions: PropTypes.func.isRequired,
}