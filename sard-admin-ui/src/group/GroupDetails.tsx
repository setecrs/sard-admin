import React, { Fragment, useState, useEffect } from 'react'

import { SelectList } from '../elements/SelectList'
import { Job } from '../data/fetcher'

export function GroupDetails({
    group,
    myUsers,
    allUsers,
    addMember,
    listMembers,
    fixPermissions,
    listJobHistory,
}: {
    group: string,
    myUsers: string[],
    allUsers: string[],
    addMember: ({ user, group }: { user: string, group: string }) => Promise<void>,
    listMembers: ({ group }: { group: string }) => Promise<void>,
    fixPermissions: ({ group }: { group: string }) => Promise<void>,
    listJobHistory: ({ group }: { group: string }) => Promise<Job[]>,
}) {
    const [selectedUser, setSelectedUser] = useState('')
    const [refreshing, setRefreshing] = useState(false)
    const [jobs, setJobs] = useState<Job[]>([])

    useEffect(() => {
        (async () => {
            setRefreshing(true)
            const lm = listMembers({ group })
            const lh = listJobHistory({ group })
            setJobs(await lh)
            await lm
            setRefreshing(false)
        })()
    }, [group])

    if (!group) {
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
        <div className="row p-3">
            <div>
                <SelectList
                    id='selectMyUser'
                    elements={allUsers}
                    selectedValue={selectedUser}
                    setSelectedValue={setSelectedUser}
                />
            </div>
            <div>
                <button
                    className="button btn btn-primary"
                    onClick={async () => {
                        setRefreshing(true)
                        await addMember({ user: selectedUser, group })
                        setRefreshing(false)
                    }}
                >Add user</button>
            </div>
        </div>
        <div className="row p-3">
            <button
                className="button btn btn-primary"
                onClick={() => fixPermissions({ group })}
            >Fix group directory permissions</button>
        </div>
        {(jobs) ?
            <ul> <h5>Group permission jobs:</h5>
                {jobs.map((j, i) => {
                    return <li key={i}>
                        Running: {JSON.stringify(j.running)}
                        <br />
                        Start: {j.start.toISOString()}
                        <br />
                        End: {j.end.toISOString()}
                        <br />
                        Output: <pre>{j.output}</pre>
                    </li>
                })}
            </ul>
            : ''
        }
    </Fragment>
}
