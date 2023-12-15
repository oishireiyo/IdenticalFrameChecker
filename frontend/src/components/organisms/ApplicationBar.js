import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

export default function ApplicationBar() {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h5">Time Code Coincident</Typography>
      </Toolbar>
    </AppBar>
  );
}
