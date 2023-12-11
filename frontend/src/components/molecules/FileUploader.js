import React from 'react'
import Button from '@mui/material/Button'
import FileUploadIcon from '@mui/icons-material/FileUpload'

export default function FileUploader(props) {
  const {setFile} = props

  const inputRef = React.useRef(null)

  function handleClickSelect() {
    console.log('ファイルの選択')
    inputRef.current.click()
  }

  function handleChangeFile(event) {
    const files = event.target.files
    if (files[0]) {
      console.log(files[0])
      setFile(files[0])
    }
  }

  return (
    <>
      <Button color='primary' variant='contained' endIcon={<FileUploadIcon />} onClick={handleClickSelect}>ファイルの選択</Button>
      <input type='file' accept='video/mp4' hidden onChange={handleChangeFile} ref={inputRef}/>
    </>
  )
}