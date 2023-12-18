import React from 'react';
import Button from '@mui/material/Button';
import Axios from 'axios';
import DownloadIcon from '@mui/icons-material/Download';

export default function DownloadButton(props) {
  const { done, fileName } = props;

  async function handleClick() {
    // ファイルのダウンロード
    await Axios.post('/generate_output_file', { as_str: true })
      .then(function (response) {
        console.log(response);

        // Step 1: create the blob object with the text
        const blob = new Blob([response.data.str], { type: 'text/plain' });

        // Step 2: create blob object url
        const url = URL.createObjectURL(blob);

        // Step 3: trigger downloading the object using the url
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        a.click();

        // Step 4: revoke
        URL.revokeObjectURL(url);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  return (
    <Button
      color="primary"
      variant="contained"
      disabled={!done}
      onClick={handleClick}
      startIcon={<DownloadIcon />}
    >
      処理結果の取得
    </Button>
  );
}
