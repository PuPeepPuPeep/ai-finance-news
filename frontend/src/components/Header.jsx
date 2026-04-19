import { useState, useEffect } from "react"
import { FaBars, FaGithub } from "react-icons/fa"
import { AiOutlineClose } from "react-icons/ai"

function Header({ activeTopic, onSelectTopic }) {
    const [isMenuOpen, setIsMenuOpen] = useState(false)
    const [topics, setTopics] = useState(["All"])

    useEffect(() => {
        fetch("http://localhost:8000/topics")
        .then((res) => res.json())
        .then((data) => setTopics(["All", ...data]))
        .catch((err) => console.error("Error feching topics:", err))
    }, [])

    return (
        <header className="sticky top-0 z-50 bg-gray-800 border-b border-slate-200">
            <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <button
                        className="md:hidden p-2 text-slate-600 hover:bg-slate-100 rounded"
                        onClick={() => setIsMenuOpen(true)}
                    >
                        <FaBars className="w-6 h-6" />
                    </button>
                    <span className="text-xl font-bold text-blue-600">AI News</span>
                </div>
                <a
                    href="https://github.com"
                    target="_blank"
                    rel="noreferrer"
                    className="text-slate-600 hover:text-black"
                >
                    <FaGithub className="w-8 h-8" />
                </a>
            </div>

            {/* Mobile */}
            <div
                className={`fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity duration-300 ${isMenuOpen ? 'opacity-50' : 'opacity-0 pointer-events-none'}`}
                onClick={() => setIsMenuOpen(false)}
            >
            </div>

            <div className={`fixed top-0 left-0 h-full w-64 bg-white z-50 transform transition-transform duration-300 ease-in-out ${isMenuOpen ? 'translate-x-0' : '-translate-x-full'}`}>
                <div className="p-4 border-b flex justify-between items-center">
                    <span className="font-bold text-lg">Menu</span>
                    <button onClick={() => setIsMenuOpen(false)} className="p-2 text-slate-600">
                        <AiOutlineClose className="w-6 h-6" />
                    </button>
                </div>
                <nav className="p-4 flex flex-col gap-2">
                    {topics.map((topic) => (
                        <button
                            key={topic}
                            onClick={() => { onSelectTopic(topic); setIsMenuOpen(false); }}
                            className={`px-4 py-3 rounded-md text-left font-medium transition-colors
                                ${activeTopic === topic
                                    ? 'bg-blue-600'
                                    : 'hover:bg-slate-100'
                                }`}
                        >
                            {topic}
                        </button>
                    ))}
                </nav>
            </div>

            {/* Desktop */}
            <nav className="hidden md:block bg-white border-t border-slate-100">
                <div className="max-w-6xl mx-auto px-4 py-3 flex flex-wrap gap-2">
                    {topics.map((topic) => (
                        <button
                            key={topic}
                            onClick={() => onSelectTopic(topic)}
                            className={`px-3 py-3 rounded-md text-sm font-medium transition-colors ${
                                activeTopic === topic ? 'bg-blue-600 text-white' : 'text-slate-600 hover:bg-slate-100'
                            }`}
                        >
                            {topic}
                        </button>
                    ))}
                </div>
            </nav>
        </header>
    )
}

export default Header