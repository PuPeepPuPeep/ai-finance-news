import { useState, useEffect } from 'react'
import { getNews } from './services/api'
import Navbar from './components/Navbar'
import NewsCard from './components/NewsCard'

function App() {
  const [news, setNews] = useState([])
  const [selectedTopic, setSelectedTopic] = useState('All')

  useEffect(() => {
    getNews(selectedTopic).then(data => setNews(data))
  }, [selectedTopic])
  return (
    <div className='min-h-screen bg-slate-50'>
      <Navbar activeTopic={selectedTopic} onSelectTopic={setSelectedTopic} />

      <main className='max-w-6xl mx-auto p-6'>
        <header className='mb-8'>
          <h1 className='text-2xl font-bold text-slate-900'>
            {selectedTopic === 'All' ? 'ข่าวล่าสุด' : `ข่าวหมวดหมู่: ${selectedTopic}`}
          </h1>
        </header>
        
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
