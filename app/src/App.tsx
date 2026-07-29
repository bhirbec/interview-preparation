import { Routes, Route } from 'react-router-dom'
import ProblemList from './pages/ProblemList'
import ProblemDetail from './pages/ProblemDetail'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<ProblemList />} />
      {/* Ids can contain "/" (e.g. CTCI/1.1-is-unique), so use a splat route. */}
      <Route path="/problem/*" element={<ProblemDetail />} />
    </Routes>
  )
}
