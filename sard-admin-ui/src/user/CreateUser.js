import React, { useState, Fragment } from 'react'

export function CreateUser({ createUser }) {
    const [inuse, setInuse] = useState(false)
    const [newuser, setNewuser] = useState('')
    return <div className="row border-bottom border-gray my-3 p-3">
        <div className="col text-right">
            {(inuse) ?
                <Fragment>

                    <input
                        placeholder='New user'
                        value={newuser}
                        onChange={e => {
                            setNewuser(e.target.value)
                        }} />
                    <button
                        className="btn btn-success"
                        onClick={() => {
                            createUser(newuser)
                            setInuse(false)
                            setNewuser('')
                        }}>
                        Create new user
                </button>
                </Fragment>
                :
                <button
                    className="btn btn-default"
                    onClick={() => setInuse(true)}>
                    Create new user
                </button>
            }
        </div>
    </div>

}