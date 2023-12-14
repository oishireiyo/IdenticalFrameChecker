import React from 'react'
import Button from '@mui/material/Button'
import Axios from 'axios'

export default function DownloadButton(props) {
  const {fileName} = props

  async function handleClick() {
    // 実行結果を出力ファイルにダンプする
    await Axios.post('/generate_output_file', {'output_file_name': 'output.py'})
    .then(function(response) {
      console.log(response)
    })
    .catch(function(error) {
      console.error(error)
    })

    // ファイルのダウンロード
    await Axios.get('/get_generated_output_file')
    .then(function(response) {
      console.log(response)

      // Step 1: create the blob object with the text
      const blob = new Blob([response.data], {type: response.headers.content-type})

      // Step 2: create blob object url
      const url = URL.createObjectURL(blob)

      // Step 3: trigger downloading the object using the url
      const a = document.createElement('a')
      a.href = url
      a.download = fileName
      a.click()

      // Step 4: revoke
      URL.revokeObjectURL(url)
    })
    .catch(function(error) {
      console.log(error)
    })
  }

  return (
    <Button color='primary' variant='contained' onClick={handleClick}>
      処理結果の取得
    </Button>
  )
}