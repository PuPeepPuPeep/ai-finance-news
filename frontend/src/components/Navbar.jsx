const topics = ["All", "Fed", "Crypto", "Stock Market", "Inflation", "Gold", "Tech"]

function Navbar({ activeTopic, onSelectTopic }) {
    return (
        <nav className="bg-gray-800 border-b border-slate-200 sticky top-0 z-10">
            <div className="max-w-6xl mx-auto px-4">
                <div className="flex items-center justify-between h-16">
                    <span className="text-xl font-bold text-blue-600">AI Finance</span>

                    <div className="flex space-x-2">
                        {topics.map((topic) => (
                            <button
                                key={topic}
                                onClick={() => onSelectTopic(topic)}
                                className={`px-3 py-2 rounded-md text-white text-sm font-medium transition-colors
                                    ${activeTopic === topic
                                        ? 'bg-blue-600'
                                        : 'text-slate-600 hover:bg-slate-500'
                                    }`}
                            >
                                {topic}
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        </nav>
    )
}

export default Navbar