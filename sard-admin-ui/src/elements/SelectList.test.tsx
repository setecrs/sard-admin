import React, { useState } from 'react'
import { SelectList } from './SelectList'
import { render, fireEvent } from '@testing-library/react'

test('filter list of groups', async () => {
  let v = 'xxx'
  const userDetails = <SelectList
    id='myid'
    elements={['alpha', 'beta']}
    selectedValue={v}
    setSelectedValue={(newv) => { v = newv }}
  />
  const { getByPlaceholderText, getAllByRole, baseElement } = render(userDetails)
  const filter = getByPlaceholderText(/filter/i)

  fireEvent.change(filter, { target: { value: 'et' } })
  expect(getAllByRole('option')).toHaveLength(1)
  expect(getAllByRole('option')[0].textContent).toEqual('beta')

  fireEvent.change(filter, { target: { value: 'lp' } })
  expect(getAllByRole('option')).toHaveLength(1)
  expect(getAllByRole('option')[0].textContent).toEqual('alpha')
  expect(v).toEqual('alpha')

  fireEvent.change(filter, { target: { value: '' } })
  expect(getAllByRole('option')).toHaveLength(3)
  expect(getAllByRole('option')[0].textContent).toEqual('')
  expect(getAllByRole('option')[1].textContent).toEqual('alpha')
  expect(getAllByRole('option')[2].textContent).toEqual('beta')
})
