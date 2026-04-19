function NewsCard({data}) {
    return (
        <div className="bg-gray-100 text-gray-700 rounded-xl shadow-sm hover:shadow-md transition p-6 border border-slate-200 flex flex-col h-full">
            <div className="text-xs font-bold uppercase tracking-wider mb-2">
                {data.source_name}
            </div>
            <h2 className="text-xl font-bold mb-3">{data.title}</h2>
            <div className="text-sm text-slate-600 whitespace-pre-line mb-4 flex-grow">
                {data.summary}
            </div>

            <div className="border-t border-slate-800 pt-4 mt-auto">
                <div className="flex justify-between items-center mb-3">
                    <span className="text-xs text-slate-400">
                        {new Date(data.published_at).toLocaleString('th-TH')}
                    </span>

                    {data.model_used && (
                        <span className="text-xs text-slate-500 font-medium">
                            สรุปโดย: <span className="text-slate-700">{data.model_used}</span>
                        </span>
                    )}
                </div>

                <a 
                href={data.url} 
                target="_blank" 
                className="block w-full text-center py-2 bg-slate-200 hover:bg-slate-300 text-blue-600 rounded-lg text-sm font-medium transition-colors">
                    อ่านฉบับเต็ม
                </a>
            </div>
        </div>
    )
}

export default NewsCard