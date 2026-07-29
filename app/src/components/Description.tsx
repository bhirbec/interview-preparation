// The problem description comes from impl.py comment blocks that are hard-wrapped
// at ~78 columns for Python source readability. Rendering those newlines verbatim
// makes prose look ragged. So we split the text into blank-line-separated blocks
// and reflow the prose ones, while preserving blocks whose line breaks or
// alignment are meaningful (constraints lists, aligned example tables).

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

export default function Description({ text }: Props) {
  const blocks = text.split(/\n[ \t]*\n/)
  return (
    <div className="prose">
      {blocks.map((block, i) =>
        isProse(block) ? (
          <p key={i} className="para">
            {block.split('\n').join(' ')}
          </p>
        ) : (
          <pre key={i} className="block">
            {block}
          </pre>
        ),
      )}
    </div>
  )
}
