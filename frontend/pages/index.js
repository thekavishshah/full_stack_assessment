import { useState } from 'react'
import QueryInput from '../components/QueryInput'
import ResultsTable from '../components/ResultsTable'
import ResultsChart from '../components/ResultsChart'

export default function Home() {
  const [query, setQuery] = useState('')
  const [data, setData] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    const res = await fetch('http://localhost:8000/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: query }),
    })
    const json = await res.json()
    // Simulated patients data
    setData([{ name: 'John Doe', ...json }])
  }

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">FHIR NLP Query UI</h1>
      <QueryInput query={query} setQuery={setQuery} onSubmit={handleSubmit} />
      {data && (
        <>
          <ResultsTable data={data} />
          <ResultsChart data={data} />
        </>
      )}
    </main>
  )
}