import React from 'react';

export function GroupsList({
    groups,
    selectedGroup,
    setSelectedGroup,
}:{
    groups:string[],
    selectedGroup:string,
    setSelectedGroup:(x:string)=>void,
}) {
    return <ul id='group_list' className="list-group">
        {groups.sort().map((u, i) => (
            <li key={i}
                className={(u === selectedGroup) ? "list-group-item active" : "list-group-item"}
                onClick={() => setSelectedGroup(u)}>
                {u}
            </li>
        ))}
    </ul>
}
