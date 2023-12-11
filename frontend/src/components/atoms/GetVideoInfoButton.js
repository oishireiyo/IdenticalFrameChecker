import React from "react"
import Button from '@mui/material/Button'
import Axios from 'axios'

export default function GetVideoInfoButton(props) {
  const {file} = props

  const [fileinfo, setFileinfo] = React.useState({})

  function handleClick() {
    console.log(file)

    const formData = new FormData()
    formData.append('file', file)

    Axios.get('http://127.0.0.1:5000/get_video_information', {'video': file})
    .then(function(response) {
      console.log(response)
      setFileinfo(response.data.information)
    })
    .catch(function(error) {
      console.log(error)
    })
  }

  return (
    <>
      <Button color="primary" variant="contained" disabled={!file} onClick={handleClick}>
        画像の情報を取得
      </Button>
    </>
  )
}