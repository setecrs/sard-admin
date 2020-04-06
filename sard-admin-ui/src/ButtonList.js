import React from 'react';

function ButtonList({ id, elements, selectedIdx, setSelectedIdx }) {
    return <ul id={id} className="list-group">
        {elements.map((element, i) => (
            <li key={i}
                className={(i === selectedIdx) ? "list-group-item active" : "list-group-item"}
                onClick={() => setSelectedIdx(i)}>
                {element}
            </li>
        ))}
    </ul>
}

export default ButtonList