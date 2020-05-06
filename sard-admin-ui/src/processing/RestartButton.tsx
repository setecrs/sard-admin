import React, { useEffect } from 'react'
import { useState } from "react"

export function RestartButton({
  imagepath,
  folders_count,
  folders_rename,
}: {
  imagepath: string,
  folders_count: ({ imagepath }: { imagepath: string }) => Promise<number>,
  folders_rename: ({ imagepath }: { imagepath: string }) => Promise<boolean>,
}) {
  const [countTxt, setCountTxt] = useState('')
  const [className, setClassName] = useState('button btn btn-primary')

  const onClick = async () => {
    try {
      setClassName('button btn btn-secondary')
      const result = await folders_rename({ imagepath })
      if (!result) {
        setClassName('button btn btn-danger disabled')
      } else {
        setClassName('button btn btn-success disabled')
      }
    } catch (e) {
      setClassName('button btn btn-danger disabled')
    } finally {
      await new Promise(resolve => setTimeout(resolve, 1000))
      setClassName('button btn btn-primary')
      await updateCounter()
    }
  }

  const updateCounter = async () => {
    const counter = await folders_count({ imagepath })
    setCountTxt(` (${counter})`)
  }

  useEffect(() => {
    updateCounter()
  }, [])

  return <button
    className={className}
    disabled={(className.endsWith('disabled'))}
    onClick={onClick}
  >Restart{countTxt}</button>
}