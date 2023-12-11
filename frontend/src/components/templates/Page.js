import React from 'react'
import ApplicationBar from '../organisms/ApplicationBar'
import GivenVideoPlayer from '../organisms/GivenVideoPlayer'

export default function Page() {
  return (
    <>
      <ApplicationBar />
      <div className='h-screen grid grid-cols-6 divide-x-2 divide-gray-300'>
        <div className='col-span-2'>
          <p>hoge</p>
        </div>
        <div className='col-span-2'>
          <div className='grid grid-rows-2 m-4'>
            <GivenVideoPlayer alerttext="ソース動画を指定してください。"/>
          </div>
          <div>
            <h1>hoge</h1>
          </div>
        </div>
        <div className='col-span-2'>
          <div className='grid grid-rows-2 m-4'>
            <GivenVideoPlayer alerttext="ターゲット動画を指定してください。"/>
          </div>
          <div>
            <h1>aho</h1>
          </div>
        </div>
      </div>
    </>
  )
}