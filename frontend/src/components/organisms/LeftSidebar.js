import React from "react"
import ConfigRadio from "../atoms/ConfigRadio"
import CallButton from "../atoms/CallButton"
import DownloadFile from "../molecules/DownloadFile"
import Alert from "@mui/material/Alert"

export default function LeftSidebar() {
  return (
    <div className="flex-col space-y-2">
      <div>
        <Alert security="info">処理の設定と結果の取得。</Alert>
      </div>
      <div>
        <ConfigRadio />
      </div>
      <div>
        <CallButton />
      </div>
      <div>
        <DownloadFile />
      </div>
    </div>
  )
}