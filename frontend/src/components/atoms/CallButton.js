import React from 'react';
import Button from '@mui/material/Button';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import Axios from 'axios';

export default function CallButton(props) {
  const { sourceVideo, targetVideo, setDone } = props;

  function handleClick() {
    Axios.get('/execute')
      .then(function (response) {
        console.log(response);
        setDone(true);
      })
      .catch(function (error) {
        console.error(error);
      });
  }

  return (
    <Button
      color="primary"
      variant="contained"
      disabled={!sourceVideo || !targetVideo}
      onClick={handleClick}
      startIcon={<ArrowForwardIcon />}
    >
      処理実行
    </Button>
  );
}
