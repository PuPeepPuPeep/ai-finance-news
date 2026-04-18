import { useState, useEffect } from 'react'
import { getNews, getTimeSummary } from './services/api'
import Navbar from './components/Navbar'
import TimeSummary from './components/TimeSummary'
import NewsCard from './components/NewsCard'

function App() {
  const [news, setNews] = useState([])
  const [selectedTopic, setSelectedTopic] = useState('All')
  const [timeSummary, setTimeSummary] = useState('')

  useEffect(() => {
    getNews(selectedTopic).then(data => setNews(data))
    if (selectedTopic === 'All'){
      getTimeSummary().then(data => {
        if (data && data.summary) {
          setTimeSummary(data.summary)
        }
      })
    } else {
      setTimeSummary('')
    }
  }, [selectedTopic])
  return (
    <div className='min-h-screen bg-slate-50'>
      <Navbar activeTopic={selectedTopic} onSelectTopic={setSelectedTopic} />

      <main className='max-w-6xl mx-auto p-6'>

        {selectedTopic === 'All' && <TimeSummary summary={timeSummary} />}

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
