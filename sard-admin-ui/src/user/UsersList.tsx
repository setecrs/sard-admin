import React, { useState, Fragment, useEffect } from 'react';
import PropTypes from 'prop-types'

export function UsersList({
    users,
    selectedUser,
    setSelectedUser,
}: {
    users: string[],
    selectedUser: string,
    setSelectedUser: (x: string) => void,
}) {
    const [filter, setFilter] = useState('')
    const [filteredUsers, setFilteredUsers] = useState<string[]>([])

    useEffect(() => {
        setFilteredUsers([...users].filter(x => x.indexOf(filter)>-1))
    },[filter, users])

    return <Fragment>
        Filter: <input
            placeholder="Filter"
            value={filter}
            onChange={e => setFilter(e.target.value)}
        />
        <ul id='user_list' className="list-group">
            {filteredUsers.sort().map((u, i) => (
                <li key={i}
                    className={(u === selectedUser) ? "list-group-item active" : "list-group-item"}
                    onClick={() => setSelectedUser(u)}>
                    {u}
                </li>
            ))}
        </ul>
    </Fragment >
}
UsersList.propTypes = {
    users: PropTypes.arrayOf(PropTypes.string)
}
