import React from 'react'
import TextField from '@mui/material/TextField'

export default function DownloadFileName(props) {
  const {fileName, setFileName} = props

  function handleChange(event) {
    setFileName(event.target.value)
  }

  return (
    <TextField
      color='primary'
      variant='outlined'
      label='ダウンロードファイル名の指定 (.pyを忘れずに)'
      defaultValue={fileName}
      fullWidth
      onChange={handleChange}
    />
  )
}