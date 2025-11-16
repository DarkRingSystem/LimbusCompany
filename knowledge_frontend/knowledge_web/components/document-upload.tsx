'use client'

import { useState } from 'react'
import { uploadDocuments } from '@/lib/api'
import { FileUpload } from '@/components/file-upload'
import { ChunkingConfig } from '@/components/chunking-config'
import { toast } from 'react-hot-toast'

interface DocumentUploadProps {
  kbId: string
  onComplete: () => void
}

export function DocumentUpload({ kbId, onComplete }: DocumentUploadProps) {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])
  const [chunkSize, setChunkSize] = useState(1024)
  const [chunkOverlap, setChunkOverlap] = useState(200)
  const [isUploading, setIsUploading] = useState(false)

  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      toast.error('请选择要上传的文件')
      return
    }

    try {
      setIsUploading(true)
      await uploadDocuments(kbId, selectedFiles, chunkSize, chunkOverlap)
      toast.success('文档上传成功')
      setSelectedFiles([])
      onComplete()
    } catch (err) {
      const message = err instanceof Error ? err.message : '上传文档失败'
      toast.error(message)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-6">上传新文档</h3>
      
      <div className="space-y-6">
        <FileUpload onFilesSelected={setSelectedFiles} />
        
        {selectedFiles.length > 0 && (
          <>
            <ChunkingConfig
              chunkSize={chunkSize}
              chunkOverlap={chunkOverlap}
              onChunkSizeChange={setChunkSize}
              onChunkOverlapChange={setChunkOverlap}
            />
            
            <div className="flex justify-end gap-4">
              <button
                onClick={() => setSelectedFiles([])}
                disabled={isUploading}
                className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:bg-gray-100 transition-colors"
              >
                取消
              </button>
              <button
                onClick={handleUpload}
                disabled={isUploading}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {isUploading ? '上传中...' : '上传文档'}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

