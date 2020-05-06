import React from 'react'
import { render, wait } from "@testing-library/react"
import { RestartButton } from "./RestartButton"

test('restart button', async () => {
  const folders_count = async () => {
    return 3
  }
  const folders_rename = async () => {
    return true
  }
  const { baseElement } = render(<RestartButton
    imagepath='/a/b/c/image.dd'
    folders_count={folders_count}
    folders_rename={folders_rename}
  />)
  await wait(() => {
    expect(baseElement).toBeDefined()
  })
})