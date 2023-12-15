import React from "react"
import Alert from "@mui/material/Alert"
import FramesDiffTexts from "../atoms/FrameDiffTexts"
import FramesDiffImage from "../atoms/FrameDiffImage"

export default function FrameDiff() {
  const [b64frame, setb64frame] = React.useState(null)

  return (
    <div className="flex-col space-y-4">
      <div>
        <Alert security="info">ソース動画とターゲット動画の差分取得。</Alert>
      </div>
      <div>
        <FramesDiffTexts setb64frame={setb64frame}/>
      </div>
      {b64frame &&
        <div>
          <FramesDiffImage b64frame={b64frame}/>
        </div>
      }
    </div>
  )
}