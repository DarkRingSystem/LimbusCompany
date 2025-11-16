'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { ArrowLeft, Plus } from 'lucide-react'
import { getKnowledgeBase } from '@/lib/api'
import type { KnowledgeBase } from '@/lib/api'
import { DocumentList } from '@/components/document-list'
import { SearchPanel } from '@/components/search-panel'
import { toast } from 'react-hot-toast'

interface KnowledgeBaseDetailProps {
  kbId: string
}

export function KnowledgeBaseDetail({ kbId }: KnowledgeBaseDetailProps) {
  const [kb, setKb] = useState<KnowledgeBase | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'documents' | 'search'>('documents')

  useEffect(() => {
    fetchKnowledgeBase()
  }, [kbId])

  const fetchKnowledgeBase = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getKnowledgeBase(kbId)
      setKb(data)
    } catch (err) {
      const message = err instanceof Error ? err.message : '加载知识库失败'
      setError(message)
      toast.error(message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error || !kb) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Link href="/" className="flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-4">
          <ArrowLeft className="w-4 h-4" />
          返回知识库列表
        </Link>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error || '未找到知识库'}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <Link href="/" className="flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-4">
          <ArrowLeft className="w-4 h-4" />
          返回知识库列表
        </Link>
        
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{kb.name}</h1>
            {kb.description && (
              <p className="mt-2 text-gray-600">{kb.description}</p>
            )}
            <p className="mt-2 text-sm text-gray-500">
              创建于 {new Date(kb.created_at).toLocaleDateString()}
            </p>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">文档</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{kb.document_count}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">最后更新</p>
          <p className="text-lg font-semibold text-gray-900 mt-2">
            {new Date(kb.updated_at).toLocaleDateString()}
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">状态</p>
          <p className="text-lg font-semibold text-green-600 mt-2">活跃</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <div className="flex">
            <button
              onClick={() => setActiveTab('documents')}
              className={`px-6 py-4 font-medium border-b-2 transition-colors ${
                activeTab === 'documents'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-600 hover:text-gray-900'
              }`}
            >
              文档
            </button>
            <button
              onClick={() => setActiveTab('search')}
              className={`px-6 py-4 font-medium border-b-2 transition-colors ${
                activeTab === 'search'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-600 hover:text-gray-900'
              }`}
            >
              召回测试
            </button>
          </div>
        </div>

        <div className="p-6">
          {activeTab === 'documents' && (
            <DocumentList kbId={kbId} onRefresh={fetchKnowledgeBase} />
          )}
          {activeTab === 'search' && (
            <SearchPanel kbId={kbId} />
          )}
        </div>
      </div>
    </div>
  )
}

