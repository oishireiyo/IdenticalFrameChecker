import React from 'react'
import Alert from '@mui/material/Alert'
import FileUploader from '../molecules/FileUploader'
import VideoPlayer from '../molecules/VideoPlayer'
import GetVideoInfoButton from '../atoms/GetVideoInfoButton'
import VideoInfoCard from '../atoms/VideoInfoCard'

export default function GivenVideoPlayer(props) {
  const {kind, alerttext} = props

  const [video, setVideo] = React.useState(null)
  const [videoinfo, setVideoinfo] = React.useState({})

  const videoRef = React.useRef(null)

  return (
    <div className='space-y-2 bg-gray-100'>
      <Alert security='info'>{alerttext}</Alert>
      <FileUploader kind={kind} setVideo={setVideo}/>
      <VideoPlayer video={video} videoRef={videoRef}/>
      <GetVideoInfoButton kind={kind} video={video} setVideoinfo={setVideoinfo}/>
      <VideoInfoCard videoinfo={videoinfo}/>
    </div>
  )
}