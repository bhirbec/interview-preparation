import { useEffect, useRef, useState } from 'react'
import { api } from '../api'

export type SaveState = 'idle' | 'unsaved' | 'saving' | 'saved' | 'error'

export const SAVE_LABELS: Record<SaveState, string> = {
  idle: '',
  unsaved: '● Unsaved',
  saving: 'Saving…',
  saved: 'Saved ✓',
  error: 'Save failed',
}

// Autosave the editor with a debounce. `scheduleSave` after each edit; `saveNow`
// (also bound to Cmd/Ctrl+S) flushes immediately and resolves when the write
// finishes — callers await it before a test run. `code` is mirrored so Cmd+S and
// saveNow always persist the latest value.
export function useDebouncedSave(id: string, code: string) {
  const [saveState, setSaveState] = useState<SaveState>('idle')
  const timer = useRef<number | undefined>(undefined)
  const codeRef = useRef(code)
  codeRef.current = code

  function doSave(next: string) {
    setSaveState('saving')
    return api
      .saveCode(id, next)
      .then(() => setSaveState('saved'))
      .catch(() => setSaveState('error'))
  }

  function scheduleSave(next: string) {
    setSaveState('unsaved')
    clearTimeout(timer.current)
    timer.current = window.setTimeout(() => doSave(next), 700)
  }

  function saveNow() {
    clearTimeout(timer.current)
    return doSave(codeRef.current)
  }
  const saveNowRef = useRef(saveNow)
  saveNowRef.current = saveNow

  // Reset status on problem change; drop any pending debounce on id change/unmount.
  useEffect(() => {
    setSaveState('idle')
    return () => clearTimeout(timer.current)
  }, [id])

  // Cmd/Ctrl+S saves immediately (and suppresses the browser's Save dialog).
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 's') {
        e.preventDefault()
        saveNowRef.current()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  return { saveState, scheduleSave, saveNow }
}
