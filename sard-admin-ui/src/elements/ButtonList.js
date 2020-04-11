import React from 'react';

function ButtonList({ id, elements, selectedIdx, selectedValue, setSelectedIdx, setSelectedValue }) {
    return <ul id={id} className="list-group">
        {elements.map((element, i) => (
            <li key={i}
                className={(i === selectedIdx || selectedValue === element) ? "list-group-item active" : "list-group-item"}
                onClick={() => setSelectedIdx?setSelectedIdx(i):setSelectedValue(element)}>
                {element}
            </li>
        ))}
    </ul>
}

export default ButtonList