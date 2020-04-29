import React, { Fragment, useEffect, useState } from 'react';

export function GroupsList({
    groups,
    selectedGroup,
    setSelectedGroup,
}: {
    groups: string[],
    selectedGroup: string,
    setSelectedGroup: (x: string) => void,
}) {
    const [filter, setFilter] = useState('')
    const [filteredGroups, setFilteredGroups] = useState<string[]>([])

    useEffect(() => {
        setFilteredGroups([...groups].filter(x => x.indexOf(filter) > -1))
    }, [filter, groups])

    return <Fragment>
        Filter: <input
            placeholder="Filter"
            value={filter}
            onChange={e => setFilter(e.target.value)}
        />
        <ul id='group_list' className="list-group">
            {filteredGroups.sort().map((u, i) => (
                <li key={i}
                    className={(u === selectedGroup) ? "list-group-item active" : "list-group-item"}
                    onClick={() => setSelectedGroup(u)}>
                    {u}
                </li>
            ))}
        </ul>
    </Fragment>
}
