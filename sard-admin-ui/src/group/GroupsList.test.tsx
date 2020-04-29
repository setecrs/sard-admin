import React from 'react'
import { render, fireEvent } from '@testing-library/react';
import { GroupsList } from './GroupsList';


test('GroupsList renders', () => {
    const groupList = <GroupsList
        groups={[]}
        selectedGroup={'g1'}
        setSelectedGroup={async () => { }}
    />
    const { baseElement } = render(groupList);
    expect(baseElement).toBeDefined()
});

test('GroupList has 2 groups, sorted', () => {
    const groupList = <GroupsList
        groups={['g2', 'g1']}
        selectedGroup={'g1'}
        setSelectedGroup={async () => { }}
    />
    const { baseElement } = render(groupList);
    const ul = baseElement.querySelector('#group_list')
    expect(ul).toBeDefined()
    expect(ul.childNodes).toHaveLength(2)
    expect(ul.childNodes[0].textContent).toBe('g1')
    expect(ul.childNodes[1].textContent).toBe('g2')
});

test('groupList uses a filter', () => {
    const userList = <GroupsList
        groups={['alpha', 'beta']}
        selectedGroup={'group1'}
        setSelectedGroup={async () => { }}
    />
    const { baseElement, getByPlaceholderText } = render(userList);
    const ul = baseElement.querySelector('#group_list')
    expect(ul).toBeDefined()
    expect(ul.childNodes).toHaveLength(2)
    expect(ul.childNodes[0].textContent).toBe('alpha')
    expect(ul.childNodes[1].textContent).toBe('beta')

    const filter = getByPlaceholderText('Filter')

    fireEvent.change(filter, { target: { value: 'et' } })
    expect(ul.childNodes).toHaveLength(1)
    expect(ul.childNodes[0].textContent).toBe('beta')

    fireEvent.change(filter, { target: { value: 'lph' } })
    expect(ul.childNodes).toHaveLength(1)
    expect(ul.childNodes[0].textContent).toBe('alpha')

    fireEvent.change(filter, { target: { value: '' } })
    expect(ul.childNodes).toHaveLength(2)
    expect(ul.childNodes[0].textContent).toBe('alpha')
    expect(ul.childNodes[1].textContent).toBe('beta')
});