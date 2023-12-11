import React from 'react'
import Button from '@mui/material/Button'
import FileUploadIcon from '@mui/icons-material/FileUpload'
import Axios from 'axios'

export default function FileUploader(props) {
  const {kind, setVideo} = props

  const inputRef = React.useRef(null)

  function handleClickSelect() {
    console.log('ファイルの選択')
    inputRef.current.click()
  }

  async function handleChangeFile(event) {
    const files = event.target.files
    if (files[0]) {
      setVideo(files[0])
    }

    const formData = new FormData()
    formData.append('video', files[0])

    await Axios.post(`http://127.0.0.1:5000/set_${kind}_video`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    })
    .then(function(response) {
      console.log(response)
    })
    .catch(function(error) {
      console.log(error)
    })
  }

  return (
    <>
      <Button color='primary' variant='contained' endIcon={<FileUploadIcon />} onClick={handleClickSelect}>ファイルの選択</Button>
      <input type='file' accept='video/mp4' hidden onChange={handleChangeFile} ref={inputRef}/>
    </>
  )
}