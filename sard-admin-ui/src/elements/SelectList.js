import React, { Fragment } from 'react';

export function SelectList({ id, elements, selectedValue, setSelectedValue }) {
    return <Fragment>
        <select
            id={id}
            value={selectedValue}
            onChange={e => setSelectedValue(e.target.value)}
        >   
            <option value=''/>
            {elements.map(element => (
                <option key={element} value={element}>
                    {element}
                </option>
            ))}
        </select>
    </Fragment>
}
