import React from 'react'

export default function VideoInfoCard(props) {
  const {videoinfo} = props

  const entries = Object.entries(videoinfo)

  console.log(entries)

  return (
    <ul>
      {
        entries.map(function(entry, index) {
          return (
            <li key={`info-item-${index}`}>{entry[0]}: {entry[1]}</li>
          )
        })
      }
    </ul>
  )
}