import React, { Fragment, useState, useEffect } from 'react'
import PropTypes from 'prop-types'

import { SelectList } from '../elements/SelectList'
import { UserPassword } from './UserPassword'

export function UserDetails({
    user,
    mygroups,
    allGroups,
    fixHome,
    fixPermissions,
    addMember,
    listSubscriptions,
    setPassword,
}: {
    user: string,
    mygroups: string[],
    allGroups: string[],
    fixHome: ({ user }: { user: string }) => Promise<void>,
    fixPermissions: ({ user }: { user: string }) => Promise<void>,
    addMember: ({ user, group }: { user: string, group: string }) => Promise<void>,
    listSubscriptions: ({ user }: { user: string }) => Promise<void>,
    setPassword: ({ user, password }: { user: string, password: string }) => Promise<void>,
}) {
    const [selectedGroup, setSelectedGroup] = useState('')
    const [refreshing, setRefreshing] = useState(false)

    useEffect(() => {
        (async () => {
            setRefreshing(true)
            await listSubscriptions({ user })
            setRefreshing(false)
        })()
    }, [user])

    if (!user) {
        return <Fragment></Fragment>
    }

    return <Fragment>
        <h2>{user}</h2>
        {(refreshing) ? 'refreshing' : ''}
        <ul>
            {mygroups.map((g, i) =>
                <li key={i}>{g}</li>
            )}
        </ul>
        <div className="row p-3">
            <div>
                <SelectList
                    id='selectMyGroup'
                    elements={allGroups}
                    selectedValue={selectedGroup}
                    setSelectedValue={setSelectedGroup}
                />
            </div>
            <div>
                <button
                    className="button btn btn-primary"
                    onClick={async () => {
                        setRefreshing(true)
                        await addMember({ group: selectedGroup, user })
                        setRefreshing(false)
                    }}
                >Add group</button>
            </div>
        </div>
        <div className="row p-3">
            <button
                className="button btn btn-primary"
                onClick={() => fixHome({ user })}
            >
                Fill home directory
            </button>
        </div>
        <div className="row p-3">
            <button
                className="button btn btn-primary"
                onClick={() => fixPermissions({ user })}
            >
                Fix home directory permissions
            </button>
        </div>
        <div className="row p-3">
            <UserPassword user={user} setPassword={setPassword} />
        </div>
    </Fragment>
}

UserDetails.propTypes = {
    user: PropTypes.string.isRequired,
    mygroups: PropTypes.arrayOf(PropTypes.string).isRequired,
    allGroups: PropTypes.arrayOf(PropTypes.string).isRequired,
    fixHome: PropTypes.func.isRequired,
    addMember: PropTypes.func.isRequired,
    listSubscriptions: PropTypes.func.isRequired,
}