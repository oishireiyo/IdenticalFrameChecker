import React from 'react'
import Alert from '@mui/material/Alert'
import FileUploader from '../molecules/FileUploader'
import VideoPlayer from '../molecules/VideoPlayer'
import GetVideoInfoButton from '../atoms/GetVideoInfoButton'
import VideoInfoCard from '../atoms/VideoInfoCard'

export default function GivenVideoPlayer(props) {
  const {kind, alerttext, video, setVideo} = props

  // const [video, setVideo] = React.useState(null)
  const [videoinfo, setVideoinfo] = React.useState({})

  const videoRef = React.useRef(null)

  return (
    <div className='space-y-2 bg-gray-100'>
      <div>
        <Alert security='info'>{alerttext}</Alert>
      </div>
      <div>
        <FileUploader kind={kind} setVideo={setVideo}/>
      </div>
      <div>
        <VideoPlayer video={video} videoRef={videoRef}/>
      </div>
      <div>
        <GetVideoInfoButton kind={kind} video={video} setVideoinfo={setVideoinfo}/>
      </div>
      <div>
        <VideoInfoCard videoinfo={videoinfo}/>
      </div>
    </div>
  )
}