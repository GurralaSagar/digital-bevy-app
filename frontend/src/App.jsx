import { useEffect, useState } from 'react'
import api from './api'
import './styles.css'

export default function App() {
  const [keyword, setKeyword] = useState('')
  const [repos, setRepos] = useState([])
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(10)
  const [count, setCount] = useState(0)
  const [ordering, setOrdering] = useState('-stars')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const fetchRepos = async (p = page) => {
    setLoading(true)
    setError('')
    try {
      const params = new URLSearchParams({ page: p, page_size: pageSize, ordering })
      if (keyword) params.append('keyword', keyword)
      const { data } = await api.get(`/api/repos/?${params.toString()}`)
      setRepos(data.results)
      setCount(data.count)
      setPage(p)
    } catch (e) {
      setError('Failed to load repositories')
    } finally {
      setLoading(false)
    }
  }

  const onSearch = async (e) => {
    e.preventDefault()
    setError('')
    try {
      setLoading(true)
      await api.post('/api/search/', { keyword, page: 1, per_page: 10 })
      await fetchRepos(1)
    } catch (e) {
      setError(e?.response?.data?.error || 'Search failed')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchRepos(1) }, [])

  const totalPages = Math.ceil(count / pageSize) || 1

  return (
    <div className="container">
      <h1>GitHub Repo Search (Stored)</h1>
      <form onSubmit={onSearch} className="row">
        <input className="input" value={keyword} onChange={(e) => setKeyword(e.target.value)} placeholder="Enter keyword (e.g., django)" />
        <button className="button" type="submit">Search & Store</button>
      </form>

      <div className="row">
        <label>Order:</label>
        <select value={ordering} onChange={(e) => { setOrdering(e.target.value); fetchRepos(1) }}>
          <option value="-stars">Stars ↓</option>
          <option value="stars">Stars ↑</option>
          <option value="-created_at">Newest</option>
          <option value="created_at">Oldest</option>
          <option value="name">Name A→Z</option>
        </select>
        <label>Page size:</label>
        <select value={pageSize} onChange={(e) => { setPageSize(Number(e.target.value)); fetchRepos(1) }}>
          <option>10</option>
          <option>20</option>
          <option>50</option>
        </select>
      </div>

      {error && <div className="err">{error}</div>}
      {loading ? <p>Loading…</p> : (
        <div>
          <p className="meta">Total stored: {count}</p>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {repos.map((r) => (
              <li key={r.url} className="card">
                <a href={r.url} target="_blank" rel="noreferrer"><strong>{r.full_name || r.name}</strong></a>
                <div className="meta">⭐ {r.stars} • {r.language || 'N/A'} • keyword: {r.keyword}</div>
                <p style={{ margin: '6px 0' }}>{r.description || 'No description'}</p>
              </li>
            ))}
          </ul>
          <div className="pager">
            <button className="button" disabled={page <= 1} onClick={() => fetchRepos(page - 1)}>Prev</button>
            <span>Page {page} / {totalPages}</span>
            <button className="button" disabled={page >= totalPages} onClick={() => fetchRepos(page + 1)}>Next</button>
          </div>
        </div>
      )}
    </div>
  )
}
