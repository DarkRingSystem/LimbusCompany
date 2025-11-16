'use client'

import { useState, useEffect } from 'react'
import { Trash2, Settings, Upload } from 'lucide-react'
import { listDocuments, deleteDocument } from '@/lib/api'
import type { Document } from '@/lib/api'
import { DocumentUpload } from '@/components/document-upload'
import { toast } from 'react-hot-toast'

interface DocumentListProps {
  kbId: string
  onRefresh: () => void
}

export function DocumentList({ kbId, onRefresh }: DocumentListProps) {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showUpload, setShowUpload] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchDocuments()
  }, [kbId])

  const fetchDocuments = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await listDocuments(kbId)
      setDocuments(data)
    } catch (err) {
      const message = err instanceof Error ? err.message : '加载文档失败'
      setError(message)
      toast.error(message)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (docId: string, docName: string) => {
    if (!confirm(`您确定要删除文档 "${docName}" 吗？`)) {
      return
    }

    try {
      await deleteDocument(docId)
      setDocuments(documents.filter(doc => doc.id !== docId))
      onRefresh()
      toast.success('文档删除成功')
    } catch (err) {
      const message = err instanceof Error ? err.message : '删除文档失败'
      toast.error(message)
    }
  }

  const handleUploadComplete = () => {
    setShowUpload(false)
    fetchDocuments()
    onRefresh()
  }

  const filteredDocuments = documents.filter(doc =>
    doc.name.toLowerCase().includes(searchTerm.toLowerCase())
  )

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
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Upload Section */}
      {showUpload && (
        <DocumentUpload kbId={kbId} onComplete={handleUploadComplete} />
      )}

      {/* Search and Upload Button */}
      <div className="flex gap-4">
        <input
          type="text"
          placeholder="搜索文档..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <button
          onClick={() => setShowUpload(!showUpload)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Upload className="w-4 h-4" />
          上传文档
        </button>
      </div>

      {/* Documents Table */}
      {filteredDocuments.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">还没有文档</p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">名称</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">类型</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">大小</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">分块数</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">召回次数</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">状态</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">操作</th>
              </tr>
            </thead>
            <tbody>
              {filteredDocuments.map((doc) => (
                <tr key={doc.id} className="border-b border-gray-200 hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm text-gray-900">{doc.name}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{doc.file_type}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {(doc.file_size / 1024 / 1024).toFixed(2)} MB
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">{doc.chunk_count}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{doc.recall_count}</td>
                  <td className="px-6 py-4 text-sm">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-medium ${
                        doc.status === 'completed'
                          ? 'bg-green-100 text-green-800'
                          : doc.status === 'processing'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {doc.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm">
                    <div className="flex gap-2">
                      <button
                        className="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                        title="分块设置"
                      >
                        <Settings className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(doc.id, doc.name)}
                        className="p-2 text-gray-400 hover:text-red-600 transition-colors"
                        title="删除文档"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

