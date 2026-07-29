import { useEffect, useState } from 'react'

// The problem description comes from impl.py comment blocks that are hard-wrapped
// at ~78 columns for Python source readability. Rendering those newlines verbatim
// makes prose look ragged. So we split the text into blank-line-separated blocks
// and reflow the prose ones, while preserving blocks whose line breaks or
// alignment are meaningful (constraints lists, aligned example tables).
//
// The trailing "Approach:" block is a solution hint, so it is hidden behind a
// Show/Hide button rather than shown by default.

interface Props {
  text: string
}

// A block is reflowable prose only if every line reads like plain sentence text:
// not indented, not a bullet, no alignment runs (double spaces), no "->" arrows.
function isProse(block: string): boolean {
  const lines = block.split('\n')
  return lines.every(
    (l) =>
      l.length > 0 &&
      !/^\s/.test(l) &&
      !/^[-*]\s/.test(l) &&
      !/\s{2,}/.test(l) &&
      !l.includes('->'),
  )
}

function renderBlock(block: string, i: number) {
  return isProse(block) ? (
    <p key={i} className="para">
      {block.split('\n').join(' ')}
    </p>
  ) : (
    <pre key={i} className="block">
      {block}
    </pre>
  )
}

export default function Description({ text }: Props) {
  const [showHint, setShowHint] = useState(false)

  // Collapse the hint again when the problem changes.
  useEffect(() => setShowHint(false), [text])

  const blocks = text.split(/\n[ \t]*\n/)
  const hintIdx = blocks.findIndex((b) => /^approach\b/i.test(b.trim()))
  const mainBlocks = hintIdx === -1 ? blocks : blocks.slice(0, hintIdx)
  const hintBlocks = hintIdx === -1 ? [] : blocks.slice(hintIdx)

  return (
    <div className="prose">
      {mainBlocks.map(renderBlock)}
      {hintBlocks.length > 0 && (
        <div className="hint">
          <button
            type="button"
            className="hint-toggle"
            onClick={() => setShowHint((s) => !s)}
          >
            {showHint ? '🡳 Hide hint' : '💡 Show hint'}
          </button>
          {showHint && <div className="hint-body">{hintBlocks.map(renderBlock)}</div>}
        </div>
      )}
    </div>
  )
}
