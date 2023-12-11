import React from 'react'
import Radio from '@mui/material/Radio'
import RadioGroup from '@mui/material/RadioGroup'
import FormControlLabel from '@mui/material/FormControlLabel'
import FormControl from '@mui/material/FormControl'
import FormLabel from '@mui/material/FormLabel'
import Axios from 'axios'

export default function ConfigRadio() {
  const [config, setConfig] = React.useState('first')

  function handleChange(event) {
    Axios.get(`http://127.0.0.1:5000/set_config/${event.target.value}`)
    .then(function(response) {
      console.log(response)
      setConfig(event.target.value)
    })
    .catch(function(error) {
      console.error(error)
    })
  }

  return (
    <FormControl>
      <FormLabel>同一フレームの取得設定</FormLabel>
      <RadioGroup
        row
        value={config}
        onChange={handleChange}
      >
        <FormControlLabel value="first" control={<Radio />} label="初めのフレーム"/>
        <FormControlLabel value="last" control={<Radio />} label="最後のフレーム"/>
        <FormControlLabel value="all" control={<Radio />} label="全てのフレーム"/>
      </RadioGroup>
    </FormControl>
  )
}
