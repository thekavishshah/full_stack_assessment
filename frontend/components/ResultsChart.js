import { BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts'

export default function ResultsChart({ data }) {
  const chartData = data.map((item) => ({
    name: item.name,
    value: item.age?.gt || item.age?.lt || 0,
  }))
  return (
    <BarChart width={500} height={300} data={chartData}>
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Bar dataKey="value" />
    </BarChart>
  )
}