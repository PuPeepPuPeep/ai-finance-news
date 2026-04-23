import { FaGithub } from "react-icons/fa"

function Footer() {
    return (
        <footer className="bg-gray-800 border-t border-slate-200 mt-12 py-6">
            <div className="max-w-6xl mx-auto px-4 flex items-center justify-between">
                <span className="text-sm text-slate-100">
                    เนื้อหาที่สรุปโดย AI อาจมีความผิดพลาดได้
                </span>
                <a
                    href="https://github.com/PuPeepPuPeep/ai-finance-news"
                    target="_blank"
                    rel="noreferrer"
                    className="text-white hover:text-slate-600 transition-colors"
                >
                    <FaGithub className="w-8 h-8" />
                </a>
            </div>
        </footer>
    )
}

export default Footer