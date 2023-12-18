import React from 'react';
import Slider from '@mui/material/Slider';

import sec2Min from '../../utils/Sec2Min';
import zeroPadding from '../../utils/ZeroPadding';

export default function Seekbar(props) {
  const { file, currentInSec, handleSeekbarValue, durationInSec } = props;
  const current = sec2Min(currentInSec);
  const duration = sec2Min(durationInSec);

  return (
    <>
      <p>
        {current.min}:{zeroPadding(current.sec, 2)} / {duration.min}:
        {zeroPadding(duration.sec, 2)}
      </p>
      <Slider
        value={currentInSec}
        min={0}
        max={durationInSec}
        onChange={handleSeekbarValue}
        step={0.2}
        disabled={!file}
      />
    </>
  );
}
