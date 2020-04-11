import React, { Fragment } from 'react';
import ButtonList from '../elements/ButtonList';
import { CreateName } from '../elements/CreateName';

export function GroupPage({
    groups,
    selectedGroup,
    setSelectedGroup,
    createGroup,
}) {
    const groupList =     ButtonList({
        id:'groupPage',
        elements:groups,
        selectedValue: selectedGroup,
        setSelectedValue: setSelectedGroup
    }) 

    return <Fragment>
        <CreateName id='createGroup' name='group' createFunc={createGroup} />
        {groupList}
    </Fragment>
}
