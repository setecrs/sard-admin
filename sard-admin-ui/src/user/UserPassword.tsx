import React, { useState } from 'react'

export function UserPassword({
  user,
  setPassword,
}: {
  user:string,
  setPassword: ({ user, password }: { user: string, password: string }) => Promise<void>,
}) {

  const [password, setPassword1] = useState('')
  const [password2, setPassword2] = useState('')
  const defaultBtnClass = "button btn btn-primary"
  const [btnClass, setBtnclass] = useState(defaultBtnClass)

  return <div>
    <div>
      <input
        placeholder='Password'
        value={password}
        onChange={e => setPassword1(e.target.value)}
      />
    </div>
    <div>
      <input
        placeholder='Retype password'
        value={password2}
        onChange={e => setPassword2(e.target.value)}
      />
    </div>
    <div>
      <button
        className={btnClass}
        disabled={!(password && password == password2 && btnClass == defaultBtnClass)}
        onClick={async () => {
          try {
            setBtnclass("button btn btn-secondary")
            await setPassword({ user, password })
            setBtnclass("button btn btn-success")
            setPassword1('')
            setPassword2('')
          } catch (e) {
            console.error(e)
            setBtnclass("button btn btn-danger")
          }
          setTimeout(() => {
            setBtnclass(defaultBtnClass)
          }, 2000);
        }}
      >
        Set password
      </button>
    </div>
  </div>

}