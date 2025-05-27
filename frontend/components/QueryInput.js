import { useState, useEffect } from 'react'

export default function QueryInput({ query, setQuery, onSubmit }) {
  const [suggestions, setSuggestions] = useState([])

  // -------------------------------------------------------------
  // Autocomplete hook – hit backend as the user types
  // -------------------------------------------------------------
  useEffect(() => {
    if (!query) {
      setSuggestions([])
      return
    }

    const controller = new AbortController()
    const url = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/autocomplete?prefix=${encodeURIComponent(query)}`

    fetch(url, { signal: controller.signal })
      .then((r) => r.json())
      .then(setSuggestions)
      .catch(() => {})

    return () => controller.abort()
  }, [query])

  const choose = (s) => {
    setQuery(s)
    setSuggestions([])
  }

  return (
    <div className="relative">
      <form onSubmit={onSubmit} className="flex space-x-2 mb-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter natural‑language query"
          className="border p-2 flex-grow"
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
          Search
        </button>
      </form>

      {suggestions.length > 0 && (
        <ul className="absolute z-10 w-full bg-white border shadow max-h-60 overflow-y-auto">
          {suggestions.map((s) => (
            <li key={s} className="p-2 cursor-pointer hover:bg-gray-100" onClick={() => choose(s)}>
              {s}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}