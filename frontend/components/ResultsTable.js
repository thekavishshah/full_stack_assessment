export default function ResultsTable({ data }) {
  return (
    <table className="min-w-full border mb-4">
      <thead>
        <tr className="bg-gray-200">
          <th className="p-2">Name</th>
          <th className="p-2">Age Filter</th>
          <th className="p-2">Condition</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item, i) => (
          <tr key={i} className="border-t">
            <td className="p-2">{item.name}</td>
            <td className="p-2">{item.age?.gt || item.age?.lt || 'N/A'}</td>
            <td className="p-2">{item['condition.code:text']}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}