import React from 'react';

export default function FramesDiffImage(props) {
  const { b64frame } = props;

  return <img src={`data:image/jpeg;base64,${b64frame}`} alt="Base64 image" />;
}
