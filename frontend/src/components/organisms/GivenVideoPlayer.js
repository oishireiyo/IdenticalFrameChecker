import React from 'react'
import Alert from '@mui/material/Alert'
import FileUploader from '../molecules/FileUploader'
import VideoPlayer from '../molecules/VideoPlayer'
import GetVideoInfoButton from '../atoms/GetVideoInfoButton'

export default function GivenVideoPlayer(props) {
  const {alerttext} = props

  const [file, setFile] = React.useState(null)

  const videoRef = React.useRef(null)

  return (
    <div className='space-y-2 bg-gray-100'>
      <Alert security='info'>{alerttext}</Alert>
      <FileUploader setFile={setFile}/>
      <VideoPlayer file={file} videoRef={videoRef}/>
      <GetVideoInfoButton file={file}/>
    </div>
  )
}