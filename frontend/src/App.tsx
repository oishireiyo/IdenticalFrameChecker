import React, { ChangeEvent } from 'react'
import Page from './components/templates/Page'
import Axios from 'axios'

// https://keko5342.hatenadiary.jp/entry/2021/12/10/031756
Axios.defaults.baseURL = 'http://127.0.0.1:5000'

export default function App() {
  return (
    <Page />
  )
}