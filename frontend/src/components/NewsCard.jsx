function NewsCard({data}) {

    const getSentimentDetails = (sentiment) => {
        switch (sentiment) {
            case 'บวก': return { label: 'บวก', color: 'bg-green-500' }
            case 'ลบ' : return { label: 'ลบ', color: 'bg-red-500' }
            case 'เป็นกลาง': return { label: 'เป็นกลาง', color: 'bg-gray-300' }
            default: return { label: '-', color: 'bg-gray-300' }
        }
    }
    
    const sentiment = getSentimentDetails(data.sentiment)

    return (
        <div className="bg-gray-100 rounded-xl shadow-sm hover:shadow-md transition p-6 border border-slate-200 flex flex-col h-full">
            
            <div className="text-[10px] font-bold uppercase tracking-widest mb-2">
                {data.source_name}
            </div>

            <h2 className="text-xl font-bold mb-2 text-slate-900 leading-snug">
                {data.title}
            </h2>

            <div className="flex justify-between items-center mb-4">
                <div className="flex flex-wrap gap-1">
                    {data.topics && data.topics.map((t, index) => (
                        <span key={index} className="text-[10px] bg-blue-50 text-blue-600 px-2 py-0.5 rounded font-medium">
                            #{t}
                        </span>
                    ))}
                </div>

                <div className="flex items-center gap-2 shrink-0 bg-slate-50 px-2 py-1 rounded-lg border border-slate-100">
                    <span className="text-[11px] text-slate-500 font-medium">
                        แนวโน้ม: {sentiment.label}
                    </span>
                    <div className={`w-2 h-2 rounded-full ${sentiment.color} shadow-sm`}></div>
                </div>
            </div>
            <div className="text-sm text-slate-600 whitespace-pre-line mb-4 flex-grow">
                {data.summary || "กำลังรอสรุปจาก AI . . ."}
            </div>

            <div className="border-t border-slate-200 pt-4 mt-auto">
                <div className="flex justify-between items-center mb-3">
                    <span className="text-xs text-slate-400">
                        {new Date(data.published_at).toLocaleString('th-TH', {
                            dateStyle: 'medium',
                            timeStyle: 'short',
                            timeZone: 'Asia/Bangkok'
                        })}
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
                rel="noreferrer"
                className="block w-full text-center py-2 bg-slate-200 hover:bg-slate-300 text-blue-600 rounded-lg text-sm font-medium transition-colors">
                    อ่านฉบับเต็ม
                </a>
            </div>
        </div>
    )
}

export default NewsCard