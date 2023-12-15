import React from 'react'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Axios from 'axios'

export default function FramesDiffTexts(props) {
  const {setb64frame} = props

  const [sourceFrameID, setSourceFrameID] = React.useState(undefined)
  const [targetFrameID, setTargetFrameID] = React.useState(undefined)

  function handleSourceFrameIDChange(event) {
    setSourceFrameID(event.target.value)
  }

  function handleTargetFrameIDChange(event) {
    setTargetFrameID(event.target.value)
  }

  function handleClick() {
    Axios.post('/get_frames_diff', {'sourceFrameID': sourceFrameID, 'targetFrameID': targetFrameID})
    .then(function(response) {
      console.log(response)
      setb64frame(response.data.b64_frame)
    })
    .catch(function(error) {
      console.error(error)
    })
  }

  return (
    <div className='flex flex-row space-x-2'>
      <div className='flex-1'>
        <TextField
          color='primary'
          variant='outlined'
          label='ソース動画のフレーム番号'
          defaultValue={sourceFrameID}
          required
          onChange={handleSourceFrameIDChange}
        />
      </div>
      <div className='flex-1'>
        <TextField
          color='primary'
          variant='outlined'
          label='ターゲット動画のフレーム番号'
          defaultValue={targetFrameID}
          required
          onChange={handleTargetFrameIDChange}
        />
      </div>
      <div className='flex-auto'>
        <Button
          color='primary'
          variant='contained'
          disabled={!sourceFrameID || !targetFrameID}
          onClick={handleClick}
        >
          差分取得
        </Button>
      </div>
    </div>
  )
}