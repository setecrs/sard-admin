import React from 'react';
import PropTypes from 'prop-types'

function UsersList({ users, selectedUser, setSelectedUser }) {
    return <ul id='user_list' className="list-group">
        {users.map((u, i) => (
            <li key={i} 
            className={(u===selectedUser)?"list-group-item active":"list-group-item"}
            onClick={() => setSelectedUser(u)}>
                {u}
            </li>
        ))}
    </ul>
}
UsersList.propTypes = {
    users: PropTypes.arrayOf(PropTypes.string)
}

export default UsersList