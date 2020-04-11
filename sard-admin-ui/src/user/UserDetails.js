import React, { Fragment, useState } from 'react'

import { SelectList } from '../elements/SelectList'

export function UserDetails({
    user,
    fixHome,
    addMember,
    mygroups,
    allGroups,
}) {
    const [selectedGroup, setSelectedGroup] = useState('')

    return <Fragment>
        <h2>{user}</h2>
        <ul>
            {mygroups.map((g, i) =>
                <li key={i}>{g}</li>
            )}
        </ul>
        <div>
            <SelectList
                id='selectMyGroup'
                elements={allGroups}
                selectedValue={selectedGroup}
                setSelectedValue={setSelectedGroup}
            />
            <button
                onClick={() => addMember({ group: selectedGroup, user })}
            >Add group</button>
        </div>
        <div>
            <button
                onClick={() => fixHome(user)}
            >
                Fix home directory permissions
            </button>
        </div>
    </Fragment>
}