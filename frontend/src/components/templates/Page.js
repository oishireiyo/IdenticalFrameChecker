import React from 'react'
import CallAndSetConfig from '../organisms/CallAndSetConfig'
import ApplicationBar from '../organisms/ApplicationBar'
import GivenVideoPlayer from '../organisms/GivenVideoPlayer'

export default function Page() {
  return (
    <>
      <ApplicationBar />
      <div className='h-screen grid grid-cols-6 divide-x-2 divide-gray-300'>
        <div className='col-span-2'>
          <div className='m-4'>
            <CallAndSetConfig />
          </div>
        </div>
        <div className='col-span-2'>
          <div className='m-4'>
            <GivenVideoPlayer kind="source" alerttext="ソース動画を指定してください。"/>
          </div>
        </div>
        <div className='col-span-2'>
          <div className='m-4'>
            <GivenVideoPlayer kind="target" alerttext="ターゲット動画を指定してください。"/>
          </div>
        </div>
      </div>
    </>
  )
}