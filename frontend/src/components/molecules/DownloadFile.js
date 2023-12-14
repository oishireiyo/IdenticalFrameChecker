import React from "react"
import DownloadFileName from "../atoms/DownloadFileName"
import DownloadButton from "../atoms/DownloadButton"

export default function DownloadFile(props) {
  const {done} = props

  const [fileName, setFileName] = React.useState('output.py')

  return (
    <div className="flex-col space-y-4">
      <div>
        <DownloadFileName
          fileName={fileName}
          setFileName={setFileName}
        />
      </div>
      <div>
        <DownloadButton
          done={done}
          fileName={fileName}
        />
      </div>
    </div>
  )
}