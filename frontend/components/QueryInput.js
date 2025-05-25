export default function QueryInput({ query, setQuery, onSubmit }) {
  return (
    <form onSubmit={onSubmit} className="flex space-x-2 mb-4">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter natural language query"
        className="border p-2 flex-grow"
      />
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
        Search
      </button>
    </form>
  )
}