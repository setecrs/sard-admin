import React from 'react';
import PropTypes from 'prop-types'

export function UsersList({
    users,
    selectedUser,
    setSelectedUser,
}:{
    users:string[],
    selectedUser:string,
    setSelectedUser:(x:string)=>void,
}) {
    return <ul id='user_list' className="list-group">
        {users.map((u, i) => (
            <li key={i}
                className={(u === selectedUser) ? "list-group-item active" : "list-group-item"}
                onClick={() => setSelectedUser(u)}>
                {u}
            </li>
        ))}
    </ul>
}
UsersList.propTypes = {
    users: PropTypes.arrayOf(PropTypes.string)
}
