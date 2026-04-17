import { useState, useEffect } from 'react'
import { getNews } from './services/api'
import NewsCard from './components/NewsCard'

function App() {
  const [news, setNews] = useState([])

  useEffect(() => {
    getNews().then(data => setNews(data))
  }, [])
  return (
    <div className='min-h-screen bg-slate-50'>
      <main className='max-w-6xl mx-auto p-6'>
        <h2 className='text-2xl font-bold mb-6'>ข่าวล่าสุด</h2>
        <div className='grid grid-cols-1 md:grid-cols-2 gap-6'>
          {news.map((news) => (
            <NewsCard key={news.id} data={news}/>
          ))}
        </div>
      </main>
    </div>
  )
    
}

export default App
