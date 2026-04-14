import { useCallback, useEffect, useRef, useState } from 'react'
import Grid from './components/Grid.jsx'
import Keyboard from './components/Keyboard.jsx'
import ThemeBanner from './components/ThemeBanner.jsx'

const MAX_GUESSES = 6

function App() {
  const [theme, setTheme] = useState('')
  const [date, setDate] = useState('')
  const [wordLength, setWordLength] = useState(5)
  const [rows, setRows] = useState([])
  const [currentGuess, setCurrentGuess] = useState('')
  const [status, setStatus] = useState('loading')
  const [errorMessage, setErrorMessage] = useState('')
  const restoredRef = useRef(false)

  useEffect(() => {
    fetch('/api/puzzle/today')
      .then(async r => {
        if (!r.ok) throw new Error(`puzzle fetch failed (${r.status})`)
        return r.json()
      })
      .then(data => {
        setTheme(data.theme)
        setDate(data.date)
        setWordLength(data.reveal_length)
        setStatus('playing')
      })
      .catch(err => {
        setErrorMessage(err.message)
        setStatus('error')
      })
  }, [])

  useEffect(() => {
    if (!date) return
    const saved = localStorage.getItem(`mindforge:${date}`)
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        if (Array.isArray(parsed.rows)) {
          // eslint-disable-next-line react-hooks/set-state-in-effect
          setRows(parsed.rows)
        }
        if (parsed.status === 'won' || parsed.status === 'lost') {
          setStatus(parsed.status)
        }
      } catch {
        // ignore malformed cache
      }
    }
    restoredRef.current = true
  }, [date])

  useEffect(() => {
    if (!date || !restoredRef.current) return
    localStorage.setItem(
      `mindforge:${date}`,
      JSON.stringify({ rows, status })
    )
  }, [rows, status, date])

  const submitGuess = useCallback(async () => {
    if (status !== 'playing' || currentGuess.length !== wordLength) return
    try {
      const r = await fetch('/api/guess', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ guess: currentGuess }),
      })
      const body = await r.json().catch(() => ({}))
      if (r.status === 400 || r.status === 409) {
        setErrorMessage(body.error || 'invalid guess')
        return
      }
      if (!r.ok) {
        setErrorMessage(`server error (${r.status})`)
        return
      }
      setErrorMessage('')
      setRows(prev => [...prev, { guess: currentGuess, feedback: body.feedback }])
      setCurrentGuess('')
      if (body.solved) {
        setStatus('won')
      } else if (body.guess_count >= MAX_GUESSES) {
        setStatus('lost')
      }
    } catch (err) {
      setErrorMessage(err.message || 'network error')
    }
  }, [currentGuess, wordLength, status])

  const onLetter = useCallback(
    letter => {
      if (status !== 'playing') return
      setErrorMessage('')
      setCurrentGuess(prev =>
        prev.length >= wordLength ? prev : prev + letter.toUpperCase()
      )
    },
    [status, wordLength]
  )

  const onBackspace = useCallback(() => {
    if (status !== 'playing') return
    setErrorMessage('')
    setCurrentGuess(prev => prev.slice(0, -1))
  }, [status])

  useEffect(() => {
    const handler = e => {
      if (e.metaKey || e.ctrlKey || e.altKey) return
      if (e.key === 'Enter') {
        e.preventDefault()
        submitGuess()
      } else if (e.key === 'Backspace') {
        e.preventDefault()
        onBackspace()
      } else if (/^[a-zA-Z]$/.test(e.key)) {
        onLetter(e.key)
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [submitGuess, onLetter, onBackspace])

  if (status === 'loading') {
    return (
      <div className="app">
        <p className="muted">Loading today's puzzle…</p>
      </div>
    )
  }

  if (status === 'error') {
    return (
      <div className="app">
        <p className="error">Couldn't load puzzle: {errorMessage}</p>
      </div>
    )
  }

  const letterStates = computeLetterStates(rows)

  return (
    <div className="app">
      <ThemeBanner theme={theme} date={date} />
      <Grid
        rows={rows}
        currentGuess={currentGuess}
        maxGuesses={MAX_GUESSES}
        wordLength={wordLength}
        shake={Boolean(errorMessage) && status === 'playing'}
      />
      {errorMessage && status === 'playing' && (
        <p className="error">{errorMessage}</p>
      )}
      {status === 'won' && (
        <p className="banner banner-win">Solved in {rows.length}!</p>
      )}
      {status === 'lost' && (
        <p className="banner banner-lose">Out of guesses.</p>
      )}
      <Keyboard
        onLetter={onLetter}
        onEnter={submitGuess}
        onBackspace={onBackspace}
        letterStates={letterStates}
        disabled={status !== 'playing'}
      />
    </div>
  )
}

function computeLetterStates(rows) {
  const priority = { hit: 3, present: 2, miss: 1 }
  const states = {}
  for (const { guess, feedback } of rows) {
    for (let i = 0; i < guess.length; i++) {
      const letter = guess[i]
      const status = feedback[i]
      const prev = states[letter]
      if (!prev || priority[status] > priority[prev]) {
        states[letter] = status
      }
    }
  }
  return states
}

export default App
