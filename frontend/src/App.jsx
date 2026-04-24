import { useState, useEffect } from 'react'
import { getNews, getTimeSummary } from './services/api'
import Header from './components/Header'
import TimeSummary from './components/TimeSummary'
import NewsCard from './components/NewsCard'
import Footer from './components/Footer'

function App() {
  const [news, setNews] = useState([])
  const [selectedTopic, setSelectedTopic] = useState('Latest')
  const [timeSummary, setTimeSummary] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    setIsLoading(true)
    getNews(selectedTopic)
      .then(data => setNews(data))
      .finally(() => setIsLoading(false))

    if (selectedTopic === 'Latest'){
      getTimeSummary().then(data => {
        if (data) setTimeSummary(data)
      })
    } else {
      setTimeSummary('')
    }
  }, [selectedTopic])

  return (
    <div className='min-h-screen bg-slate-50 flex flex-col'>
      <Header activeTopic={selectedTopic} onSelectTopic={setSelectedTopic} />

      <main className='flex-grow max-w-6xl mx-auto p-6 w-full'>

        {selectedTopic === 'Latest' && <TimeSummary data={timeSummary} />}

        <header className='mb-8'>
          <h1 className='text-2xl font-bold text-slate-900'>
            {selectedTopic === 'Latest' ? 'ข่าวล่าสุด' : `ข่าวหมวดหมู่: ${selectedTopic}`}
          </h1>
        </header>
        
        {isLoading ? (
          <div className='text-center text-slate-400 py-12'>กำลังโหลด...</div>
        ) : (
          <div className='grid grid-cols-1 md:grid-cols-2 gap-6'>
            {news.map((item) => (
              <NewsCard key={item.id} data={item} />
            ))}
          </div>
        )}
      </main>

      <Footer />
    </div>
  )
}

export default App
