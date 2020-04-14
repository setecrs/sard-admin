import PropTypes from 'prop-types'
import React, { useState, Fragment } from 'react'

export function LoginPage({ login, logout, isLogged }) {
    return <Fragment>
        {(isLogged) ?
            <Logout logout={logout} />
            :
            <Login login={login} />
        }
    </Fragment>
}

export function Logout({ logout }) {
    return <div>
        <button
            className="btn btn-danger"
            onClick={() => {
                logout()
            }}
        >
            Logout
            </button>
    </div>
}

export function Login({ login }) {
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
                type="password"
                onChange={e => {
                    setPassword(e.target.value)
                }}
            />
        </div>
        <div>
            <button
                className="btn btn-success"
                onClick={() => {
                    login({ user, password })
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