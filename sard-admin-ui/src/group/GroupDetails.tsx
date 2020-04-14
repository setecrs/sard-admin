import React, { Fragment, useState, useEffect } from 'react'

import { SelectList } from '../elements/SelectList'

export function GroupDetails({
    group,
    myUsers,
    allUsers,
    addMember,
    listMembers,
    fixPermissions,
}:{
    group:string,
    myUsers: string[],
    allUsers: string[],
    addMember:({user, group}:{user:string,group:string})=>Promise<void>,
    listMembers:({group}:{group:string})=>Promise<void>,
    fixPermissions:({group}:{group:string})=>Promise<void>,
}) {
    const [selectedUser, setSelectedUser] = useState('')
    const [refreshing, setRefreshing] = useState(false)

    useEffect(() => {
        (async () => {
            setRefreshing(true)
            await listMembers({ group })
            setRefreshing(false)
        })()
    }, [group])

    if (!group){
        return <Fragment></Fragment>
    }

    return <Fragment>
        <h2>{group}</h2>
        {(refreshing) ? 'refreshing' : ''}
        <ul>
            {myUsers.map((g, i) =>
                <li key={i}>{g}</li>
            )}
        </ul>
        <div>
            <SelectList
                id='selectMyUser'
                elements={allUsers}
                selectedValue={selectedUser}
                setSelectedValue={setSelectedUser}
            />
            <button
                onClick={async () => {
                    setRefreshing(true)
                    await addMember({ user: selectedUser, group })
                    setRefreshing(false)
                }}
            >Add user</button>
        </div>
        <div>
            <button
                onClick={() => fixPermissions({group})}
            >
                Fix group directory permissions
            </button>
        </div>
    </Fragment>
}
