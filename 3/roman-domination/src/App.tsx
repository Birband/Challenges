import { useState } from 'react'
import './App.css'
import GraphComponent from './components/graph/Graph'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1>Graph</h1>
      <div>
        <GraphComponent />
      </div>
    </>
  )
}

export default App
