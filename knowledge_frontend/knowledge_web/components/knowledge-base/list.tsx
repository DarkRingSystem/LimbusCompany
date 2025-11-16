'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Trash2, Edit2, ChevronRight } from 'lucide-react'
import { listKnowledgeBases, deleteKnowledgeBase } from '@/lib/api'
import type { KnowledgeBase } from '@/lib/api'
import { toast } from 'react-hot-toast'

export function KnowledgeBaseList() {
  const [knowledgeBases, setKnowledgeBases] = useState<KnowledgeBase[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchKnowledgeBases()
  }, [])

  const fetchKnowledgeBases = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await listKnowledgeBases()
      setKnowledgeBases(data)
    } catch (err) {
      const message = err instanceof Error ? err.message : '加载知识库失败'
      setError(message)
      toast.error(message)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: string, name: string) => {
    if (!confirm(`您确定要删除知识库 "${name}" 吗？`)) {
      return
    }

    try {
      await deleteKnowledgeBase(id)
      setKnowledgeBases(knowledgeBases.filter(kb => kb.id !== id))
      toast.success('知识库删除成功')
    } catch (err) {
      const message = err instanceof Error ? err.message : '删除知识库失败'
      toast.error(message)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">{error}</p>
        <button
          onClick={fetchKnowledgeBases}
          className="mt-2 text-red-600 hover:text-red-800 font-medium"
        >
          再试一次
        </button>
      </div>
    )
  }

  if (knowledgeBases.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">还没有知识库</p>
        <p className="text-gray-400 mt-2">创建您的第一个知识库以开始使用</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {knowledgeBases.map((kb) => (
        <div
          key={kb.id}
          className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow"
        >
          <Link href={`/knowledge-bases/${kb.id}`}>
            <div className="p-6 cursor-pointer">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 hover:text-blue-600">
                    {kb.name}
                  </h3>
                  {kb.description && (
                    <p className="mt-2 text-sm text-gray-600 line-clamp-2">
                      {kb.description}
                    </p>
                  )}
                </div>
                <ChevronRight className="w-5 h-5 text-gray-400" />
              </div>
              
              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">
                    {kb.document_count} 个文档
                  </span>
                  <span className="text-gray-500">
                    {new Date(kb.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          </Link>

          <div className="px-6 py-3 bg-gray-50 border-t border-gray-200 flex gap-2">
            <button
              onClick={() => handleDelete(kb.id, kb.name)}
              className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded transition-colors"
            >
              <Trash2 className="w-4 h-4" />
              删除
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}

