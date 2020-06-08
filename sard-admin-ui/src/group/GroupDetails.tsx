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
    const [refreshingHistory, setRefreshingHistory] = useState(false)

    const updateHistory = async () => {
        setRefreshingHistory(true)
        const lh = listJobHistory({ group })
        setJobs(await lh)
        setRefreshingHistory(false)
    }

    useEffect(() => {
        (async () => {
            updateHistory()
            setRefreshing(true)
            await listMembers({ group })
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
                onClick={async () => {
                    await fixPermissions({ group })
                    updateHistory()
                }}
            >Fix group directory permissions</button>
        </div>
        {(refreshingHistory) ? 'refreshing' : ''}
        {(jobs && jobs.length > 0) ?
            <ul> <h5>Group permission jobs:</h5>
                <button
                    className="button btn btn-primary"
                    onClick={() => updateHistory()}
                >Update</button>
                {jobs.map((j, i) => {
                    return <li key={i}>
                        Running: {JSON.stringify(j.running)}
                        <br />
                        Start: {toDate(j.start)}
                        <br />
                        End: {toDate(j.end)}
                        <br />
                        Output: <pre>{j.output}</pre>
                    </li>
                })}
            </ul>
            : ''
        }
    </Fragment>
}

function toDate(d: Date) {
    try {
        return JSON.stringify(new Date(Number(d) * 1000))
    } catch (error) {
    }
    return JSON.stringify(d)
}