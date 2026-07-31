import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { MdMoreVert, MdClose, MdListAlt, MdSchool } from 'react-icons/md'
import ThemeToggle from './ThemeToggle'

// Top-left 3-dot button that opens a left-hand drawer. Holds app-wide nav and
// controls (Questions, theme). Closes on overlay click, Escape, or navigation.
export default function AppMenu() {
  const [open, setOpen] = useState(false)

  useEffect(() => {
    if (!open) return
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') setOpen(false)
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open])

  return (
    <>
      <button
        type="button"
        className="menu-btn"
        onClick={() => setOpen(true)}
        aria-label="Open menu"
        aria-expanded={open}
      >
        <MdMoreVert />
      </button>

      {open && <div className="drawer-overlay" onClick={() => setOpen(false)} />}

      <aside className={`drawer ${open ? 'open' : ''}`} aria-hidden={!open}>
        <div className="drawer-head">
          <span className="drawer-title">Coding Trainer</span>
          <button
            type="button"
            className="drawer-close"
            onClick={() => setOpen(false)}
            aria-label="Close menu"
          >
            <MdClose />
          </button>
        </div>
        <nav className="drawer-items">
          <Link to="/" className="drawer-item" onClick={() => setOpen(false)}>
            <MdListAlt />
            <span>Questions</span>
          </Link>
          <Link to="/program" className="drawer-item" onClick={() => setOpen(false)}>
            <MdSchool />
            <span>Program</span>
          </Link>
          <ThemeToggle />
        </nav>
      </aside>
    </>
  )
}
