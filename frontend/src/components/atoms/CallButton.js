import React from 'react'
import Button from '@mui/material/Button'
import ArrowForwardIcon from '@mui/icons-material/ArrowForward'
import Axios from 'axios'

export default function CallButton() {
  function handleClick() {
    Axios.get('/execute')
    .then(function(response) {
      console.log(response)
    })
    .catch(function(error) {
      console.error(error)
    })
  }

  return (
    <>
      <Button color='primary' variant='contained' onClick={handleClick} startIcon={<ArrowForwardIcon />}>
        処理実行
      </Button>
    </>
  )
}