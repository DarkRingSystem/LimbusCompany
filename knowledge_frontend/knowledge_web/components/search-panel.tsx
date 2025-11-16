'use client'

import { useState } from 'react'
import { Search, AlertCircle } from 'lucide-react'
import { searchKnowledgeBase } from '@/lib/api'
import type { RetrievalResponse } from '@/lib/api'
import { toast } from 'react-hot-toast'

interface SearchPanelProps {
  kbId: string
}

export function SearchPanel({ kbId }: SearchPanelProps) {
  const [query, setQuery] = useState('')
  const [topK, setTopK] = useState(5)
  const [retrievalType, setRetrievalType] = useState<'vector' | 'hybrid'>('vector')
  const [results, setResults] = useState<RetrievalResponse | null>(null)
  const [isSearching, setIsSearching] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async () => {
    if (!query.trim()) {
      toast.error('请输入搜索查询')
      return
    }

    try {
      setIsSearching(true)
      setError(null)
      const data = await searchKnowledgeBase(kbId, query, topK, retrievalType)
      setResults(data)
    } catch (err) {
      const message = err instanceof Error ? err.message : '搜索失败'
      setError(message)
      toast.error(message)
    } finally {
      setIsSearching(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !isSearching) {
      handleSearch()
    }
  }

  return (
    <div className="space-y-6">
      {/* Search Input */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            搜索查询
          </label>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="请输入您的搜索查询..."
            rows={3}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              返回结果数量
            </label>
            <input
              type="number"
              min="1"
              max="20"
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              检索类型
            </label>
            <select
              value={retrievalType}
              onChange={(e) => setRetrievalType(e.target.value as 'vector' | 'hybrid')}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="vector">向量搜索</option>
              <option value="hybrid" disabled>混合搜索 (即将推出)</option>
            </select>
          </div>
        </div>

        <button
          onClick={handleSearch}
          disabled={isSearching}
          className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
        >
          <Search className="w-5 h-5" />
          {isSearching ? '搜索中...' : '搜索'}
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Results */}
      {results && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">
              结果 ({results.results.length})
            </h3>
            <span className="text-sm text-gray-600">
              查询: "{results.query}"
            </span>
          </div>

          {results.results.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500">未找到结果</p>
            </div>
          ) : (
            <div className="space-y-4">
              {results.results.map((result, index) => (
                <div
                  key={result.chunk_id}
                  className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {result.document_name}
                      </p>
                      <p className="text-xs text-gray-500">
                        分块 {result.chunk_index}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-semibold text-blue-600">
                        {(result.similarity_score * 100).toFixed(1)}%
                      </p>
                      <p className="text-xs text-gray-500">相关度</p>
                    </div>
                  </div>

                  <div className="mt-3 p-3 bg-gray-50 rounded border border-gray-200">
                    <p className="text-sm text-gray-700 line-clamp-3">
                      {result.content}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

