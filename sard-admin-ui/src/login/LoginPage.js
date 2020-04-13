import PropTypes from 'prop-types'
import React, { useState, Fragment } from 'react'

export function LoginPage({login}) {
    const [user, setUser] = useState('')
    const [password, setPassword] = useState('')

return <Fragment>
        <div>
            <input
                placeholder='user'
                value={user}
                onChange={e => {
                    setUser(e.target.value)
                }}
            />
        </div>
        <div>
            <input
                placeholder='password'
                value={password}
                password
                onChange={e => {
                    setPassword(e.target.value)
                }}
            />
        </div>
        <div>
            <button
                className="btn btn-success"
                onClick={() => {
                    login({user, password})
                    setUser('')
                    setPassword('')
                }}
            >
                Login
            </button>

        </div>
    </Fragment>
}

LoginPage.propTypes = {
    login: PropTypes.func.isRequired,
}