import React, { Fragment, useState, useEffect } from 'react';

export function SelectList({ id, elements, selectedValue, setSelectedValue }: { id: string, elements: string[], selectedValue: string, setSelectedValue: (v: string) => void }) {
    const [filter, setFilter] = useState('')
    const [filtered, setFiltered] = useState<string[]>([])

    useEffect(() => {
        setFiltered(['', ...elements].filter(x => x.indexOf(filter) > -1))
    }, [filter, elements])

    useEffect(() => {
        if (!filtered.includes(selectedValue)) {
            if (filtered.length > 0) {
                setSelectedValue(filtered[0])
            }
        }
    }, [filtered, selectedValue])


    return <Fragment>
        Filter: <input
            placeholder="Filter"
            value={filter}
            onChange={e => setFilter(e.target.value)}
        />
        <select
            id={id}
            value={selectedValue}
            onChange={e => setSelectedValue(e.target.value)}
        >
            {filtered.map(element => (
                <option key={element} value={element}>
                    {element}
                </option>
            ))}
        </select>
    </Fragment>
}
