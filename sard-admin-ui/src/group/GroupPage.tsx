import React from 'react';

import { CreateName } from '../elements/CreateName';
import { GenericPage } from '../elements/GenericPage';
import { GroupDetails } from './GroupDetails'
import { GroupsList } from './GroupsList'
import { Job } from '../data/fetcher'

export function GroupPage({
    groups,
    allUsers,
    myUsers,
    selectedGroup,
    setSelectedGroup,
    createGroup,
    addMember,
    listMembers,
    fixPermissions,
    listJobHistory,
}: {
    groups: string[],
    allUsers: string[],
    myUsers: string[],
    selectedGroup: string,
    setSelectedGroup: (x: string) => void,
    createGroup: ({ group }: { group: string }) => Promise<void>,
    addMember: ({ user, group }: { user: string, group: string }) => Promise<void>,
    listMembers: ({ group }: { group: string }) => Promise<void>,
    fixPermissions: ({ group }: { group: string }) => Promise<void>,
    listJobHistory: ({group}:{group:string}) => Promise<Job[]>,
}) {
    const elemCreate = <CreateName
        id='createGroup'
        name='group'
        createFunc={createGroup}
    />
    const elemList = <GroupsList
        groups={groups}
        selectedGroup={selectedGroup}
        setSelectedGroup={setSelectedGroup}
    />
    const elemDetail = <GroupDetails
        group={selectedGroup}
        myUsers={myUsers}
        allUsers={allUsers}
        fixPermissions={fixPermissions}
        addMember={addMember}
        listMembers={listMembers}
        listJobHistory={listJobHistory}
    />

    return <GenericPage
        elemCreate={elemCreate}
        elemList={elemList}
        elemDetail={elemDetail}
    />
}
