import React from "react"
import DownloadFileName from "../atoms/DownloadFileName"
import DownloadButton from "../atoms/DownloadButton"

export default function DownloadFile() {
  const [fileName, setFileName] = React.useState('output.py')

  return (
    <div className="flex-col space-y-2">
      <div>
        <DownloadFileName setFileName={setFileName}/>
      </div>
      <div>
        <DownloadButton fileName={fileName}/>
      </div>
    </div>
  )
}