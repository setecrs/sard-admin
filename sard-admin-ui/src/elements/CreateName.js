import React, { useState, Fragment } from 'react'

export function CreateName({
    id,
    name,
    createFunc,
}) {
    const [inuse, setInuse] = useState(false)
    const [newName, setNewName] = useState('')
    const creating = <Fragment>
        <input
            placeholder={`New ${name}`}
            value={newName}
            onChange={e => {
                setNewName(e.target.value)
            }} />
        <button
            className="btn btn-success"
            onClick={() => {
                createFunc({[name]:newName})
                setInuse(false)
                setNewName('')
            }}>
            Create new {name}
        </button>
        <button
            className="btn btn-danger"
            onClick={() => {
                setInuse(false)
                setNewName('')
            }}
        >
            Cancel
        </button>
    </Fragment>
    const notCreating = <button
        className="btn btn-primary"
        onClick={() => setInuse(true)}
    >
        Create new {name}
    </button>
    return <div id={id} className="row border-bottom border-gray my-3 p-3">
        <div className="col text-right">
            <div className='input-group'>
                {(inuse) ? creating : notCreating}
            </div>
        </div>
    </div>

}