import React from "react"
import Button from '@mui/material/Button'
import Axios from 'axios'

export default function GetVideoInfoButton(props) {
  const {kind, video, setVideoinfo} = props

  function handleClick() {
    Axios.get(`http://127.0.0.1:5000/get_video_information/${kind}`)
    .then(function(response) {
      console.log(response)
      setVideoinfo(response.data.information)
    })
    .catch(function(error) {
      console.error(error)
    })
  }

  return (
    <>
      <Button color="primary" variant="contained" disabled={!video} onClick={handleClick}>
        画像の情報を取得
      </Button>
    </>
  )
}