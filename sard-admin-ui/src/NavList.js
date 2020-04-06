import React from 'react';

function NavList({ id, elements, selectedIdx, setSelectedIdx }) {
    return <ul id={id} className="nav nav-tabs">
        {elements.map((element, i) => (
            <li key={i} className="nav-item">
                <a className={(i === selectedIdx) ? "nav-link active" : "nav-link"}
                    onClick={() => setSelectedIdx(i)}>
                    {element}
                </a>
            </li>
        ))}
    </ul>
}

export default NavList