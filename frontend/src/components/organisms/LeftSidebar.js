import React from "react"
import ConfigRadio from "../atoms/ConfigRadio"
import CallButton from "../atoms/CallButton"
import DownloadFile from "../molecules/DownloadFile"
import Alert from "@mui/material/Alert"

export default function LeftSidebar(props) {
  const {sourceVideo, targetVideo} = props

  const {done, setDone} = React.useState(false)

  return (
    <div className="flex-col space-y-4">
      <div>
        <Alert security="info">処理の設定と結果の取得。</Alert>
      </div>
      <div>
        <ConfigRadio />
      </div>
      <div>
        <CallButton
          sourceVideo={sourceVideo}
          targetVideo={targetVideo}
          setDone={setDone}
        />
      </div>
      <div>
        <DownloadFile done={done}/>
      </div>
    </div>
  )
}