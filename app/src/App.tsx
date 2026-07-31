import { Routes, Route } from 'react-router-dom'
import ProblemList from './pages/ProblemList'
import ProblemDetail from './pages/ProblemDetail'
import Program from './pages/Program'
import Chapter from './pages/Chapter'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<ProblemList />} />
      {/* Ids can contain "/" (e.g. CTCI/1.1-is-unique), so use a splat route. */}
      <Route path="/problem/*" element={<ProblemDetail />} />
      <Route path="/program" element={<Program />} />
      <Route path="/chapter/*" element={<Chapter />} />
    </Routes>
  )
}
