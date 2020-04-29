import { render } from '@testing-library/react';
import { GroupsList } from './GroupsList';


test('GroupsList renders', () => {
    const groupList = GroupsList({
        groups: [],
        selectedGroup: 'g1',
        setSelectedGroup: async () => { },
    })
    const { baseElement } = render(groupList);
    expect(baseElement).toBeDefined()
});

test('GroupList has 2 groups, sorted', () => {
    const groupList = GroupsList({
        groups: ['g2', 'g1'],
        selectedGroup: 'g1',
        setSelectedGroup: async () => { },
    })
    const { baseElement } = render(groupList);
    const ul = baseElement.querySelector('#group_list')
    expect(ul).toBeDefined()
    expect(ul.childNodes).toHaveLength(2)
    expect(ul.childNodes[0].textContent).toBe('g1')
    expect(ul.childNodes[1].textContent).toBe('g2')
});
